"""Prévision mécanique et énergétique du V2 ; aucune mesure du prototype."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from pre_dimensionnement import autonomy, finite, stability

ROOT = Path(__file__).resolve().parents[1]
G = 9.81


def traction(mass_kg, radius_m, stall_torque_nm, drive_normal_n,
             rolling_coefficient, adhesion, slope_deg=0, acceleration=0,
             torque_fraction=0.25):
    """Effort longitudinal ; couple de blocage distinct du couple de travail."""
    m, r, ts, nd = [finite(v, label, True) for v, label in
                   [(mass_kg, 'masse'), (radius_m, 'rayon'),
                    (stall_torque_nm, 'couple'), (drive_normal_n, 'réaction')]]
    cr, mu, q = [finite(v, label, True) for v, label in
                 [(rolling_coefficient, 'roulement'), (adhesion, 'adhérence'),
                  (torque_fraction, 'fraction de couple')]]
    if q > 1 or nd > m * G + 1e-8:
        raise ValueError('Fraction de couple ou réaction incohérente')
    theta = math.radians(finite(slope_deg, 'pente'))
    a = finite(acceleration, 'accélération')
    required = m * G * (cr * math.cos(theta) + math.sin(theta)) + m * a
    motor = 2 * ts * q / r
    grip = mu * nd * math.cos(theta)
    usable = min(motor, grip)
    return {'required_force_n': required, 'motor_work_force_n': motor,
            'adhesion_limit_n': grip, 'usable_force_n': usable,
            'margin_ratio': usable / required if required > 0 else None,
            'can_move_under_assumptions': required <= usable,
            'required_torque_per_motor_nm': max(0, required) * r / 2}


def speed(no_load_rpm, stall_torque_nm, radius_m, force_n, duty=1):
    n0, ts, r = [finite(v, label, True) for v, label in
                 [(no_load_rpm, 'tr/min'), (stall_torque_nm, 'couple'),
                  (radius_m, 'rayon')]]
    d = finite(duty, 'PWM', True)
    if d > 1:
        raise ValueError('PWM > 1')
    load_fraction = max(0, finite(force_n, 'effort')) * r / (2 * ts)
    # Approximation tension moyenne et droite couple/vitesse d'un moteur CC.
    rpm = n0 * max(0, d - load_fraction)
    v = rpm * 2 * math.pi * r / 60
    return {'wheel_rpm': rpm, 'speed_m_s': v, 'speed_km_h': v * 3.6,
            'stall_torque_fraction': load_fraction, 'duty': d}


def differential(left_m_s, right_m_s, track_m):
    b = finite(track_m, 'voie', True)
    left, right = finite(left_m_s, 'gauche'), finite(right_m_s, 'droite')
    v, omega = (left + right) / 2, (right - left) / b
    return {'axle_speed_m_s': v, 'yaw_rate_rad_s': omega,
            'radius_m': v / omega if abs(omega) > 1e-12 else None,
            'full_turn_s': 2 * math.pi / abs(omega) if abs(omega) > 1e-12 else None}


def compute(data):
    geom, motor = data['geometry'], data['motor_analogue']
    masses = data['masses']
    st = stability(geom['support_points_mm'], masses)
    m = st['total_mass_g'] / 1000
    cx, cy, _ = st['center_of_mass_mm']
    axle, caster = geom['axle_x_mm'], geom['caster_x_mm']
    b = geom['track_mm'] / 1000
    length = (caster - axle) / 1000
    drive_fraction = (caster - cx) / (caster - axle)
    weight = m * G
    nd, nc = weight * drive_fraction, weight * (1 - drive_fraction)
    nl, nr = nd / 2 + weight * cy / (b * 1000), nd / 2 - weight * cy / (b * 1000)
    if min(nl, nr, nc) <= 0:
        raise ValueError('Un des trois appuis est déchargé')
    # Interpolations d'un moteur analogue entre les tensions documentées.
    voltage = data['effective_motor_voltage_v']
    n0 = 185 + (voltage - 4.5) * (250 - 185) / (6 - 4.5)
    ts = motor['stall_torque_6v_kg_cm'] * 0.0980665 * voltage / 6
    stall_i = 1.2 + (voltage - 4.5) * (1.5 - 1.2) / 1.5
    radius = geom['wheel_diameter_mm'] / 2000
    cr, mu = data['rolling_coefficient'], data['adhesion_coefficient']
    q = data['working_torque_fraction']
    scenarios = {}
    for name, slope, acc in [('plat', 0, 0), ('demarrage_progressif', 0, 0.3),
                             ('pente_5_deg', 5, 0), ('pente_10_deg', 10, 0)]:
        scenarios[name] = traction(m, radius, ts, nd, cr, mu, slope, acc, q)
    flat = scenarios['plat']['required_force_n']
    velocities = {name: speed(n0, ts, radius, flat, duty) for name, duty in
                  [('full_pwm', 1), ('configured_pwm', data['configured_max_duty'])]}
    inertia = sum(item['mass_g'] / 1000 * (
        ((item['center_mm'][0] - axle) / 1000) ** 2
        + (item['center_mm'][1] / 1000) ** 2
        + (item['body_xy_mm'][0] ** 2 + item['body_xy_mm'][1] ** 2) / 12e6
    ) for item in masses)
    # Moment disponible limité par la roue la moins chargée ; pas de glissement latéral.
    yaw_motor = 2 * ts * q / radius * b / 2
    yaw_grip = 2 * mu * min(nl, nr) * b / 2
    yaw_available = min(yaw_motor, yaw_grip)
    yaw_tests = {}
    for name, coefficient in data['caster_lateral_coefficients'].items():
        resistance = coefficient * nc * length + cr * nd * b / 2
        required = resistance + inertia * data['yaw_acceleration_rad_s2']
        yaw_tests[name] = {'assumed_caster_lateral_coefficient': coefficient,
                           'resisting_moment_nm': resistance,
                           'required_moment_nm': required,
                           'available_moment_nm': yaw_available,
                           'margin_ratio': yaw_available / required,
                           'can_turn_under_assumptions': required <= yaw_available}
    turn_speed = speed(n0, ts, radius,
                       2 * yaw_tests['appui_libre_aligne']['required_moment_nm'] / b,
                       data['configured_max_duty'])
    v = turn_speed['speed_m_s']
    power = data['energy']
    energy_wh = power['capacity_cell_mah'] / 1000 * power['assumed_cell_voltage_v']
    nominal_energy = energy_wh * power['conversion_efficiency'] * power['usable_fraction']
    runtimes = {name: autonomy(energy_wh, power['conversion_efficiency']
                              * power['usable_fraction'], watts)
                for name, watts in power['power_scenarios_5v_w'].items()}
    startup_i = 2 * stall_i + power['pi_camera_current_a'] + power['driver_idle_current_a']
    sensitivities = []
    for mm, cc, aa, tq in [(0.38, .03, .6, 1), (.65, .10, .3, .5), (.65, .15, .3, .5)]:
        # Même répartition relative des masses, différent sol et moteur plus faible.
        sensitivities.append({'mass_kg': mm, 'rolling_coefficient': cc, 'adhesion': aa,
                              'torque_multiplier': tq,
                              **traction(mm, radius, ts * tq, mm * G * drive_fraction,
                                         cc, aa, torque_fraction=q)})
    return {'status': 'prévision sous hypothèses, aucune validation matérielle',
            'hardware_verified': False, 'stability': st,
            'reactions_n': {'drive_total': nd, 'left': nl, 'right': nr, 'caster': nc},
            'analogue_at_assumed_voltage': {'voltage_v': voltage,
                'no_load_rpm': n0, 'stall_torque_nm': ts, 'stall_current_a': stall_i},
            'traction': scenarios, 'speed': velocities, 'sensitivity': sensitivities,
            'speed_voltage_sensitivity': {str(vv): speed(
                185 + (vv - 4.5) * 65 / 1.5,
                motor['stall_torque_6v_kg_cm'] * .0980665 * vv / 6,
                radius, flat) for vv in [4, 5]},
            'turning': {'yaw_inertia_kg_m2': inertia, 'moment_tests': yaw_tests,
                'aligned_turn_wheel_speed': turn_speed,
                'opposite_wheels_ideal': differential(-v, v, b),
                'one_wheel_stopped_ideal': differential(0, v, b),
                'swept_diameter_upper_bound_m': geom['swept_diameter_bound_mm'] / 1000},
            'energy': {'cell_energy_wh': energy_wh, 'usable_energy_wh': nominal_energy,
                'runtimes': runtimes,
                'range_hours': [energy_wh * .75 * .85 / 10, energy_wh * .9 * .95 / 5],
                'full_duty_two_motor_startup_plus_pi_a': startup_i,
                'startup_estimate_at_5v_a': 2 * 1.3 + power['pi_camera_current_a']
                                          + power['driver_idle_current_a'],
                'announced_usb_limit_a': power['announced_usb_limit_a'],
                'startup_within_announced_limit': startup_i <= power['announced_usb_limit_a']}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT/'Mecanique/hypotheses-performance.json')
    parser.add_argument('--output', type=Path, default=ROOT/'Validation/resultats/performance.json')
    args = parser.parse_args()
    result = compute(json.loads(args.input.read_text()))
    result['sources'] = [{'file': str(path.relative_to(ROOT)),
                         'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                        for path in [args.input, Path(__file__),
                                     ROOT/'tools/pre_dimensionnement.py',
                                     ROOT/'Assemblage/implantation.json',
                                     ROOT/'Logiciel/config/robot.example.json']]
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
