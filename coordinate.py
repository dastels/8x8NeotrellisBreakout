from vector import Vector
from math import atan2, sqrt

class Coordinate(object):

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return int(self._x)

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return int(self._y)

    @y.setter
    def y(self, new_y):
        self._y = new_y

    def __str__(self):
        return '({0:6.4f}, {1:6.4f})'.format(self.x, self.y)

    def move_by(self, dx_or_vector, dy=None):
        if isinstance(dx_or_vector, Vector):
            self._x += dx_or_vector.x
            self._y += dx_or_vector.y
        else:
            self._x += dx_or_vector
            self._y += dy

    def convert_to_tile_position(self, scale):
        return Coordinate(self._x // scale, self._y // scale)

    def clip_x(self, low, high):
        self._x = min([high, max([low, self._x])])

    def clip_y(self, low, high):
        self._y = min([high, max([low, self._y])])

    def out_of_bounds_x(self, low, high):
        return self._x < low or self._x > high

    def out_of_bounds_y(self, low, high):
        return self._y < low or self._y > high

    def vector_difference(self, other):
        dx = self._x - other.x
        dy = self._y - other.y
        return Vector(atan2(dy, dx), sqrt(dx * dx + dy * dy))
