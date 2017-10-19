import numpy as np
import json
import math
from functools import total_ordering

from app.components.camera import Camera
from app.components.grid import FieldGrid, CameraGrid
from app.utils.camera_angle_solution import CameraAngleSolution


def test_camera_format(camera):
    message = "The key '%s' must be in the dictionary describing a camera"
    assert "x" in camera, message % "x"
    assert "y" in camera, message % "x"
    assert "alignment_angle" in camera, message % "alignment_angle"


@total_ordering
class Solution(object):
    def __init__(self, cameras, max_distance, angle_of_view,
                 field_len_x, field_len_y, field_origin_x, field_origin_y,
                 points_on_grid=10000):
        """

        :param list cameras:         A list of cameras. Each camera is defined by a dict with entries
                                     "x", "y" and "alignment_angle"
        :param float max_distance:   The maximum distance an object can be apart from the camera
        :param float angle_of_view:  The maximum angle of view of a camera
        :param float field_len_x:    The length in x direction of the observing field
        :param float field_len_y:    The length in y direction of the observing field
        :param float field_origin_x: The smallest x coordinate of the observing field
        :param float field_origin_y: The smallest y coordinate of the observing field
        :param int points_on_grid:   Number of points on the grid
        """
        # initialize cameras
        self.angle_of_view = angle_of_view
        self.max_distance = max_distance
        self.cameras = []
        for camera in cameras:
            test_camera_format(camera)
            self.cameras.append(Camera(angle_of_view, max_distance, float(camera["x"]), float(camera["y"]),
                                       float(camera["alignment_angle"])))
        # initialize grid
        m = math.sqrt(points_on_grid/((field_len_x+1) * (field_len_y+1)))
        self._grid_start_x = field_origin_x
        self._grid_end_x = field_origin_x + field_len_x
        self._grid_start_y = field_origin_y
        self._grid_end_y = field_origin_y + field_len_y
        self._grid_count_x = math.ceil((field_len_x + 1) * m)
        self._grid_count_y = math.ceil((field_len_y + 1) * m)
        self.grid = FieldGrid(self._grid_start_x, self._grid_end_x, self._grid_start_y, self._grid_end_y,
                              self._grid_count_x, self._grid_count_y)
        self.camera_solutions = {}

    def run(self):
        self._calculate_camera_angle_solutions()
        self._calculate_solution()

    def _calculate_camera_angle_solutions(self):
        for camera in self.cameras:
            grid = CameraGrid(self._grid_start_x, self._grid_end_x, self._grid_start_y, self._grid_end_y,
                              self._grid_count_x, self._grid_count_y)
            cam_solution = CameraAngleSolution(camera, grid)
            cam_solution.calculate()
            self.camera_solutions[id(camera)] = cam_solution

    def _calculate_solution(self):
        for key, camera_solution in self.camera_solutions.items():
            self.grid.count_seen = np.add(self.grid.count_seen, camera_solution.grid.seen,
                                          out=self.grid.count_seen)

    def points_seen_by_x_cameras(self, x):
        return np.count_nonzero((self.grid.count_seen - x) == 0)

    def percentage_seen_by_x_cameras(self, x):
        return self.points_seen_by_x_cameras(x) / (self.grid.count_seen.shape[0] *
                                                   self.grid.count_seen.shape[1])

    def max_seen(self):
        return int(np.max(self.grid.count_seen))

    # rich comparisons
    def __lt__(self, other):
        self._same_type(other)

        # check if overall coverage is smaller
        if self.points_seen_by_x_cameras(0) > other.points_seen_by_x_cameras(0):
            return True
        # check if point with highest camera coverage is smaller
        if self.max_seen() < other.max_seen():
            return True
        elif self.max_seen() > other.max_seen():
            return False
        # check if number of points seen by x is smaller. starting with the max value
        for i in reversed(range(self.max_seen())):
            if self.points_seen_by_x_cameras(i+1) < other.points_seen_by_x_cameras(i+1):
                return True
        return False

    def __le__(self, other):
        self._same_type(other)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other):
        self._same_type(other)
        if self.max_seen() != other.max_seen():
            return False
        max_seen = self.max_seen()
        for i in range(max_seen + 1):
            if self.points_seen_by_x_cameras(i) != other.points_seen_by_x_cameras(i):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        self._same_type(other)

        # check if overall coverage is bigger
        if self.points_seen_by_x_cameras(0) < other.points_seen_by_x_cameras(0):
            return True
        # check if amount of points with highest camera coverage is larger
        if self.max_seen() > other.max_seen():
            return True
        elif self.max_seen() < other.max_seen():
            return False
        # check if number of points seen by x is smaller. starting with the max value
        for i in reversed(range(self.max_seen())):
            if self.points_seen_by_x_cameras(i + 1) > other.points_seen_by_x_cameras(i + 1):
                return True
        return False

    def __ge__(self, other):
        self._same_type(other)
        return self.__gt__(other) or self.__eq__(other)

    def _same_type(self, other):
        if type(self) is not type(other):
            raise NotImplemented


class ExportSolution(object):
    def __init__(self, solution):
        """

        :param Solution solution:
        """
        self.solution = solution
        self.max = solution.max_seen()
        self.seen_by_x = {}
        self.percentage_seen_by_x = {}
        for i in range(self.max + 1):
            self.seen_by_x[i] = solution.points_seen_by_x_cameras(i)
            self.percentage_seen_by_x[i] = solution.percentage_seen_by_x_cameras(i)

    def create_solution_dict(self):
        cameras = []
        for camera in self.solution.cameras:
            cameras.append({'x':               camera.x,
                            'y':               camera.y,
                            'angle_of_view':   camera.angle_of_view,
                            'alignment':       camera.alignment_angle,
                            'percentage_seen': round(self.solution.camera_solutions[id(camera)].percentage_seen(), 4)
                            })
        sol_dict = {'cameras':  cameras,
                    'max_seen': self.solution.max_seen()}

        key = "seen_by_%s"
        for i in range(self.solution.max_seen() + 1):
            sol_dict[key % i] = self.solution.percentage_seen_by_x_cameras(i)
        return sol_dict

    def write_to_file(self, name):
        sol = self.create_solution_dict()
        with open(name, 'w+') as outfile:
            outfile.write(json.dumps(sol, indent=4, sort_keys=True))
