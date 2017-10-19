import math


class Camera(object):
    """
    This class represents a camera object

    the triangle is described by the points A, B and C, the sides a, b and c.
    a and b have the same size. h is the height running from c to C
    the angle of view is gamma(located at C between a and b)
    """

    def __init__(self, angle_of_view, max_distance, x, y, alignment_angle):
        """
        :param float angle_of_view:   gamma in degrees
        :param float max_distance:    the length of sides a and b
        :param float x:               the x coordinate of point C
        :param float y:               the y coordinate of point C
        :param float alignment_angle: alignment of the camera in degrees. the angle is between the height h
                                      and the parallel to the x axis running through the point C
        """
        self.angle_of_view = angle_of_view
        self.max_distance = max_distance
        self.x = x
        self.y = y
        self.alignment_angle = alignment_angle

    def len_h(self):
        return self.max_distance * math.cos(math.radians(self.angle_of_view / 2))

    def point_a(self):
        x = self.x + self.max_distance * math.cos(math.radians(- self.angle_of_view / 2 + self.alignment_angle))
        y = self.y + self.max_distance * math.sin(math.radians(- self.angle_of_view / 2 + self.alignment_angle))
        return x, y

    def point_b(self):
        x = self.x + self.max_distance * math.cos(math.radians(self.angle_of_view / 2 + self.alignment_angle))
        y = self.y + self.max_distance * math.sin(math.radians(self.angle_of_view / 2 + self.alignment_angle))
        return x, y


if __name__ == "__main__":
    for i in range(360):
        c = Camera(71, 18.75, 0, 10, i)
        print(c.len_h())
