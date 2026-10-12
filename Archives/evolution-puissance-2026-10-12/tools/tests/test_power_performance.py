"""Sanity checks against published motor points and battery energy limits."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
from performance_puissance import calculate


class PowerPerformanceTests(unittest.TestCase):
    def setUp(self):
        self.h = json.loads((ROOT/'Mecanique/hypotheses-puissance.json').read_text())

    def test_unloaded_motor_matches_published_six_volt_point(self):
        h = copy.deepcopy(self.h)
        h.update(rolling_coefficient=0, driver_drop_v=0, target_max_duty=1,
                 pack_voltages_v=[6])
        result = calculate(h)
        self.assertAlmostEqual(result['speed_predictions'][0]['loaded_rpm_estimate'], 265)

    def test_battery_energy_excludes_spare_and_duration_falls_with_power(self):
        result = calculate(self.h)
        self.assertAlmostEqual(result['energy_wh_nominal_per_pack'], 24.42)
        self.assertLess(result['energy_wh_usable_assumed'], 24.42)
        durations = [s['autonomy_minutes'] for s in result['autonomy_scenarios']]
        self.assertGreater(durations[0], durations[1])
        self.assertGreater(durations[1], durations[2])
        self.assertAlmostEqual(durations[0] / durations[2], 2.5)

    def test_rough_ground_and_low_voltage_reduce_speed(self):
        smooth = calculate(self.h)
        h = copy.deepcopy(self.h)
        h['rolling_coefficient'] *= 4
        rough = calculate(h)
        self.assertLess(rough['speed_predictions'][1]['speed_km_h'],
                        smooth['speed_predictions'][1]['speed_km_h'])
        speed = [v['speed_km_h'] for v in smooth['speed_predictions']]
        self.assertGreater(speed[0], speed[1])
        self.assertGreater(speed[1], speed[2])

    def test_cg_outside_supports_rejects_design(self):
        h = copy.deepcopy(self.h)
        for mass in h['mass_items']:
            mass['x_m'] = .2
        with self.assertRaisesRegex(ValueError, 'triangle'):
            calculate(h)

    def test_predictions_do_not_claim_hardware_or_speed_in_initial_profile(self):
        result = calculate(self.h)
        self.assertFalse(result['hardware_verified'])
        self.assertLess(result['initial_profile_max_duty'], result['target_profile_max_duty_after_tests'])
        self.assertGreater(result['unlimited_stall_source_current_a_estimate'], 11)
        self.assertLess(result['ideal_lateral_acceleration_grid_max_m_s2'], 1.5)


if __name__ == '__main__':
    unittest.main()
