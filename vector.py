from math import sin, cos, atan2, sqrt, fabs, pi

class Vector (object):

    def __init__(self, angle, magnitude):
        self._angle = angle
        self._magnitude = magnitude

    def __str__(self):
        return "a: {0:6.4f}, s: {1:4.2f}".format(self._angle, self._magnitude)

    @property
    def x(self):
        return self._magnitude * cos(self._angle)

    @property
    def y(self):
        return self._magnitude * sin(self._angle)

    @property
    def angle(self):
        return self._angle

    @property
    def magnitude(self):
        return self._magnitude

    def flip_x(self):
        offset = 2 * pi if self._angle > pi else 0.0
        return offset + pi - self._angle

    def flip_y(self):
        return (2 * pi) - self._angle

    def angle_as_deg_512(self):
        return int((self._angle * 163)) >> 1

    def __iadd__(self, o):
        cx = self.x + o.x
        cy = self.y + o.y
        self.angle = atan2(cy, cx)
        self.magnitude = sqrt(cx * cx + cy * cy)
        return self

    def __add__(self, o):
        s = Vector(self._angle, self._magnitude)
        s += o
        return s

    def __isub__(self, o):
        cx = self.x - o.x
        cy = self.y - o.y
        self.angle = atan2(cy, cx)
        self.magnitude = sqrt(cx * cx + cy * cy)
        return self

    def __sub__(self, o):
        s = Vector(self._angle, self._magnitude)
        s -= o
        return s

    def __imul__(self, scale):
        self._magnitude *= scale
        return self

    def __idiv__(self, scale):
        self._magnitude /= scale
        return self

    def __mul__(self, scale):
        return Vector(self.angle, self._magnitude * scale)

    def __div__(self, scale):
        return Vector(self.angle, self._magnitude / scale)

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def normalize(self):
        self._magnitude = 1.0

    def clip_magnitude_at(self, high):
        if self._magnitude > high:
            self._magnitude = high

    def clip_magnitude_between(self, low, high):
        if self._magnitude < low:
            self._magnitude = low
        if self._magnitude > high:
            self._magnitude = high

    def clip_angle_between(self, low, high):
        if self._angle < low:
            self._angle = low
        if self._angle > high:
            self._angle = high

    def normalize_angle(self):
        while self._angle > 2 * pi:
            self._angle -= 2 * pi

    @property
    def is_left(self):
        self.normalize_angle()
        return (self._angle > (0.5 * pi)) and (self._angle < (1.5 * pi))

    @property
    def is_right(self):
        self.normalize_angle()
        return (self._angle > (1.5 * pi)) or (self._angle < (0.5 * pi))

    @property
    def is_down(self):
        self.normalize_angle()
        return self._angle < pi

    @property
    def is_up(self):
        self.normalize_angle()
        return self._angle > pi

    @property
    def is_primarily_right(self):
        self.normalize_angle()
        return self._angle <= (0.25 * pi) or self._angle >= (1.75 * pi)

    def is_primarily_up(self):
        self.normalize_angle()
        return self._angle >= (1.25 * pi) and self._angle <= (1.75 * pi)

    def is_primarily_left(self):
        self.normalize_angle()
        return self._angle >= 0.75 * pi and self._angle <= 1.25 * pi

    def is_primarily_down(self):
        self.normalize_angle()
        return self._angle >= 0.25 * pi and self._angle <= 0.75 * pi

    def is_in_the_same_direction_as(self, v):
        difference = fabs(v - self)
        return difference.angle < 0.5 * pi
