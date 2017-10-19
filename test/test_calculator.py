import math
import unittest

from app.components.camera import Camera
from app.utils.calculator import Calculator


class TestCalculatorAngleAroundPoint(unittest.TestCase):
    def test_x_positive_y_positive(self):
        self.assertEqual(Calculator.calculate_angle(2, 2, 0, 0), 45)
        self.assertEqual(Calculator.calculate_angle(4, 4, 2, 2), 45)
        self.assertEqual(Calculator.calculate_angle(0, 0, -2, -2), 45)
        self.assertEqual(round(Calculator.calculate_angle(1, math.sqrt(3), 0, 0)), 60)

    def test_x_positive_y_negative(self):
        self.assertEqual(Calculator.calculate_angle(2, -2, 0, 0), 315)
        self.assertEqual(Calculator.calculate_angle(4, 0, 2, 2), 315)
        self.assertEqual(Calculator.calculate_angle(0, -4, -2, -2), 315)
        self.assertEqual(round(Calculator.calculate_angle(1, -math.sqrt(3), 0, 0)), 300)

    def test_x_positive_y_zero(self):
        self.assertEqual(Calculator.calculate_angle(2, 0, 0, 0), 0)
        self.assertEqual(Calculator.calculate_angle(4, 2, 2, 2), 0)
        self.assertEqual(Calculator.calculate_angle(0, -2, -2, -2), 0)

    def test_x_negative_y_positive(self):
        self.assertEqual(Calculator.calculate_angle(-2, 2, 0, 0), 135)
        self.assertEqual(Calculator.calculate_angle(0, 4, 2, 2), 135)
        self.assertEqual(Calculator.calculate_angle(-4, 0, -2, -2), 135)
        self.assertEqual(round(Calculator.calculate_angle(-1, math.sqrt(3), 0, 0)), 120)

    def test_x_negative_y_negative(self):
        self.assertEqual(Calculator.calculate_angle(-2, -2, 0, 0), 225)
        self.assertEqual(Calculator.calculate_angle(0, 0, 2, 2), 225)
        self.assertEqual(Calculator.calculate_angle(-4, -4, -2, -2), 225)
        self.assertEqual(round(Calculator.calculate_angle(-1, -math.sqrt(3), 0, 0)), 240)

    def test_x_negative_y_zero(self):
        self.assertEqual(Calculator.calculate_angle(-2, 0, 0, 0), 180)
        self.assertEqual(Calculator.calculate_angle(0, 2, 2, 2), 180)
        self.assertEqual(Calculator.calculate_angle(-4, -2, -2, -2), 180)

    def test_x_zero_y_positive(self):
        self.assertEqual(Calculator.calculate_angle(0, 2, 0, 0), 90)
        self.assertEqual(Calculator.calculate_angle(2, 4, 2, 2), 90)
        self.assertEqual(Calculator.calculate_angle(-2, 0, -2, -2), 90)

    def test_x_zero_y_negative(self):
        self.assertEqual(Calculator.calculate_angle(0, -2, 0, 0), 270)
        self.assertEqual(Calculator.calculate_angle(2, 0, 2, 2), 270)
        self.assertEqual(Calculator.calculate_angle(-2, -4, -2, -2), 270)

    def test_x_zero_y_zero(self):
        self.assertRaises(ValueError, Calculator.calculate_angle, 0, 0, 0, 0)
        self.assertRaises(ValueError, Calculator.calculate_angle, 2, 2, 2, 2)


class TestCalculatorDistance(unittest.TestCase):
    def test(self):
        self.assertEqual(Calculator.distance_between_points(0, 0, 2, 0), 2)
        self.assertEqual(Calculator.distance_between_points(2, 0, 0, 0), 2)

        self.assertEqual(Calculator.distance_between_points(0, 0, 1, 1), math.sqrt(2))
        self.assertEqual(Calculator.distance_between_points(1, 1, 0, 0), math.sqrt(2))

        self.assertEqual(Calculator.distance_between_points(100, 100, 102, 100), 2)
        self.assertEqual(Calculator.distance_between_points(102, 100, 100, 100), 2)

        self.assertEqual(Calculator.distance_between_points(100, 100, 101, 101), math.sqrt(2))
        self.assertEqual(Calculator.distance_between_points(101, 101, 100, 100), math.sqrt(2))


class TestCalculatorInCameraTriangleAngle90Alignment45(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(90, 4, 10, 10, 45)

    def test_in(self):
        self.assertTrue(Calculator.point_in_camera_view_triangle(11, 12, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(11, 11, self.camera))

    def test_on(self):
        self.assertTrue(Calculator.point_in_camera_view_triangle(12, 12, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(13, 10, self.camera))

    def test_out(self):
        self.assertFalse(Calculator.point_in_camera_view_triangle(12.1, 12.1, self.camera))
        self.assertFalse(Calculator.point_in_camera_view_triangle(13, 9.9, self.camera))
        self.assertFalse(Calculator.point_in_camera_view_triangle(9, 9, self.camera))
        self.assertFalse(Calculator.point_in_camera_view_triangle(9, 12, self.camera))
        self.assertFalse(Calculator.point_in_camera_view_triangle(12, 9, self.camera))


class TestCalculatorInCameraTriangleAngle90Alignment135(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(90, 4, 6, 0, 135)

    def test_in(self):
        self.assertTrue(Calculator.point_in_camera_view_triangle(4, 1, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(5, 2, self.camera))

    def test_on(self):
        self.assertTrue(Calculator.point_in_camera_view_triangle(3, 1, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(2, 0, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(6, 4, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(4, 2, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(4, 0, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(6, 2, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(5, 3, self.camera))

    def test_out(self):
        self.assertFalse(Calculator.point_in_camera_view_triangle(0, 0, self.camera))
        self.assertFalse(Calculator.point_in_camera_view_triangle(3.9, 2, self.camera))
        self.assertFalse(Calculator.point_in_camera_view_triangle(6.1, 2, self.camera))
        self.assertFalse(Calculator.point_in_camera_view_triangle(4, -0.1, self.camera))


class TestCalculatorInCameraTriangleAngle71Alignment90(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(71, 18.75, 10, 0, 90)

    def test_in(self):
        self.assertTrue(Calculator.point_in_camera_view_triangle(10, 2, self.camera))
        self.assertTrue(Calculator.point_in_camera_view_triangle(6, 14, self.camera))


class TestCalculatorLengthOfLine(unittest.TestCase):
    def test(self):
        self.assertEqual(Calculator.length_of_line_in_triangle(math.sqrt(2), 90, 45), math.sqrt(2))
        ans = Calculator.length_of_line_in_triangle(math.sqrt(8), 90, 71.57)
        self.assertEqual(round(ans, 2), round(math.sqrt(10), 2))


class TestAnfleInOrOnAngle(unittest.TestCase):
    def test_in_basic(self):
        self.assertTrue(Calculator.angle_is_between_or_on_angles(1, 0, 2))
        self.assertTrue(Calculator.angle_is_between_or_on_angles(45, 20, 91))
        self.assertTrue(Calculator.angle_is_between_or_on_angles(180, 90, 270))

    def test_in_over_zero(self):
        self.assertTrue(Calculator.angle_is_between_or_on_angles(0, 350, 10))
        self.assertTrue(Calculator.angle_is_between_or_on_angles(0, -10, 10))
        self.assertTrue(Calculator.angle_is_between_or_on_angles(-2, 181, 179))
        self.assertTrue(Calculator.angle_is_between_or_on_angles(0, 270, 90))

    def test_in_over_180(self):
        self.assertTrue(Calculator.angle_is_between_or_on_angles(179, 168, 180))
        self.assertTrue(Calculator.angle_is_between_or_on_angles(179, 168, 180))

    def test_on(self):
        self.assertTrue(Calculator.angle_is_between_or_on_angles(0, 0, 0))
        self.assertTrue(Calculator.angle_is_between_or_on_angles(45, 45, 90))
        self.assertTrue(Calculator.angle_is_between_or_on_angles(90, 45, 90))

    def test_out(self):
        self.assertFalse(Calculator.angle_is_between_or_on_angles(180, 270, 90))