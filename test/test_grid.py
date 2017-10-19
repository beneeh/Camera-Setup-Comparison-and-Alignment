import unittest
import numpy as np

from app.components.grid import Grid, FieldGrid


class TestBaseGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(1, 6, 1, 7, 6, 7)

    def test_len_x_coordinates(self):
        self.assertEqual(len(self.grid.coordinates_x), 6)

    def test_len_y_coordinates(self):
        self.assertEqual(len(self.grid.coordinates_y), 7)

    def test_values_x_coordinates(self):
        array = np.array([1, 2, 3, 4, 5, 6])
        np.testing.assert_equal(array, self.grid.coordinates_x)

    def test_values_y_coordinates(self):
        array = np.array([1, 2, 3, 4, 5, 6, 7])
        np.testing.assert_equal(array, self.grid.coordinates_y)


class TestCameraAndFieldGrid(unittest.TestCase):
    def setUp(self):
        self.grid = FieldGrid(1, 6, 1, 7, 6, 7)

    def test_matrix_x_dimensions(self):
        self.assertEqual(self.grid.count_seen.shape[0], 6)

    def test_matrix_y_dimensions(self):
        self.assertEqual(self.grid.count_seen.shape[1], 7)
