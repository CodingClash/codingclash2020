import random
from stubs import *


TEAM_KEY = 100 if get_team() == TeamColor.RED else 200

def add(loc1, loc2):
    return (loc1[0] + loc2[0], loc1[1] + loc2[1])

def sub(loc1, loc2):
    return (loc1[0] - loc2[0], loc1[1] - loc2[1])

def inbounds(a, b):
    return a >= 0 and b >= 0 and a < GameConstants.BOARD_WIDTH and b < GameConstants.BOARD_HEIGHT

def filter_blockchain(round_num):
    blocks = get_blockchain(round_num)
    valid = []
    for b in blocks:
        if b[0] == TEAM_KEY:
            valid.append(b)
    return valid



class Robot:
    def __init__(self):
        self.team = get_team()
        self.type = get_type()
        self.location = get_location()
        self.board_width = GameConstants.BOARD_WIDTH
        self.board_height = GameConstants.BOARD_HEIGHT
        self.round_num = 0
        if self.type != RobotType.HQ:
            blocks = filter_blockchain(0)
            assert(len(blocks) == 1)
            block = blocks[0]
            self.hq_loc = (block[1], block[2])
        else:
            self.hq_loc = self.location
        self.enemy_hq_loc = sub((self.board_width, self.board_height), self.hq_loc)


    def run(self):
        self.oil = get_oil()
        self.health = get_health()
        self.is_stunned = is_stunned()


    def trybuild(self, robot_type):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                delta = (dx, dy)
                loc = add(self.location, delta)
                sensed = sense_location(loc)
                if sensed.type == RobotType.NONE:
                    create(robot_type, loc)
                    return True
        return False


class HQ(Robot):

    def __init__(self):
        super().__init__()
        add_to_blockchain([TEAM_KEY, self.location[0], self.location[1]])
        self.num_builders = 0


    def run(self):
        super().run()
        if self.num_builders < 4:
            if self.oil > GameConstants.BUILDER_COST:
                if self.trybuild(RobotType.BUILDER):
                    return


class Builder(Robot):

    def __init__(self):
        super().__init__()
    

    def run(self):
        super().run()


type_to_obj = {
    RobotType.HQ: HQ,
    RobotType.BUILDER: Builder
}

obj = type_to_obj[get_type()]
robot = obj()

def turn():
    robot.run()

