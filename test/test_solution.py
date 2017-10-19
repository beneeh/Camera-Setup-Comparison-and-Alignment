import unittest
import copy

import numpy as np

from app.solution import Solution


class TestSolution1(unittest.TestCase):
    def setUp(self):
        cameras = [{'x': 0, 'y': 0, 'alignment_angle': 45},
                   {'x': 6, 'y': 0, 'alignment_angle': 135},
                   {'x': 6, 'y': 6, 'alignment_angle': 225},
                   {'x': 0, 'y': 6, 'alignment_angle': 315}]
        angle_of_view = 90
        max_distance = 4
        field_origin_x = 1
        field_origin_y = 1
        field_len_x = 4
        field_len_y = 4
        grid_count = 25
        self.solution = Solution(cameras, max_distance, angle_of_view, field_len_x, field_len_y,
                                 field_origin_x, field_origin_y, grid_count)
        self.solution._calculate_camera_angle_solutions()
        self.solution._calculate_solution()

    def test(self):
        a = np.array([[1, 1, 2, 1, 1],
                      [1, 1, 0, 1, 1],
                      [2, 0, 0, 0, 2],
                      [1, 1, 0, 1, 1],
                      [1, 1, 2, 1, 1]])
        np.testing.assert_equal(a, self.solution.grid.count_seen)

    def test_seen_by(self):
        self.assertEqual(5, self.solution.points_seen_by_x_cameras(0))
        self.assertEqual(16, self.solution.points_seen_by_x_cameras(1))
        self.assertEqual(4, self.solution.points_seen_by_x_cameras(2))
        self.assertEqual(0, self.solution.points_seen_by_x_cameras(3))

    def test_percentage_seen_by(self):
        self.assertEqual(0.2, self.solution.percentage_seen_by_x_cameras(0))
        self.assertEqual(16/25, self.solution.percentage_seen_by_x_cameras(1))
        self.assertEqual(4/25, self.solution.percentage_seen_by_x_cameras(2))
        self.assertEqual(0, self.solution.percentage_seen_by_x_cameras(3))


class TestRichComparisons(unittest.TestCase):
    def setUp(self):
        self.solution1 = Solution([], 3, 2, 2, 2, 2, 2)
        self.solution2 = copy.deepcopy(self.solution1)

    def test_equal_True(self):
        self.solution1.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertTrue(self.solution1 == self.solution2)

    def test_equal_False(self):
        self.solution1.grid.count_seen = np.array([[0, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertFalse(self.solution1 == self.solution2)

    def test_not_equal_False(self):
        self.solution1.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertFalse(self.solution1 != self.solution2)

    def test_not_equal_True(self):
        self.solution1.grid.count_seen = np.array([[0, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertTrue(self.solution1 != self.solution2)

    def test_less_than_true_more_zeros(self):
        self.solution1.grid.count_seen = np.array([[0, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertTrue(self.solution1 < self.solution2)

    def test_less_than_false_less_zeros(self):
        self.solution1.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[0, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertFalse(self.solution1 < self.solution2)

    def test_less_than_true_smaller_max(self):
        self.solution1.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[1, 3, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertTrue(self.solution1 < self.solution2)

    def test_less_than_false_bigger_max(self):
        self.solution1.grid.count_seen = np.array([[1, 3, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertFalse(self.solution1 < self.solution2)

    def test_less_than_false_equal(self):
        self.solution1.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertFalse(self.solution1 < self.solution2)

    def test_less_than_True_more_max(self):
        self.solution1.grid.count_seen = np.array([[1, 2, 1],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.solution2.grid.count_seen = np.array([[1, 2, 2],
                                                   [1, 0, 1],
                                                   [1, 2, 1]])
        self.assertTrue(self.solution1 < self.solution2)


class TestSolution2(unittest.TestCase):
    def setUp(self):
        cameras = [{'x': 10, 'y': 0, 'alignment_angle': 90},
                   {'x': 20, 'y': 10, 'alignment_angle': 180},
                   {'x': 10, 'y': 20, 'alignment_angle': 270},
                   {'x': 0, 'y': 10, 'alignment_angle': 360}]
        angle_of_view = 71
        max_distance = 18.75
        field_origin_x = 2
        field_origin_y = 2
        field_len_x = 16
        field_len_y = 16
        grid_count = 25
        self.solution = Solution(cameras, max_distance, angle_of_view, field_len_x, field_len_y,
                                 field_origin_x, field_origin_y, grid_count)
        self.solution._calculate_camera_angle_solutions()
        self.solution._calculate_solution()

    def test_grid(self):
        a = np.array([[0, 1, 1, 1, 0],
                      [1, 4, 4, 4, 1],
                      [1, 4, 4, 4, 1],
                      [1, 4, 4, 4, 1],
                      [0, 1, 1, 1, 0]])
        np.testing.assert_equal(a, self.solution.grid.count_seen)
