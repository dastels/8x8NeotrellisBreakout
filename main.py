import time

import rotaryio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer

from board import D5, D11, D12
from paddle import Paddle
import neotrellis_display
from game_board import Board

import adafruit_logging as logging
logger = logging.getLogger('breakout')

encoder = rotaryio.IncrementalEncoder(D11, D12)
last_position = encoder.position

switch = DigitalInOut(D5)
switch.direction = Direction.INPUT
switch.pull = Pull.UP
button = Debouncer(switch)

paddle = Paddle(8)

board = Board(8, 8, 8, paddle)
display = neotrellis_display.Adapter(8)

board.reset_game()
board.set_up_level(0)
display.update(board)

board.dump()

logger.debug('Starting game')
while not board.is_game_over:
    #the trellis can only be read every 17 millisecons or so
    #    trellis.sync()
    display.update(board)

    logger.debug('Waiting for launch')
    button.update()
    # wait for the encoder button to be pushed, then launch a ball & start the round
    while not button.fell:
        button.update()
    logger.debug('Launching a ball')
    board.launch()
    display.update(board)

    while board.is_still_in_play:

        # logger.debug('Pausing')
        # button.update()
        # while not button.fell:
        #     button.update()

        position = encoder.position
        if position == last_position:
            paddle.stop()
        else:
            if position > last_position:
                paddle.move_right()
            else:
                paddle.move_left()

        board.update_paddle()
        board.move_balls()
        display.update(board)

        last_position = position
