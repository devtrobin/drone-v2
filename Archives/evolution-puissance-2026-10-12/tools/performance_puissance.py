"""Prévisions 37D / LiPo 3S : aucune validation physique ou boucle de vitesse."""
from pathlib import Path
import argparse
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]


def calculate(h):
    mass = sum(p['mass_kg'] for p in h['mass_items'])
    cg = {axis: sum(p['mass_kg'] * p[axis + '_m'] for p in h['mass_items']) / mass
          for axis in ('x', 'z')}
    g, radius, track = 9.80665, h['wheel_diameter_m'] / 2, h['track_m']
    front = (h['caster_x_m'] - cg['x']) / (h['caster_x_m'] - h['axle_x_m'])
    if not 0 < front < 1:
        raise ValueError('Centre de gravité hors triangle de support')
    torque_12 = h['stall_torque_kg_cm_at_12v'] * .0980665
    rows = []
    for voltage in h['pack_voltages_v']:
        effective = max(0, voltage * h['target_max_duty'] - h['driver_drop_v'])
        stall_torque = torque_12 * effective / 12
        resistance = h['rolling_coefficient'] * mass * g
        torque_each = resistance * radius / 2
        load_ratio = torque_each / stall_torque
        rpm = h['no_load_rpm_at_12v'] * effective / 12 * max(0, 1 - load_ratio)
        speed = rpm * 2 * math.pi * radius / 60
        current = h['no_load_current_a_at_12v'] + (
            h['stall_current_a_at_12v'] - h['no_load_current_a_at_12v']) * load_ratio
        power = 2 * voltage * current + h['pi_video_power_w'] / h['ubec_efficiency']
        rows.append({'pack_v': voltage, 'effective_motor_v': effective,
                     'loaded_rpm_estimate': rpm, 'speed_km_h': speed * 3.6,
                     'motor_current_each_a_estimate': current,
                     'straight_power_w_estimate': power})
    adhesion_force = h['adhesion_coefficient'] * mass * g * front
    nominal_torque = torque_12 * (h['nominal_pack_v'] * h['target_max_duty']
                                  - h['driver_drop_v']) / 12
    conservative_torque_force = 2 * nominal_torque * h['working_stall_fraction'] / radius
    traction = min(adhesion_force, conservative_torque_force)
    rolling = h['rolling_coefficient'] * mass * g
    scenarios = []
    energy = h['nominal_pack_v'] * h['capacity_ah']
    usable = energy * h['usable_energy_fraction']
    for scenario in h['power_scenarios']:
        hours = usable / scenario['power_w']
        scenarios.append(dict(scenario, autonomy_minutes=hours * 60,
                              distance_km=hours * scenario['mean_speed_km_h']))
    stall_each = h['stall_current_a_at_12v'] * h['full_pack_v'] / 12
    # Full PWM is a fault/startup bound, not the configured initial duty.
    stall_bus = 2 * stall_each + h['pi_video_power_w'] / (
        h['ubec_efficiency'] * h['full_pack_v'])
    profile = json.loads((ROOT/'Logiciel/config/robot.puissance.example.json').read_text())
    full_v0 = h['no_load_rpm_at_12v'] * (h['full_pack_v'] - h['driver_drop_v']) / 12
    full_v0 *= 2 * math.pi * radius / 60
    lateral = 0
    for t_i in range(101):
        for yaw_i in range(101):
            t, yaw = t_i / 100, yaw_i / 100
            v = full_v0 * t * h['target_max_duty'] * (1 - .5 * yaw)
            omega = full_v0 * 2 * yaw * profile['max_turn_duty'] * (1 - .5 * t) / track
            lateral = max(lateral, v * omega)
    margin_x = min(cg['x'] - h['axle_x_m'], h['caster_x_m'] - cg['x'])
    # Distance to slanted edge of the triangular support polygon (CG y = 0).
    half_track = track / 2
    slope = half_track / (h['caster_x_m'] - h['axle_x_m'])
    margin_y = half_track * front / math.sqrt(1 + slope * slope)
    return {'hardware_verified': False, 'revision': 'puissance-2026-10-12',
            'mass_kg_estimate': mass, 'cg_m_estimate': cg,
            'drive_axle_weight_fraction': front, 'speed_predictions': rows,
            'energy_wh_nominal_per_pack': energy, 'energy_wh_usable_assumed': usable,
            'autonomy_scenarios': scenarios, 'traction_force_n_assumed': traction,
            'flat_resistance_n_assumed': rolling,
            'flat_force_margin_ratio': traction / rolling if rolling else None,
            'acceleration_traction_bound_m_s2': (traction - rolling) / mass,
            'resistance_at_10_percent_grade_n': mass*g*(math.sin(math.atan(.1))
                + h['rolling_coefficient']*math.cos(math.atan(.1))),
            'unlimited_stall_current_each_a_at_full_pack': stall_each,
            'unlimited_stall_source_current_a_estimate': stall_bus,
            'initial_profile_max_duty': profile['max_duty'],
            'target_profile_max_duty_after_tests': h['target_max_duty'],
            'turn_duty_limit': profile['max_turn_duty'],
            'ideal_pivot_rpm_at_nominal_pack': (h['no_load_rpm_at_12v']
                * (h['nominal_pack_v'] - h['driver_drop_v']) / 12
                * 2*math.pi*radius/60 * 2*profile['max_turn_duty']/track
                * 60/(2*math.pi)),
            'ideal_lateral_acceleration_grid_max_m_s2': lateral,
            'assumed_static_tipping_acceleration_x_m_s2': g * margin_x / cg['z'],
            'assumed_static_tipping_acceleration_edge_m_s2': g * margin_y / cg['z'],
            'radius_at_8kmh_for_1_5m_s2_m': (8/3.6)**2/1.5,
            'kinetic_energy_at_8kmh_j': .5*mass*(8/3.6)**2,
            'limitations': h['limitations']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT/'Validation/resultats/performance-puissance.json')
    args = parser.parse_args()
    path = ROOT/'Mecanique/hypotheses-puissance.json'
    result = calculate(json.loads(path.read_text()))
    result['sources'] = []
    for source in [path, Path(__file__), ROOT/'Sources/motorisation-puissance.json',
                   ROOT/'Logiciel/config/robot.puissance.example.json']:
        result['sources'].append({'file': str(source.relative_to(ROOT)),
            'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(f"Masse estimée {result['mass_kg_estimate']:.3f} kg ; vitesses : " +
          ', '.join(f"{v['speed_km_h']:.2f} km/h ({v['pack_v']} V)"
                    for v in result['speed_predictions']))


if __name__ == '__main__':
    main()
