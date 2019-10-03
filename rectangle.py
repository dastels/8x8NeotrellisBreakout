#pylint:disable=unused-argument

from coordinate import Coordinate

class Rectangle(object):

    def __init__(self, top, left, bottom, right):
        self._top = top
        self._left = left
        self._bottom = bottom
        self._right = right

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, new_top):
        self._top = new_top

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, new_left):
        self._top = new_left

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, new_bottom):
        self._bottom = new_bottom

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_right):
        self._right = new_right

    @property
    def bottom_left(self):
        return Coordinate(self._left, self._bottom)

    @property
    def bottom_center(self):
        return Coordinate((self._left + self._right) / 2, self._bottom)

    @property
    def bottom_right(self):
        return Coordinate(self._right, self._bottom)

    @property
    def top_left(self):
        return Coordinate(self._left, self._top)

    @property
    def top_center(self):
        return Coordinate((self._left + self._right) / 2, self._top)

    @property
    def top_right(self):
        return Coordinate(self._right, self._top)

    @property
    def middle_left(self):
        return Coordinate(self._left, (self._top + self._right) / 2)

    @property
    def middle_right(self):
        return Coordinate(self._right, (self._top + self._right) / 2)

    @property
    def center(self):
        return Coordinate((self._left + self._right) / 2, (self._top + self._bottom) / 2)

    def is_empty(self):
        return (self._top > self._bottom) or (self._left > self._right)

    def __or__(self, r):
        return new_rectangle(min([self._top, r.top]), min([self._left, r.left]),  max([self._bottom, r.bottom]), max([self._right, r.right]))

    def __and__(self, r):
        return new_rectangle(max([self._top, r.top]), max([self._left, r.left]),  min([self._bottom, r.bottom]), min([self._right, r.right]))

    def inset(self, margin):
        return new_rectangle(self._top + margin, self._left + margin, self._bottom - margin, self._right - margin)

    def collides_with(self, r):
        if self._top > r.bottom:
            return False
        if self._bottom < r.top:
            return False
        if self._left > r.right:
            return False
        if self._right < r.left:
            return False
        return True


class EmptyRectangle(Rectangle):

    def __init__(self):
        Rectangle.__init__(self, 0, 0, 0, 0)

    def isEmpty(self):
        return True

    def __or__(self, r):
        return other_rect

    def __and__(self, r):
        return self

    def inset(self, i):
        return self

    def collides_with(self, r):
        return False

def new_rectangle(top, left, bottom, right):
    if top > bottom or left > right:
        return EmptyRectangle()
    else:
        return Rectangle(top, left, bottom, right)
