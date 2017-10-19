import math
from app.components.camera import Camera


class Calculator(object):
    @staticmethod
    def point_in_camera_view_circle(x, y, camera):
        """
        checks if a point with coordinates x and y can be observed by a camera
        :type x: float
        :type y: float
        :type camera: Camera
        :rtype: bool
        """
        if round(Calculator.distance_between_points(x, y, camera.x, camera.y), 6) \
                <= round(camera.max_distance, 6):
            point_angle = Calculator.calculate_angle(x, y, camera.x, camera.y)
            if point_angle >= camera.alignment_angle - (1 / 2) * camera.angle_of_view:
                if point_angle <= camera.alignment_angle + (1 / 2) * camera.angle_of_view:
                    return True
        return False

    @staticmethod
    def point_in_camera_view_triangle(x, y, camera):
        """
        checks if a point with coordinates x and y can be observed by a camera
        :type x: float
        :type y: float
        :type camera: Camera
        :rtype: bool
        """
        point_angle = Calculator.calculate_angle(x, y, camera.x, camera.y)
        angle = point_angle - (camera.alignment_angle - 0.5 * camera.angle_of_view)
        length = Calculator.length_of_line_in_triangle(camera.len_h(), camera.angle_of_view, angle)
        min_angle = camera.alignment_angle - (1 / 2) * camera.angle_of_view
        max_angle = camera.alignment_angle + (1 / 2) * camera.angle_of_view
        if round(Calculator.distance_between_points(x, y, camera.x, camera.y), 5) <= round(length, 5):
            if Calculator.angle_is_between_or_on_angles(point_angle, min_angle, max_angle):
                return True
        return False

    @staticmethod
    def angle_is_between_or_on_angles(alpha, min_angle, max_angle):
        alpha = alpha % 360
        min_angle = min_angle % 360
        max_angle = max_angle % 360
        if min_angle > 180:
            p = 360 - min_angle
            alpha = (alpha + p) % 360
            min_angle = (min_angle + p) % 360
            max_angle = (max_angle + p) % 360
        return (alpha >= min_angle) and (alpha <= max_angle)

    @staticmethod
    def distance_between_points(x_a, y_a, x_b, y_b):
        """
        returns the distance between points a and b
        :param float x_a:
        :param float y_a:
        :param float x_b:
        :param float y_b:
        :rtype: float
        """
        return math.sqrt((x_a-x_b)**2 + (y_a-y_b)**2)

    @staticmethod
    def length_of_line_in_triangle(height, gamma, angle):
        """
        this method calculates th length of a line in a triangle. This line starts at point C and ends
        at side c of the triangle.
        :param float height: The height of the triangle (from Point C to side c)
        :param float gamma: The angle between sides a and b
        :param float angle: The angle between side a and the line
        """
        return height / math.cos(math.radians(0.5*gamma - angle))

    @staticmethod
    def calculate_angle(x_a, y_a, x_b, y_b):
        """
        Calculates the angle of the connection between point a and b. the angle is between the connection
        of the two points and the parallel to the x axis running through the point b.
        :param x_a: x coordinate of point a
        :param y_a: y coordinate of point a
        :param x_b: x coordinate of point b
        :param y_b: y coordinate of point b
        :return: angle in degrees
        :type x_a: float
        :type y_a: float
        :type x_b: float
        :type y_b: float
        :rtype: float
        """
        x = x_a - x_b
        y = y_a - y_b

        if x > 0:
            if y > 0:
                return math.degrees(math.atan(y / x))
            elif y < 0:
                return 360 + math.degrees(math.atan(y / x))
            else:
                return 0
        elif x < 0:
            if y > 0:
                return 180 + math.degrees(math.atan(y / x))
            elif y < 0:
                return 180 + math.degrees(math.atan(y / x))
            else:
                return 180
        else:
            if y > 0:
                return 90
            elif y < 0:
                return 270
            else:
                raise ValueError("Points A and B can not be the same")
