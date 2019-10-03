from random import random
from math import pi
from rectangle import Rectangle
from coordinate import Coordinate
from vector import Vector

BALL_SIZE = 8
COLLISION_MARGIN = 1

class Ball(object):

    def __init__(self, board, x=None, y=None, initial_velocity=None):
        self._board = board
        self._collision_bounding_box = Rectangle(0, 0, 0, 0)
        if x is None:
            self._position  = Coordinate(board.paddle_x + (board.paddle_width // 2) - (BALL_SIZE // 2), board.scale * 2)
            self._velocity = Vector(pi / 8, board.scale)
        else:
            self._position = Coordinate(x, y)
            self._velocity = initial_velocity

    def update_bounding_box(self):
        self._collision_bounding_box = Rectangle(self._position.y + COLLISION_MARGIN,
                                                 self.position.x + COLLISION_MARGIN,
                                                 self.position.y + (BALL_SIZE - 1) - COLLISION_MARGIN,
                                                 self._position.x + (BALL_SIZE - 1) - COLLISION_MARGIN)

    @property
    def velocity(self):
        return self._velocity

    def add_to_velocity(self, vector):
        self._velocity += vector
        self.velocity.clip_magnitude_between(0.5, 2.0)

    def subtract_from_velocity(self, vector):
        self._velocity -= vector

    def move(self):
        self._position.move_by(self._velocity)
        self._position.clip_x(0, self._board.width - BALL_SIZE)
        self._position.clip_y(0, self._board.height)
        self.update_bounding_box()
        self._board.process_ball(self)

    @property
    def is_heading_left(self):
        return self._velocity.is_left

    @property
    def is_heading_right(self):
        return self._velocity.is_right

    @property
    def is_heading_up(self):
        return self._velocity.is_up

    @property
    def is_heading_down(self):
        return self._velocity.is_down

    @property
    def is_heading_primarily_left(self):
        return self._velocity.is_primarily_left

    @property
    def is_heading_primarily_right(self):
        return self._velocity.is_primarily_right

    @property
    def is_heading_primarily_up(self):
        return self._velocity.is_primarily_up

    @property
    def is_heading_primarily_down(self):
        return self._velocity.is_primarily_down

    @property
    def center(self):
        return self._collision_bounding_box.center

    @property
    def position(self):
        return self._position

    @property
    def left_cell_position(self):
        return self._board.convert_to_tile_position(self._collision_bounding_box.middle_left)

    @property
    def right_cell_position(self):
        return self._board.convert_to_tile_position(self._collision_bounding_box.middle_right)

    @property
    def top_cell_position(self):
        return self._board.convert_to_tile_position(self._collision_bounding_box.top_center)

    @property
    def bottom_cell_position(self):
        return self._board.convert_to_tile_position(self._collision_bounding_box.bottom_center)

    def reflect_from_left_right(self, cell):
        cell.reflect_off_vertical(self._velocity)

    def reflect_from_top_bottom(self, cell):
        cell.reflect_off_horizontal(self._velocity)

    @property
    def bounding_box(self):
        return self._collision_bounding_box

    def is_colliding_with(self, box):
        return self._collision_bounding_box.collides_with(box)

    @property
    def transferred_velocity(self):
        angle = random() * 3.14 - 1.57
        magnitude = random() - 0.5
        return self.velocity + Vector(angle, magnitude)
