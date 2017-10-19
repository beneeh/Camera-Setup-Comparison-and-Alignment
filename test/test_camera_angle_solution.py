import unittest
import numpy as np
import math

from app.utils.camera_angle_solution import CameraAngleSolution
from app.components.grid import CameraGrid
from app.components.camera import Camera


class TestCameraAngleSolution(unittest.TestCase):
    def setUp(self):
        grid = CameraGrid(1, 6, 1, 7, 6, 7)
        camera = Camera(90, 7, 0, 0, 45)
        self.solution = CameraAngleSolution(camera, grid)
        self.solution.calculate()

    def test_points_seen_are_true(self):
        self.assertTrue(self.solution.grid.seen[0][0])
        self.assertTrue(self.solution.grid.seen[0][2])
        self.assertTrue(self.solution.grid.seen[0][5])
        self.assertTrue(self.solution.grid.seen[5][0])
        self.assertTrue(self.solution.grid.seen[2][0])
        self.assertTrue(self.solution.grid.seen[2][3])
        self.assertTrue(self.solution.grid.seen[3][2])
        self.assertTrue(self.solution.grid.seen[2][1])
        self.assertTrue(self.solution.grid.seen[1][2])

    def test_points_are_false(self):
        self.assertFalse(self.solution.grid.seen[2][6])
        self.assertFalse(self.solution.grid.seen[5][4])
        self.assertFalse(self.solution.grid.seen[2][4])
        self.assertFalse(self.solution.grid.seen[5][2])

    def test_seen_by(self):
        self.assertEqual(21, self.solution.count_true())


class TestCameraAngleSolution2(unittest.TestCase):
    def setUp(self):
        grid = CameraGrid(1, 6, 1, 7, 6, 7)
        camera = Camera(math.degrees(2 * math.asin(3/5)), 5, 0, 4, 0)
        self.solution = CameraAngleSolution(camera, grid)
        self.solution.calculate()

    def test_points_seen_are_true(self):
        self.assertTrue(self.solution.grid.seen[0][3])
        self.assertTrue(self.solution.grid.seen[1][2])
        self.assertTrue(self.solution.grid.seen[1][3])
        self.assertTrue(self.solution.grid.seen[1][4])
        self.assertTrue(self.solution.grid.seen[2][1])
        self.assertTrue(self.solution.grid.seen[2][2])
        self.assertTrue(self.solution.grid.seen[2][3])
        self.assertTrue(self.solution.grid.seen[2][4])
        self.assertTrue(self.solution.grid.seen[2][5])
        self.assertTrue(self.solution.grid.seen[3][0])
        self.assertTrue(self.solution.grid.seen[3][1])
        self.assertTrue(self.solution.grid.seen[3][2])
        self.assertTrue(self.solution.grid.seen[3][3])
        self.assertTrue(self.solution.grid.seen[3][4])
        self.assertTrue(self.solution.grid.seen[3][5])
        self.assertTrue(self.solution.grid.seen[3][6])

    def test_seen_by(self):
        self.assertEqual(16, self.solution.count_true())


class TestStatistics(unittest.TestCase):
    def setUp(self):
        grid = CameraGrid(1, 5, 1, 5, 5, 5)
        camera = Camera(90, 4, 0, 0, 45)
        self.solution = CameraAngleSolution(camera, grid)
        self.solution.calculate()

    def test_seen_by(self):
        self.assertEqual(6, self.solution.count_true())

    def test_percentage_seen(self):
        self.assertEqual(6/25, self.solution.percentage_seen())


class TestCameraAngleSolution3(unittest.TestCase):
    def setUp(self):
        self.grid = CameraGrid(1, 5, 1, 5, 5, 5)

    def test1(self):
        camera = Camera(90, 4, 0, 0, 45)
        solution = CameraAngleSolution(camera, self.grid)
        solution.calculate()
        array = np.array([[1, 1, 1, 0, 0],
                          [1, 1, 0, 0, 0],
                          [1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]], dtype=bool)
        np.testing.assert_equal(array, solution.grid.seen)

    def test2(self):
        camera = Camera(90, 4, 6, 0, 135)
        solution = CameraAngleSolution(camera, self.grid)
        solution.calculate()
        array = np.array([[0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [1, 0, 0, 0, 0],
                          [1, 1, 0, 0, 0],
                          [1, 1, 1, 0, 0]], dtype=bool)
        np.testing.assert_equal(array, solution.grid.seen)

    def test3(self):
        camera = Camera(90, 4, 6, 6, 225)
        solution = CameraAngleSolution(camera, self.grid)
        solution.calculate()
        array = np.array([[0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1],
                          [0, 0, 0, 1, 1],
                          [0, 0, 1, 1, 1]], dtype=bool)
        np.testing.assert_equal(array, solution.grid.seen)

    def test4(self):
        camera = Camera(90, 4, 0, 6, 315)
        solution = CameraAngleSolution(camera, self.grid)
        solution.calculate()
        array = np.array([[0, 0, 1, 1, 1],
                          [0, 0, 0, 1, 1],
                          [0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]], dtype=bool)
        np.testing.assert_equal(array, solution.grid.seen)

    def test5(self):
        camera = Camera(90, 4, 0, 0, 71)
        solution = CameraAngleSolution(camera, self.grid)
        solution.calculate()
        array = np.array([[1, 1, 0, 0, 0],
                          [1, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]], dtype=bool)
        np.testing.assert_equal(array, solution.grid.seen)


class TestCameraAngleSolution4(unittest.TestCase):
    def setUp(self):
        self.grid = CameraGrid(2, 18, 2, 18, 5, 5)

    def test1(self):
        camera = Camera(71, 18.75, 10, 0, 90)
        solution = CameraAngleSolution(camera, self.grid)
        solution.calculate()
        array = np.array([[0, 0, 0, 1, 0],
                          [0, 1, 1, 1, 0],
                          [1, 1, 1, 1, 0],
                          [0, 1, 1, 1, 0],
                          [0, 0, 0, 1, 0]], dtype=bool)
        np.testing.assert_equal(array, solution.grid.seen)


