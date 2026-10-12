"""Mixage et sorties : DRV8833 en roue libre ; deux MD13S PWM/DIR avec freinage."""
import logging
import time

from .config import number

LOG = logging.getLogger(__name__)


def mix(throttle, turn, maximum):
    number(throttle, "throttle", -1, 1)
    number(turn, "turn", -1, 1)
    # Positive turn = right: left wheel faster than right wheel.
    left, right = throttle + turn, throttle - turn
    scale = max(1, abs(left), abs(right))
    return left / scale * maximum, right / scale * maximum


def limited_mix(throttle, turn, maximum, turn_maximum):
    """Réduire l'avance en virage et la rotation en déplacement ; boucle ouverte."""
    number(throttle, 'throttle', -1, 1)
    number(turn, 'turn', -1, 1)
    forward = throttle * maximum * (1 - .5 * abs(turn))
    yaw = turn * turn_maximum * (1 - .5 * abs(throttle))
    return forward + yaw, forward - yaw


class SimBackend:
    def __init__(self):
        self.left = self.right = 0.0
        self.enabled = False
        self.events = []

    def outputs(self, left, right):
        if (left, right) != (self.left, self.right):
            self.events.append(("outputs", left, right))
            LOG.info("SIM moteurs gauche=%.3f droite=%.3f", left, right)
        self.left, self.right = left, right

    def enable(self, enabled):
        if enabled != self.enabled:
            self.events.append(("sleep", enabled))
            LOG.info("SIM nSLEEP=%s", enabled)
        self.enabled = enabled

    def close(self):
        self.enable(False)
        self.outputs(0, 0)


class GPIOBackend:
    def __init__(self, config, factory=None):
        if config.driver != 'drv8833':
            raise ValueError('GPIOBackend DRV8833 incompatible avec ce pilote')
        if not config.hardware_confirmed:
            raise ValueError("Câblage non confirmé : hardware_confirmed doit être validé")
        from gpiozero import DigitalOutputDevice, PWMOutputDevice
        if factory is None:
            from gpiozero.pins.lgpio import LGPIOFactory
            factory = LGPIOFactory()
        self.factory = factory
        self.devices = []
        try:
            self.sleep = DigitalOutputDevice(config.pins["sleep"], initial_value=False,
                                             pin_factory=self.factory)
            self.devices.append(self.sleep)
            self.pwm = []
            for name in ("left_forward", "left_reverse", "right_forward", "right_reverse"):
                device = PWMOutputDevice(config.pins[name], initial_value=0,
                                         frequency=config.pwm_hz, pin_factory=self.factory)
                self.devices.append(device)
                self.pwm.append(device)
        except BaseException:
            self.close()
            raise

    def outputs(self, left, right):
        # Zero both inputs before changing direction; never drive both high for braking.
        for forward, reverse, value in ((self.pwm[0], self.pwm[1], left),
                                        (self.pwm[2], self.pwm[3], right)):
            forward.value = reverse.value = 0
            if value > 0:
                forward.value = value
            elif value < 0:
                reverse.value = -value

    def enable(self, enabled):
        self.sleep.value = enabled

    def close(self):
        try:
            if self.devices:
                self.devices[0].off()
        finally:
            for device in reversed(self.devices):
                device.close()
            self.devices.clear()
            self.factory.close()


class MD13SBackend:
    """Deux MD13S en mode PWM/DIR ; PWM bas = arrêt avec freinage du pilote."""

    def __init__(self, config, factory=None):
        if not config.hardware_confirmed:
            raise ValueError('Câblage non confirmé : hardware_confirmed doit être validé')
        if config.driver != 'md13s':
            raise ValueError('Profil MD13S requis')
        from gpiozero import DigitalOutputDevice, PWMOutputDevice
        if factory is None:
            from gpiozero.pins.lgpio import LGPIOFactory
            factory = LGPIOFactory()
        self.factory, self.devices = factory, []
        self.enabled = False
        self.channels = []
        try:
            for side in ('left', 'right'):
                # Ouvrir le PWM à zéro avant toute modification de DIR.
                pwm = PWMOutputDevice(config.pins[side + '_pwm'], initial_value=0,
                                      frequency=config.pwm_hz, pin_factory=factory)
                self.devices.append(pwm)
                direction = DigitalOutputDevice(config.pins[side + '_dir'],
                                                 initial_value=False, pin_factory=factory)
                self.devices.append(direction)
                self.channels.append((pwm, direction))
        except BaseException:
            self.close()
            raise

    def outputs(self, left, right):
        for (pwm, direction), value in zip(self.channels, (left, right)):
            pwm.value = 0
            direction.value = value < 0
            pwm.value = abs(value) if self.enabled else 0

    def enable(self, enabled):
        self.enabled = bool(enabled)
        if not self.enabled:
            for pwm, _ in self.channels:
                pwm.value = 0

    def close(self):
        try:
            self.enable(False)
        finally:
            for device in reversed(self.devices):
                device.close()
            self.devices.clear()
            self.factory.close()


def gpio_backend(config, factory=None):
    implementation = MD13SBackend if config.driver == 'md13s' else GPIOBackend
    return implementation(config, factory=factory)


class MotorController:
    def __init__(self, backend, config, clock=time.monotonic):
        self.backend, self.config, self.clock = backend, config, clock
        self.last = (0.0, 0.0)
        self.paused_until = 0.0
        self.enabled = False
        self.last_update = self.clock()
        self.stop()

    def stop(self):
        if self.enabled:
            self.paused_until = self.clock() + self.config.reverse_pause_s
        self.backend.enable(False)
        self.backend.outputs(0, 0)
        self.last = (0.0, 0.0)
        self.enabled = False
        self.last_update = self.clock()

    def command(self, enabled, throttle, turn):
        now = self.clock()
        target = (mix(throttle, turn, self.config.max_duty)
                  if self.config.max_turn_duty is None else
                  limited_mix(throttle, turn, self.config.max_duty, self.config.max_turn_duty))
        if self.config.invert_left:
            target = (-target[0], target[1])
        if self.config.invert_right:
            target = (target[0], -target[1])
        if not enabled or target == (0, 0):
            self.stop()
            return
        if any(old * new < 0 for old, new in zip(self.last, target)):
            self.stop()
            self.paused_until = now + self.config.reverse_pause_s
            return
        if now < self.paused_until:
            self.stop()
            return
        if not self.enabled:
            # Wake delay is performed with all motor inputs still low.
            self.backend.enable(True)
            self.enabled = True
            time.sleep(self.config.wake_delay_s)
        if self.config.ramp_per_s:
            # Une commande retardée ne doit pas produire un saut de vitesse.
            dt = min(.1, max(0, now - self.last_update))
            step = self.config.ramp_per_s * dt
            target = tuple(old + max(-step, min(step, new - old))
                           for old, new in zip(self.last, target))
        if target != self.last:
            self.backend.outputs(*target)
        self.last = target
        self.last_update = now

    def close(self):
        try:
            self.stop()
        finally:
            self.backend.close()
