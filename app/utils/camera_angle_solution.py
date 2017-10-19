from app.components.camera import Camera
from app.components.grid import CameraGrid
from app.utils.calculator import Calculator


class CameraAngleSolution(object):
    def __init__(self, camera, grid):
        """

        :param Camera camera:
        :param CameraGrid grid:
        """
        self.camera = camera
        self.grid = grid
        self.calculated = False

    def calculate(self):
        # This is very slow code
        # TODO: rewrite
        x_len = len(self.grid.coordinates_x)
        y_len = len(self.grid.coordinates_y)
        for i in range(x_len):
            for j in range(y_len):
                self.grid.seen[i][j] = Calculator.point_in_camera_view_triangle(self.grid.coordinates_x[i],
                                                                                self.grid.coordinates_y[j],
                                                                                self.camera)
        self.calculated = True

    def count_true(self):
        return self.grid.seen.sum()

    def percentage_seen(self):
        return self.count_true() / (self.grid.seen.shape[0] * self.grid.seen.shape[1])

    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self.grid.seen == other.grid.seen

    def __ne__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self.grid.seen == other.grid.seen
