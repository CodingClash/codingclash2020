import random

class Gunner:
    def __init__(self):
        self.team = get_team()
        self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]



    def run(self):
#        dlog("Running gunner")
        self.location = get_location()
        attackable = sorted(sense(), key = lambda e: self.distance_2(e.location, self.location))
        for curr in attackable:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.GUNNER_ATTACK_RANGE:
                attack(curr.location)
                return


        dx = 1 if self.opp_hq[0] > self.location[0] else -1 if self.opp_hq[0] < self.location[0] else 0
        dy = 1 if self.opp_hq[1] > self.location[1] else -1 if self.opp_hq[1] < self.location[1] else 0
        options = [(dx, dy), (dx, 0), (0, dy)]
        for dx, dy in options:
            loc = (self.location[0] + dx, self.location[1] + dy)
            if sense_location(loc).type == RobotType.NONE:
                move(loc)
                return


    def distance_2(self, p1, p2):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2


class HQ:
    def __init__(self):
        self.team = get_team()
        self.location = get_location()
        add_to_blockchain([1, 2, 3])
        dlog(self.location)


    def run(self):
        if get_cooldown() == 0:
            robot = RobotType.GUNNER
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    loc = (self.location[0] + dx, self.location[1] + dy)
                    if sense_location(loc).type == RobotType.NONE:
                        create(robot, loc)
                        return


if get_type()==RobotType.GUNNER: robot = Gunner()
elif get_type()==RobotType.TANK: robot = Tank()
else: robot = HQ()

def turn():
    robot.run()
