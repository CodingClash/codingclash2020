import random
from stubs import *


def inbounds(a, b):
    return a >= 0 and b >= 0 and a < GameConstants.BOARD_WIDTH and b < GameConstants.BOARD_HEIGHT


class HQ:

    def __init__(self, team, location):
        self.team = team
        self.location = location

