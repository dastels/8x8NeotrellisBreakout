import math
from cells import create_block_cell, EmptyCell, TopWallCell, SideWallCell, PaddleCell, OutOfBoundsCell, BallCell
from levels import levels
from ball import Ball

import adafruit_logging as logging
logger = logging.getLogger('breakout')

MAX_BALLS_IN_PLAY = 2

class Board(object):


    def __init__(self, scale, rows, columns, paddle):
        """
        :param scale: the number of mathamatical points in a display pixel
        :param rows: the number of rows on screen
        :param columns: the number of columns on the screen
        :param paddle: the paddle object to use
        """
        self._paddle = paddle
        self._scale = scale
        self._rows = rows + 2             # stored rows & columns include a one pixel halo
        self._columns = columns + 2
        self._score = 0
        self._in_play = False
        self._balls_remaining = 3
        self._number_of_balls = 1
        self._balls = []
        for _ in range(MAX_BALLS_IN_PLAY):
            self._balls.append(None)
        self._cells = []
        for _ in range(self._columns):
            row_cells = []
            self._cells.append(row_cells)
            for _ in range(self._rows):
                row_cells.append(EmptyCell())
        self._add_border()
        self._add_out_of_bounds()
        self.update_paddle()
        self.reset_game()

    def reset_game(self):
        self._score = 0
        self.in_play = False
        self._balls_remaining = 3
        self._number_of_balls = 1
        for i in range(MAX_BALLS_IN_PLAY):
            self._balls[i] = None

    @property
    def width(self):
        return (self._columns - 2) * self._scale

    @property
    def height(self):
        return self._rows - 2

    @property
    def scale(self):
        return self._scale

    @property
    def paddle_x(self):
        return self._paddle.position.x

    @property
    def paddle_width(self):
        return self._paddle.width

    @property
    def cells(self):
        return self._cells

    def cell_at(self, x_or_coordinate, y=None, value=None):
        if isinstance(x_or_coordinate, int):
            x = x_or_coordinate
        else:
            x = x_or_coordinate.x
            y = x_or_coordinate.y
        previous_value = self._cells[x][y]
        if value is not None:
            self._cells[x][y] = value
            if x == 1 and y == 7 and value.label == 'P' :
                raise Exception('', '')
        return previous_value

    def _add_border(self):
        """Add wall cels along the top and sides"""
        top = TopWallCell(self)
        left = SideWallCell(self, False)
        right = SideWallCell(self, True)
        for col in range(self._columns):
            self.cell_at(col, self._rows - 1, top)
        for row in range(self._rows):
            self.cell_at(0, row, left)
            self.cell_at(self._columns - 1, row, right)

    def _add_out_of_bounds(self):
        """Add a row of out of bounds cells along the bottom"""
        cell = OutOfBoundsCell(self)
        for x in range(self._columns):
            self.cell_at(x, 0, cell)


    def add_blocks(self):
        self.set_up_level(0)


    def set_up_level(self, level):
        logger.debug('Loading level {0}'.format(level))
        level_data = levels[level]
        data_index = 0
        for row in range(self._rows - 2, 1, -1):
            line = level_data[data_index]
            data_index += 1
            for col in range(1, self._columns - 1):
                # print('    Col: {0}'.format(col))
                self.cell_at(col, row, create_block_cell(self, line[col - 1], row, col))

    def update_paddle(self):
        for x in range(1, self._columns - 1):
            self.cell_at(x, 1, EmptyCell())
        x = self._paddle.position.x // self._scale
        for offset in range(self._paddle.width // self._scale):
            self.cell_at(int(x + offset), 1, PaddleCell(self, self._paddle))

    def clear_level(self):
        pass

    def display_game_over(self):
        pass

    def process_ball(self, ball):
        logger.debug('Processing ball')
        self.check_for_and_handle_collision(ball)

    def check_for_and_handle_collision(self, ball):
        if self.check_for_and_handle_ball_collision(ball):
            logger.debug('Ball collision')
            return True
        if self.check_for_and_handle_non_corner_collision(ball):
            logger.debug('Non corner collision')
            return True
        if self.check_for_and_handle_corner_collision(ball):
            logger.debug('Corner collision')
            return True
        return False

    def check_for_and_handle_ball_collision(self, ball1):
        for ball_number in range(MAX_BALLS_IN_PLAY):
            ball2 = self._balls[ball_number]
            if ball2 is None:
                continue
            if ball2 == ball1:
                continue
            n12 = ball1.center.vector_difference(ball2.center)
            if n12.magnitude > 8:         #not touching
                continue
            if ball1.velocity.is_in_the_same_direction_as(n12):
                continue
            n12.normalize()
            projection_onto_n12_of_v1 = n12 * n12.dot(ball1.velocity)
            n21 = ball2.center.vector_difference(ball1.center)
            n21.normalize()
            projection_onto_n21_of_v2 = n21 * n21.dot(ball2.velocity)
            ball1.add_to_velocity(projection_onto_n21_of_v2 - projection_onto_n12_of_v1)
            ball2.add_to_velocity(projection_onto_n12_of_v1 - projection_onto_n21_of_v2)
            return True
        return False

    def check_for_and_handle_corner_collision(self, ball):
        top = ball.top_cell_position.y
        bottom = ball.bottom_cell_position.y
        left = ball.left_cell_position.x
        right = ball.right_cell_position.x

        if ball.is_heading_primarily_up:
            if ball.is_heading_left:
                self.vertical_hit(self.cell_at(top, left), ball)
                return True
            if ball.is_heading_right:
                self.vertical_hit(self.cell_at(top, right), ball)
                return True
        if ball.is_heading_primarily_down:
            if ball.is_heading_left:
                self.vertical_hit(self.cell_at(bottom, left), ball)
                return True
            if ball.is_heading_right:
                self.vertical_hit(self.cell_at(bottom, right), ball)
                return True
        if ball.is_heading_primarily_left:
            if ball.is_heading_up:
                self.horizontal_hit(self.cell_at(top, left), ball)
                return True
            if ball.is_heading_down:
                self.horizontal_hit(self.cell_at(bottom, left), ball)
                return True
        if ball.is_heading_primarily_right:
            if ball.is_heading_up:
                self.horizontal_hit(self.cell_at(top, right), ball)
                return True
            if ball.is_heading_down:
                self.horizontal_hit(self.cell_at(bottom, right), ball)
                return True

        return False

    def vertical_hit(self, cell, ball):
        if not cell.is_vertical:
            return False
        if not cell.is_hit_by(ball):
            return False
        cell.process_hit(ball)
        ball.reflect_from_side(cell)
        return True

    def horizontal_hit(self, cell, ball):
        if not cell.is_horizontal:
            return False
        if not cell.is_hit_by(ball):
            return False
        cell.process_hit(ball)
        ball.reflect_from_top_bottom(cell)
        return True

    def check_for_and_handle_non_corner_collision(self, ball):
        if self.check_for_and_handle_bottom_hit(self.cell_at(ball.bottom_cell_position), ball):
            return True
        if self.check_for_and_handle_top_hit(self.cell_at(ball.top_cell_position), ball):
            return True
        if self.check_for_and_handle_left_hit(self.cell_at(ball.left_cell_position), ball):
            return True
        if self.check_for_and_handle_right_hit(self.cell_at(ball.right_cell_position), ball):
            return True
        return False

    def check_for_and_handle_left_hit(self, cell, ball):
        if not cell.is_vertical:
            return False
        if not cell.is_hit_by(ball):
            return False
        if ball.is_heading_right:
            return False
        cell.process_hit(ball)
        ball.reflect_from_side(cell)
        return True

    def check_for_and_handle_right_hit(self, cell, ball):
        if not cell.is_vertical:
            return False
        if not cell.is_hit_by(ball):
            return False
        if ball.is_Heading_Left:
            return False
        cell.process_hit(ball)
        ball.reflect_from_side(cell)
        return True

    def check_for_and_handle_top_hit(self, cell, ball):
        if not cell.is_horizontal:
            return False
        if not cell.is_hit_by(ball):
            return False
        if ball.is_heading_down:
            return False
        cell.process_hit(ball)
        ball.reflect_from_top_bottom(cell)
        return True

    def check_for_and_handle_bottom_hit(self, cell, ball):
        if not cell.is_horizontal:
            return False
        if not cell.is_hit_by(ball):
            return False
        if ball.is_heading_up:
            return False
        cell.process_hit(ball)
        ball.reflect_from_top_bottom(cell)
        return True

    def went_out_of_bounds(self, ball):
        logger.debug('Out of bounds')
        for ball_number in range(MAX_BALLS_IN_PLAY):
            if self._balls[ball_number] is None:
                continue
            if self._balls[ball_number] == ball:
                continue
            self._balls[ball_number] = None
            self._number_of_balls -= 1
            if self._number_of_balls == 0:
                self._balls_remaining -= 1
                self._in_play = False

    @property
    def is_still_in_play(self):
        return self._in_play

    @property
    def is_game_over(self):
        return self._balls_remaining == 0

    def clear_balls(self):
        for i in range(MAX_BALLS_IN_PLAY):
            self._balls[i] = None

    def remove_block(self, cell):
        self.cell_at(cell.row, cell.column, EmptyCell())


    def move_balls(self):
        for ball in self._balls:
            if ball is None:
                continue
            old_raw_position = ball.position
            old_position = self.convert_to_tile_position(ball.position)
            ball_cell = self.cell_at(old_position.x, old_position.y)
            self.cell_at(old_position.y, old_position.x,  EmptyCell())
            ball.move()
            new_raw_position = ball.position
            if math.fabs(old_raw_position.x - new_raw_position.x) > 0.1 or math.fabs(old_raw_position.y - new_raw_position.y) > 0.1:
                logger.debug('Moving ball from %s', old_raw_position)
                logger.debug('Moving ball to %s', new_raw_position)
            logger.debug('Ball at %s', new_raw_position)
            new_position = self.convert_to_tile_position(ball.position)
            self.cell_at(new_position.y, new_position.x, ball_cell)


    def launch(self):
        self.clear_balls()
        self.add_and_enable_ball(Ball(self))
        self._in_play = True

    def addBall(self, row, column, initial_velocity):
        self.add_and_enable_ball(Ball(self, column * self._scale, row * self._scale, initial_velocity))

    def add_and_enable_ball(self, ball):
        for ball_number in range(MAX_BALLS_IN_PLAY):
            if self._balls[ball_number] is None:
                self._balls[ball_number] = ball
                ball_position = self.convert_to_tile_position(ball.position)
                logger.debug('Ball x: %d, y: %d', ball_position.x, ball_position.y)
                self.cell_at(ball_position.x, ball_position.y, BallCell(self, ball_position.y, ball_position.x))
                self._number_of_balls += 1
                return

    @property
    def can_launch_another_ball(self):
        return self._number_of_balls < MAX_BALLS_IN_PLAY

    def convert_to_tile_position(self, coord):
        return coord.convert_to_tile_position(self._scale)

    def dump(self):
        for row in range(self._rows-1, -1, -1):
            buf = ''
            for col in range(self._columns):
                buf = buf + self.cell_at(col, row).label
            logger.info('Row %d: %s', row, buf)
