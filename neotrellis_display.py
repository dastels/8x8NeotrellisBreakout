import time
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

#some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

PADDLE = (0, 255, 0)

class Adapter(object):

    def __init__(self, scale):
        self._scale = scale
        i2c_bus = busio.I2C(SCL, SDA)
        trelli = [
            [NeoTrellis(i2c_bus, False, addr=0x2F), NeoTrellis(i2c_bus, False, addr=0x2E)],
            [NeoTrellis(i2c_bus, False, addr=0x31), NeoTrellis(i2c_bus, False, addr=0x30)]
        ]

        self._trellis = MultiTrellis(trelli)
        for y in range(8):
            for x in range(8):
                self._trellis.color(x, y, OFF)
#                time.sleep(.05)


    def update(self, board):
        cells = board.cells
        for x in range(8):
            for y in range(8):
                #print('{0} {1}: {2} '.format(row, col, cells[row + 1][col + 1].color))
                self._trellis.color(x, y, cells[8 - x][y + 1].color)
