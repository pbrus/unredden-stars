"""
Test package of the unred.unred module
"""
import unittest
from unred.unred import *


class UnredTest(unittest.TestCase):

    def setUp(self):
        data_dir = "example_data/"
        self.sequence = read_unreddened_sequence(data_dir + "ub_bv_dwarfs.dat")
        self.stars = read_reddened_stars(data_dir + "stars.dat")
        self.reddening_line_slope = 0.72
        self.nodes = (
            [176], [177],
            [102, 117, 175],
            [176], [176],
            [100, 119, 175],
            [176], [177],
            [105, 114, 175]
        )

    def test_read_unreddened_sequence(self):
        indexes = 25, 46, 71
        values = (1.4, 1.2187), (1.19, 1.1216), (0.94, 0.6881)

        self.assertLoopingValues(self.sequence, indexes, values)

    def test_read_reddened_stars(self):
        indexes = 1, 3, 5
        values = (
            (2, 0.985, 0.332, 0.017, 0.033),
            (4, 0.141, 0.034, 0.012, 0.020),
            (6, 0.285, 0.062, 0.010, 0.011),
        )

        self.assertLoopingValues(self.stars, indexes, values)

    def assertLoopingValues(self, data, indexes, values):

        for index, value in zip(indexes, values):
            for i, val in enumerate(value):
                self.assertEqual(data[index][i], val)

    def test_unreddened_sequence_nodes(self):
        star = self.get_star_position(self.stars[1])

        for node in self.nodes:
            node_number = unreddened_sequence_nodes(
                next(star), self.sequence, self.reddening_line_slope)
            self.assertEqual(list(node_number), node)

    def get_star_position(self, position):
        x, y = position[1], position[2]
        dx, dy = position[3], position[4]

        for x_position in (x, x - dx, x + dx):
            for y_position in (y, y - dy, y + dy):
                yield x_position, y_position

    def test_slope_line(self):
        first_point = (3.95, -1.39)
        second_point = (5.11, 2.01)
        slope = slope_line(first_point, second_point)
        self.assertAlmostEqual(slope, 2.9310344827586197)

    def test_y_intercept_line(self):
        y_intercept = y_intercept_line(1.23, (3.94, -0.42))
        self.assertAlmostEqual(y_intercept, -5.2661999999999995)

    def test_interpolation_line_coefficients(self):
        indexes = 0, 1, 2
        values = (
            (1.1999999999999986, -0.6451999999999991),
            (0.1999999999999998, -0.09639999999999989),
            (4.480000000000003, 0.05310000000000037),
        )

        data = [interpolation_line_coefficients(self.sequence, i)
            for i in self.nodes]
        self.assertLoopingValues(data[2], indexes, values)

    def test_line(self):
        self.assertAlmostEqual(line((-0.43, 8.12), 21.4), -1.0820000000000007)

    def test_find_intersection(self):
        intersection = find_intersection((2.61, -4.32), (-7.10, 2.61))
        self.assertAlmostEqual(float(intersection), 0.71369722)


if __name__ == "__main__":
    unittest.main()
