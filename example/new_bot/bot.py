import random


class HQ:
    def __init__(self):
        self.spawned = []
        self.team = get_team()
        self.location = get_location()
        self.opp_hq = [GameConstants.BOARD_HEIGHT - self.location[0], GameConstants.BOARD_WIDTH - self.location[1]]

    def run(self):
        if True:#get_cooldown() == 0:
            robot = RobotType.BUILDER
            if len(self.spawned) > 3:
                return

            dxdy = sorted([(x, y) for x in range(-1, 2) for y in range(-1, 2)],
                          key=lambda d: self.distance_2((self.location[0] + d[0], self.location[1] + d[1]),
                                                        tuple(self.opp_hq)))
            for (dx, dy) in dxdy:
                if dx == 0 and dy == 0:
                    continue
                loc = (self.location[0] + dx, self.location[1] + dy)
                if sense_location(loc).type == RobotType.NONE:
                    self.spawned.append(robot)
                    create(robot, loc)
                    return

    def distance_2(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class Builder:
    def __init__(self):
        self.spawned = []
        self.team = get_team()
        self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]

    def run(self):
        self.location = get_location()
        if self.try_create():
            return
        self.try_move()

    def try_create(self):
        robot = RobotType.REFINERY
        if len(self.spawned) == 1:
            robot = RobotType.BARRACKS
        elif len(self.spawned) == 2:
            robot = RobotType.TURRET
        elif len(self.spawned) != 0:
            return False

        dxdy = sorted([(x, y) for x in range(-1, 2) for y in range(-1, 2)],
                      key=lambda d: self.distance_2((self.location[0] + d[0], self.location[1] + d[1]),
                                                    tuple(self.opp_hq)))
        for (dx, dy) in dxdy:
            if dx == 0 and dy == 0:
                continue
            loc = (self.location[0] + dx, self.location[1] + dy)
            if sense_location(loc).type == RobotType.NONE:
                self.spawned.append(robot)
                create(robot, loc)
                return True

    def try_move(self):
        dx = 1 if self.opp_hq[0] > self.location[0] else -1 if self.opp_hq[0] < self.location[0] else 0
        dy = 1 if self.opp_hq[1] > self.location[1] else -1 if self.opp_hq[1] < self.location[1] else 0
        options = [(dx, dy), (dx, 0), (0, dy)]
        for dx, dy in options:
            loc = (self.location[0] + dx, self.location[1] + dy)
            if sense_location(loc).type == RobotType.NONE:
                move(loc)
                return

    def distance_2(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class Gunner:
    def __init__(self):
        self.team = get_team()
        # TODO: get HQ loc using blockchain comms
        # self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        # self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]

    def try_attack(self):
        attackable = sorted(sense(), key=lambda e: self.distance_2(e.location, self.location))
        for curr in attackable:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.GUNNER_ATTACK_RANGE:
                attack(curr.location)
                return True
        return False

    def try_move(self):
        dxdy = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
        for (dx, dy) in dxdy:
            if dx == 0 and dy == 0:
                continue
            loc = (self.location[0] + dx, self.location[1] + dy)
            if sense_location(loc).type == RobotType.NONE:
                move(loc)
                return

    def run(self):
        dlog("You're going down buddy")
        self.location = get_location()
        if self.try_attack():
            return
        self.try_move()

    def distance_2(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class Tank:
    def __init__(self):
        self.team = get_team()
        # TODO: get HQ loc using blockchain comms
        # self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        # self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]

    def try_attack(self):
        attackable = sorted(sense(), key=lambda e: self.distance_2(e.location, self.location))
        for curr in attackable:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.TANK_ATTACK_RANGE:
                attack(curr.location)
                return True
        return False

    def try_move(self):
        dxdy = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
        for (dx, dy) in dxdy:
            if dx == 0 and dy == 0:
                continue
            loc = (self.location[0] + dx, self.location[1] + dy)
            if sense_location(loc).type == RobotType.NONE:
                move(loc)
                return

    def run(self):
        self.location = get_location()
        if self.try_attack():
            return
        self.try_move()

    def distance_2(self, p1, p2):
        if p1 is None or p2 is None:
            return float("inf")
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class Grenader:
    def __init__(self):
        self.team = get_team()
        # TODO: get HQ loc using blockchain comms
        # self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        # self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]

    def try_attack(self):
        targets = sorted(sense(), key=lambda e: self.distance_2(e.location, self.location))
        for curr in targets:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.GRENADER_ATTACK_RANGE:
                attack(curr.location)
                return True
        return False

    def try_stun(self):
        targets = sorted(sense(), key=lambda e: self.distance_2(e.location, self.location))
        for curr in targets:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.GRENADER_STUN_RANGE:
                stun(curr.location)
                return True
        return False

    def try_move(self):
        dxdy = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
        for (dx, dy) in dxdy:
            if dx == 0 and dy == 0:
                continue
            loc = (self.location[0] + dx, self.location[1] + dy)
            if sense_location(loc).type == RobotType.NONE:
                move(loc)
                return

    def run(self):
        self.location = get_location()
        rand_num = random.randrange(0, 1)
        if not rand_num and self.try_attack():
            return
        elif rand_num and self.try_stun():
            return
        self.try_move()

    def distance_2(self, p1, p2):
        if p1 is None or p2 is None:
            return float("inf")
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class Barracks:
    def __init__(self):
        self.spawned = []
        self.team = get_team()
        self.location = get_location()
        # TODO: get HQ loc using blockchain comms
        # self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        # self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]

    def run(self):
        if self.try_create():
            return

    def try_create(self):
        robot = RobotType.GUNNER
        if len(self.spawned) == 1:
            robot = RobotType.TANK
        elif len(self.spawned) == 2:
            robot = RobotType.GRENADER
        elif len(self.spawned) != 0:
            return False

        dxdy = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
        for (dx, dy) in dxdy:
            if dx == 0 and dy == 0:
                continue
            loc = (self.location[0] + dx, self.location[1] + dy)
            if sense_location(loc).type == RobotType.NONE:
                self.spawned.append(robot)
                create(robot, loc)
                return True

    def distance_2(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class Refinery:
    def __init__(self):
        self.spawned = []
        self.team = get_team()
        self.location = get_location()
        # TODO: get HQ loc using blockchain comms
        # self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        # self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]

    #TODO: Does refinery just passively run, or should we add functionality that users have to implement?
    def run(self):
        return


class Turret:
    def __init__(self):
        self.spawned = []
        self.team = get_team()
        self.location = get_location()
        # TODO: get HQ loc using blockchain comms
        # self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        # self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]

    def run(self):
        if self.try_attack():
            return

    def try_attack(self):
        targets = sorted(sense(), key=lambda e: self.distance_2(e.location, self.location))
        for curr in targets:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.TURRET_ATTACK_RANGE:
                attack(curr.location)
                return True
        return False

    def distance_2(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


if get_type() == RobotType.BUILDER:
    robot = Builder()
elif get_type() == RobotType.GUNNER:
    robot = Gunner()
elif get_type() == RobotType.TANK:
    robot = Tank()
elif get_type() == RobotType.GRENADER:
    robot = Grenader()
elif get_type() == RobotType.BARRACKS:
    robot = Barracks()
elif get_type() == RobotType.REFINERY:
    robot = Refinery()
elif get_type() == RobotType.TURRET:
    robot = Turret()
else:
    robot = HQ()

def turn():
    robot.run()
