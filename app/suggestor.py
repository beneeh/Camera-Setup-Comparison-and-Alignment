import copy
import logging
import json
import math

from app.components.camera import Camera
from app.utils.camera_angle_solution import CameraAngleSolution
from app.components.grid import CameraGrid
from app.utils.create_matches import CreateMatches
from app.solution import Solution, ExportSolution


log = logging.getLogger(__name__)


class Suggestor(object):
    def __init__(self, camera_positions, max_distance, angle_of_view,
                 field_len_x, field_len_y, field_origin_x, field_origin_y,
                 points_on_grid=1000):
        """

        :param camera_positions:
        :param max_distance:
        :param angle_of_view:
        :param field_len_x:
        :param field_len_y:
        :param field_origin_x:
        :param field_origin_y:
        :param points_on_grid:
        """
        self.max_distance = max_distance
        self.angle_of_view = angle_of_view
        self.field_len_x = field_len_x
        self.field_len_y = field_len_y
        self.field_origin_x = field_origin_x
        self.field_origin_y = field_origin_y

        # initialize grid
        m = math.sqrt(points_on_grid / ((field_len_x + 1) * (field_len_y + 1)))
        self._grid_start_x = field_origin_x
        self._grid_end_x = field_origin_x + field_len_x
        self._grid_start_y = field_origin_y
        self._grid_end_y = field_origin_y + field_len_y
        self._grid_count_x = math.ceil((field_len_x + 1) * m)
        self._grid_count_y = math.ceil((field_len_y + 1) * m)

        # initialize cameras
        self.cameras = []
        for camera_position in camera_positions:
            self.cameras.append(Camera(angle_of_view, max_distance, float(camera_position[0]),
                                       float(camera_position[1]), 0))
        self.camera_solutions = []
        self.best_camera_solutions = []
        self.solutions = []

    def _calculate_cameras(self, steps=360):
        log.info("Starting to calculate camera angles")
        deg_per_step = 360 / steps
        i = 0
        for camera in self.cameras:
            i += 1
            log.info("Calculating camera %i of %i" % (i, len(self.cameras)))
            camera_solution = []
            for step in range(steps):
                grid = CameraGrid(self._grid_start_x, self._grid_end_x, self._grid_start_y,
                                  self._grid_end_y, self._grid_count_x, self._grid_count_y)
                camera.alignment_angle = step * deg_per_step
                solution = CameraAngleSolution(copy.copy(camera), grid)
                solution.calculate()
                if solution.count_true() != 0:
                    if not any((solution == x).all() for x in camera_solution):
                        camera_solution.append(solution)
                camera_solution.sort(key=lambda x: x.count_true())
            self.camera_solutions.append(camera_solution)
        log.info("Finished to calculate camera angles")

    def _get_best_camera_angles(self):
        """
        function to get the 'best' camera angles from the calculated angles. The best solution are those
        with the most points on the grid seen.
        """
        for camera_solution in self.camera_solutions:
            max_seen = camera_solution[-1].count_true()
            best = [{'x': x.camera.x,
                     'y': x.camera.y,
                     'alignment_angle': x.camera.alignment_angle}
                    for x in camera_solution if x.count_true() == max_seen]
            self.best_camera_solutions.append(best)

    def _calculate_solutions(self):
        num_matches = CreateMatches.calculate_number_of_matches(self.best_camera_solutions)
        log.info("Number of matches: %i" % num_matches)
        matches = CreateMatches.create(self.best_camera_solutions)
        i = 0
        for match in matches:
            i += 1
            log.info("Calculating solution %i of %i" % (i, len(matches)))
            solution = Solution(match, self.max_distance, self.angle_of_view, self.field_len_x,
                                self.field_len_y, self.field_origin_x, self.field_origin_y)
            solution.run()
            self.solutions.append(solution)
        self.solutions.sort()

    def run(self):
        self._calculate_cameras()
        self._get_best_camera_angles()
        self._calculate_solutions()


class ExportSuggestor(object):
    @staticmethod
    def create_dict(suggestor):
        data = []
        for solution in suggestor.solutions:
            data.append(ExportSolution(solution).create_solution_dict())
        return data

    @staticmethod
    def create_best_dict(suggestor):
        solutions = [x for x in suggestor.solutions if x == max(suggestor.solutions)]
        data = []
        for solution in solutions:
            data.append(ExportSolution(solution).create_solution_dict())
        return data

    @staticmethod
    def write_all_to_file(suggestor, file_name):
        """
        :param Suggestor suggestor:
        :param str file_name:
        """
        data = ExportSuggestor.create_dict(suggestor)
        with open(file_name, 'w') as outfile:
            outfile.write(json.dumps(data, indent=4, sort_keys=True))

    @staticmethod
    def write_best_to_file(suggestor, file_name):
        """
        :param Suggestor suggestor:
        :param str file_name:
        """
        solutions = [x for x in suggestor.solutions if x == max(suggestor.solutions)]
        data = []
        for solution in solutions:
            data.append(ExportSolution(solution).create_solution_dict())
        with open(file_name, 'w') as outfile:
            outfile.write(json.dumps(data, indent=4, sort_keys=True))
