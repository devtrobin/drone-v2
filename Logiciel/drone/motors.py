"""Mixage différentiel et sorties DRV8833 ; arrêt en roue libre, sans freinage."""
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



class MotorController:
    def __init__(self, backend, config, clock=time.monotonic):
        self.backend, self.config, self.clock = backend, config, clock
        self.last = (0.0, 0.0)
        self.paused_until = 0.0
        self.enabled = False
        self.stop()

    def stop(self):
        if self.enabled:
            self.paused_until = self.clock() + self.config.reverse_pause_s
        self.backend.enable(False)
        self.backend.outputs(0, 0)
        self.last = (0.0, 0.0)
        self.enabled = False

    def command(self, enabled, throttle, turn):
        now = self.clock()
        target = mix(throttle, turn, self.config.max_duty)
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
        if target != self.last:
            self.backend.outputs(*target)
        self.last = target

    def close(self):
        try:
            self.stop()
        finally:
            self.backend.close()
