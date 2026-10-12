"""Vérification des calculs avec cas analytiques, sans masses de robot inventées."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pre_dimensionnement import autonomy, stability


class DimensionTests(unittest.TestCase):
    def test_center_and_known_margin(self):
        result = stability([[0, 0], [100, 0], [0, 100]],
                           [{"mass_g": 100, "center_mm": [20, 20, 40]}])
        self.assertEqual(result["center_of_mass_mm"], [20, 20, 40])
        self.assertAlmostEqual(result["minimum_static_margin_mm"], 20)
        self.assertAlmostEqual(result["ideal_tipping_acceleration_m_s2"], 4.905)
        self.assertTrue(result["strictly_inside_triangle"])

    def test_clockwise_triangle_and_weighted_masses(self):
        result = stability([[0, 100], [100, 0], [0, 0]],
                           [{"mass_g": 100, "center_mm": [10, 10, 20]},
                            {"mass_g": 300, "center_mm": [30, 30, 60]}])
        self.assertEqual(result["center_of_mass_mm"], [25, 25, 50])
        self.assertEqual(result["total_mass_g"], 400)
        self.assertEqual(result["minimum_static_margin_mm"], 25)

    def test_unstable_and_on_edge(self):
        for x in (0, -10):
            result = stability([[0, 0], [100, 0], [0, 100]],
                               [{"mass_g": 100, "center_mm": [x, 20, 40]}])
            self.assertFalse(result["strictly_inside_triangle"])
            self.assertIsNone(result["ideal_tipping_acceleration_m_s2"])

    def test_invalid_supports_and_masses(self):
        for supports in ([[0, 0], [1, 1], [2, 2]], [[0, 0], [1, 1]],
                         [[0, 0], [1, 1], [float("nan"), 0]]):
            with self.assertRaises(ValueError):
                stability(supports, [{"mass_g": 1, "center_mm": [0, 0, 1]}])
        with self.assertRaises(ValueError):
            stability([[0, 0], [100, 0], [0, 100]],
                      [{"mass_g": -1, "center_mm": [20, 20, 40]}])

    def test_runtime_from_energy_and_average_power(self):
        result = autonomy(10, 0.8, 4)
        self.assertEqual(result["usable_energy_wh"], 8)
        self.assertEqual(result["estimated_runtime_min"], 120)

    def test_invalid_energy(self):
        for arguments in ((0, 0.8, 4), (10, 1.1, 4), (10, 0.8, 0),
                          (10, float("nan"), 4), (10, 0.8, True)):
            with self.assertRaises(ValueError):
                autonomy(*arguments)


if __name__ == "__main__":
    unittest.main()
