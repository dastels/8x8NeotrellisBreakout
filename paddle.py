from math import pi
from vector import Vector
from coordinate import Coordinate

class Paddle(object):

    moving_left = Vector(0.0, 4)
    moving_right = Vector(pi, 4)
    stopped = Vector(0.0, 0.0)

    def __init__(self, scale, width=0):
        self._scale = scale
        if width == 0:
            width = scale * 2
        self._width = width
        self._position = Coordinate(40 - (width / 2), 8)
        self._velocity = Paddle.stopped

    @property
    def position(self):
        return self._position #Coordinate(self._position.x, self._position.y)

    @property
    def width(self):
        return self._width

    def _move_by(self, v):
        self._velocity = v
        self._position.move_by(v)
        self._position.clip_x(self._scale, 9 * self._scale - self._width)
        self._position.clip_y(0, 0)

    def move_left(self):
        self._move_by(Paddle.moving_left)

    def move_right(self):
        self._move_by(Paddle.moving_right)

    def stop(self):
        self._velocity = Paddle.stopped

    def add_velocity_to(self, v):
        v += self._velocity
        v.clip_magnitude_at(2.0)
        v.clip_angle_between(0.5, 2.6)
