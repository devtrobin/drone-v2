"""Cas analytiques indépendants pour les formules de déplacement."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from performance_drone import differential, speed, traction


class PerformanceTests(unittest.TestCase):
    def test_effort_and_adhesion_limit(self):
        result = traction(1, .05, .1, 6, .1, .2, acceleration=.2)
        self.assertAlmostEqual(result['required_force_n'], 1.181)
        self.assertAlmostEqual(result['motor_work_force_n'], 1)
        self.assertAlmostEqual(result['adhesion_limit_n'], 1.2)
        self.assertFalse(result['can_move_under_assumptions'])

    def test_speed_at_half_stall_and_pwm(self):
        # Deux moteurs : chacun 0,05 Nm pour 2 N et roues de rayon 0,05 m.
        self.assertAlmostEqual(speed(200, .1, .05, 2)['wheel_rpm'], 100)
        self.assertAlmostEqual(speed(200, .1, .05, 2, .5)['wheel_rpm'], 0)
        self.assertAlmostEqual(speed(200, .1, .05, 0, .5)['wheel_rpm'], 100)

    def test_straight_pivot_and_one_wheel(self):
        self.assertIsNone(differential(.2, .2, .16)['radius_m'])
        pivot = differential(-.2, .2, .16)
        self.assertEqual(pivot['radius_m'], 0)
        self.assertAlmostEqual(pivot['yaw_rate_rad_s'], 2.5)
        self.assertAlmostEqual(differential(0, .2, .16)['radius_m'], .08)

    def test_invalid_physical_values(self):
        with self.assertRaises(ValueError):
            speed(200, .1, .05, 0, 1.1)
        with self.assertRaises(ValueError):
            traction(1, .05, .1, 20, .1, .2)
        with self.assertRaises(ValueError):
            differential(0, 1, 0)


if __name__ == '__main__':
    unittest.main()
