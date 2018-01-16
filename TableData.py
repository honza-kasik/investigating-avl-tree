import numpy as np


class TableData:

    _threshold = 5
    _no_rotations = 0
    _single_rotations = 1
    _double_rotations = 2

    def __init__(self):
        self._data = np.zeros((20, 3))

    def new_single_rotation_event(self, path_length):
        self._data[path_length - 1][self._single_rotations] += 1

    def new_double_rotation_event(self, path_length):
        self._data[path_length - 1][self._double_rotations] += 1

    def new_no_rotation_event(self, path_length):
        self._data[path_length - 1][self._no_rotations] += 1

    def get_single_rotation_events(self, path_length):
        return self._data[path_length - 1][self._single_rotations]

    def get_double_rotation_events(self, path_length):
        return self._data[path_length - 1][self._double_rotations]

    def get_no_rotation_events(self, path_length):
        return self._data[path_length - 1][self._no_rotations]

    def get_accumulated_no_rotations_above_threshold(self, threshold):
        return sum(map(lambda x: x[self._no_rotations], self._data[threshold:]))

    def get_accumulated_single_rotations_above_threshold(self, threshold):
        return sum(map(lambda x: x[self._single_rotations], self._data[threshold:]))

    def get_accumulated_double_rotations_above_threshold(self, threshold):
        return sum(map(lambda x: x[self._double_rotations], self._data[threshold:]))

