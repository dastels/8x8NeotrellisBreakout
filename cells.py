from rectangle import Rectangle

class AbstractCell:

    @property
    def bounding_box(self):
        return Rectangle(0, 0, -1, -1)

    @property
    def color(self):
        return (0, 0, 0)

    @property
    def label(self):
        return 'A'


class Cell(AbstractCell):

    def __init__(self, board, row, column):
        self._board = board
        self._row = row
        self._column = column

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def tile_number(self):
        return 0

    def is_hit_by(self, ball):
        return ball.is_colliding_with(self.bounding_box)

    def process_hit(self, ball):
        pass

    @property
    def is_vertical(self):
        return True

    @property
    def is_horizontal(self):
        return True

    def reflect_off_vertical(self, v):
        v.flip_x()

    def reflect_off_horizontal(self, v):
        v.flip_y()

    @property
    def label(self):
        return 'C'

class EmptyCell(Cell):

    def __init__(self):
        Cell.__init__(self, 0, -1, -1)
        self._empty_box = Rectangle(0, 0, -1, -1)

    def is_hit_by(self, ball):
        return False

    @property
    def bounding_box(self):
        return self._empty_box

    @property
    def label(self):
        return 'E'


class PaddleCell(Cell):

    def __init__(self, board, paddle):
        pos = board.convert_to_tile_position(paddle.position)
        Cell.__init__(self, board, pos.y, pos.x)
        self._paddle = paddle

    @property
    def bounding_box(self):
        return Rectangle(self._board.scale * 2, self._paddle.position.x, self._board.scale, self._paddle.position.x + self._paddle.width)

    def process_hit(self, ball):
        Cell.process_hit(self, ball)

    @property
    def is_vertical(self):
        return False

    def reflect_off_horizontal(self, v):
        self._paddle.add_velocity_to(v)
        v.flip_y()

    @property
    def color(self):
        return (255, 255, 0)

    @property
    def label(self):
        return 'P'

class OutOfBoundsCell(Cell):
    def __init__(self, board):
        Cell.__init__(self, board, 0, 0)
        self._bounds = Rectangle(board.scale, 0, 0, board.width - 1)

    @property
    def bounding_box(self):
        return self._bounds

    def process_hit(self, ball):
        Cell.process_hit(self, ball)
        self._board.went_out_of_bounds(ball)

    @property
    def label(self):
        return 'O'

class BallCell(Cell):

    def __init__(self, board, row, column):
        Cell.__init__(self, board, row, column)
        scale = board.scale
        self._bounds = Rectangle(row * scale, column * scale, row * scale + (scale - 1), column * scale + (scale - 1))

    @property
    def bounding_box(self):
        return self._bounds

    @property
    def color(self):
        return (222, 222, 255)

    @property
    def label(self):
        return 'b'

class BlockCell(Cell):

    def __init__(self, board, row, column):
        Cell.__init__(self, board, row, column)
        scale = board.scale
        self._bounds = Rectangle(row * scale, column * scale, row * scale + (scale - 1), column * scale + (scale - 1))

    @property
    def value(self):
        return 0

    @property
    def removable(self):
        return True

    def process_hit(self, ball):
        Cell.process_hit(self, ball)
        if self.removable:
            self._board.remove_block(self)
        self._board.add_to_score(self.value)

    @property
    def bounding_box(self):
        return self._bounds

    @property
    def label(self):
        return 'B'

class BlueBlockCell(BlockCell):

    def __init__(self, board, row, column):
        BlockCell.__init__(self, board, row, column)

    @property
    def value(self):
        return 5

    @property
    def color(self):
        return (0, 0, 255)

    @property
    def label(self):
        return 'U'

class RedBlockCell(BlockCell):

    def __init__(self, board, row, column):
        BlockCell.__init__(self, board, row, column)

    @property
    def value(self):
        return 1

    @property
    def color(self):
        return (255, 0, 0)

    @property
    def label(self):
        return 'R'

class GreenBlockCell(BlockCell):

    def __init__(self, board, row, column):
        BlockCell.__init__(self, board, row, column)

    @property
    def value(self):
        return 10

    @property
    def color(self):
        return (0, 255, 0)

    @property
    def label(self):
        return 'G'

class SolidBlockCell(BlockCell):

    def __init__(self, board, row, column):
        BlockCell.__init__(self, board, row, column)

    @property
    def value(self):
        return 1

    @property
    def removable(self):
        return False

    @property
    def color(self):
        return (64, 64, 64)

    @property
    def label(self):
        return 'S'


class BallBlockCell(BlockCell):

    def __init__(self, board, row, column):
        BlockCell.__init__(self, board, row, column)

    @property
    def value(self):
        return 20 if self._board.can_launch_another_ball else 0

    def process_hit(self, ball):
        BlockCell.process_hit(self, ball)
        self._board.add_ball(self._row, self._column, ball.transfered_velocity)

    @property
    def removable(self):
        return self._board.can_launch_another_ball

    @property
    def color(self):
        return (255, 255, 255)

    @property
    def label(self):
        return 'o'


class WallCell(Cell):

    def __init__(self, top, left, bottom, right):
        Cell.__init__(self, None, 0, 0)
        self._bounds = Rectangle(top, left, bottom, right)

    @property
    def bounding_box(self):
        return self._bounds

    @property
    def label(self):
        return 'W'


class SideWallCell(WallCell):

    def __init__(self, board, on_right):
        left = board.width if on_right else -1 * board.scale
        right = board.width + board.scale if on_right else -1
        WallCell.__init__(self, 0, left, board.height - 1, right)

    @property
    def is_horizontal(self):
        return False

    @property
    def label(self):
        return '|'


class TopWallCell(WallCell):

    def __init__(self, board):
        WallCell.__init__(self, 0, 0, board.height - 1, board.width - 1)

    @property
    def is_vertical(self):
        return False

    @property
    def label(self):
        return '-'


def create_block_cell(board, char, row, col):
    if char == 'B':
        return BlueBlockCell(board, row, col)
    elif char == 'G':
        return GreenBlockCell(board, row, col)
    elif char == 'R':
        return RedBlockCell(board, row, col)
    elif char == 'S':
        return SolidBlockCell(board, row, col)
    elif char == 'o':
        return BallBlockCell(board, row, col)
    else:
        return EmptyCell()
