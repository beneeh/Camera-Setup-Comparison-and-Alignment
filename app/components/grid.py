import numpy as np


class Grid(object):
    def __init__(self, x_start,  x_stop, y_start, y_stop, x_count, y_count):
        """

        :param x_start:
        :param x_stop:
        :param y_start:
        :param y_stop:
        :param x_count:
        :param y_count:
        """
        self.x_start = x_start
        self.x_stop = x_stop
        self.x_count = x_count
        self.y_start = y_start
        self.y_stop = y_stop
        self.y_count = y_count
        self.coordinates_x = np.linspace(x_start, x_stop, x_count)
        self.coordinates_y = np.linspace(y_start, y_stop, y_count)


class CameraGrid(Grid):
    def __init__(self, x_start,  x_stop, y_start, y_stop, x_count, y_count):
        super(CameraGrid, self).__init__(x_start,  x_stop, y_start, y_stop, x_count, y_count)
        self.seen = np.zeros([x_count, y_count], dtype=bool)


class FieldGrid(Grid):
    def __init__(self, x_start,  x_stop, y_start, y_stop, x_count, y_count):
        super(FieldGrid, self).__init__(x_start,  x_stop, y_start, y_stop, x_count, y_count)
        self.count_seen = np.zeros([x_count, y_count])
