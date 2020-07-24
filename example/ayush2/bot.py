import random
from stubs import *


def inbounds(a, b):
    return a >= 0 and b >= 0 and a < GameConstants.BOARD_WIDTH and b < GameConstants.BOARD_HEIGHT

class HQ:
    def __init__(self):
        self.spawned = []
        self.team = get_team()
        self.location = get_location()
        self.opp_hq = [GameConstants.BOARD_HEIGHT - self.location[0], GameConstants.BOARD_WIDTH - self.location[1]]

    def run(self):
        self.try_create()

    def try_create(self):
        robot = RobotType.BUILDER
        if len(self.spawned)==0:
            add_to_blockchain([1 if get_team() == TeamColor.RED else 0, self.location[0], self.location[1], 0, 0])
        if len([1 for i in sense() if i.type==RobotType.WALL])<7:
            add_to_blockchain([1 if get_team() == TeamColor.RED else 0, 100, 100, 0, 0])
        if len([1 for i in sense() if i.type==RobotType.BUILDER])==4:
            add_to_blockchain([1 if get_team() == TeamColor.RED else 0, 101, 101, 0, 0])
        
        if len(self.spawned) > 3:
            return False
        if get_oil() < GameConstants.BUILDER_COST:
            return False

        dxdy = [(1,0), (0,1), (-1, 0), (0,-1)]
        for (dx, dy) in dxdy:
            if dx == 0 and dy == 0:
                continue
            loc = (self.location[0] + dx, self.location[1] + dy)
            if not can_sense_location(loc):
                continue
            if sense_location(loc).type == RobotType.NONE:
                self.spawned.append(robot)
                create(robot, loc)
                return True

    def distance_2(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class Builder:
    def __init__(self):
        self.spawned = []
        self.team = get_team()
        self.secret = 1 if get_team() == TeamColor.RED else 0
        self.my_hq = [i for i in get_blockchain(0) if i[0]==self.secret][0][1:3]
        self.opp_hq = (GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1])
        self.should_move = False

    def run(self):
        self.location = get_location()
        if self.try_create():
            return
        self.try_move()

    def try_create(self):
        robot = RobotType.REFINERY
        cost = GameConstants.REFINERY_COST
        if len(self.spawned)%3 == 1:
            robot = RobotType.BARRACKS
            cost = GameConstants.BARRACKS_COST
        elif len(self.spawned)%3 == 2:
            robot = RobotType.TURRET
            cost = GameConstants.TURRET_COST

        #elif len(self.spawned) != 0:
        #    return False


        dxdy = sorted([(x, y) for x in range(-1, 2) for y in range(-1, 2)],
                      key=lambda d: self.distance_2((self.location[0] + d[0], self.location[1] + d[1]),
                                                    tuple(self.opp_hq)))
        #dlog(dxdy)
        acceptable = [1, 2]

        if len(self.spawned)<2:
            if get_oil() < cost:
                return False
            dlog(self.spawned)
            for (dx, dy) in dxdy:
                if dx == 0 and dy == 0:
                    continue
                loc = (self.location[0] + dx, self.location[1] + dy)
                if not can_sense_location(loc):
                    continue
                if sense_location(loc).type == RobotType.NONE and self.distance_2(loc, self.my_hq)>2:
                    self.spawned.append(robot)
                    create(robot, loc)
                    return True

        elif get_round_num()!=0 and [self.secret, 100, 100, 0, 0] in get_blockchain(get_round_num()-1):
            for (i, j) in dxdy:
                loc = (self.location[0] + i, self.location[1] + j)
                if self.distance_2(loc, self.my_hq) in acceptable:
                    if get_oil() < GameConstants.WALL_COST:
                        dlog("Too expensive")
                        return False
                    if sense_location(loc).type == RobotType.NONE:
                        dlog("Created")
                        self.spawned.append(RobotType.WALL)
                        create(RobotType.WALL, loc)
                        return True
        else:
            if get_oil() < 2*cost:
                return False
            for (dx, dy) in dxdy:
                if dx == 0 and dy == 0:
                    continue
                loc = (self.location[0] + dx, self.location[1] + dy)
                if not can_sense_location(loc):
                    continue
                if sense_location(loc).type == RobotType.NONE and self.distance_2(loc, self.my_hq)>8 and self.distance_2(loc, self.my_hq)<self.distance_2(self.location, self.my_hq):
                    self.spawned.append(robot)
                    create(robot, loc)
                    return True

    def try_move(self):
        if [self.secret, 101, 101, 0, 0] in get_blockchain(get_round_num()-1):
            self.should_move=True
        if self.should_move:
            if get_round_num()!=0 and [self.secret, 100, 100, 0, 0] in get_blockchain(get_round_num()-1):
                self.opp_hq = self.my_hq
            else: self.opp_hq = (GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1])
            #dlog(self.opp_hq)
            #dlog(get_round_num())
            dx = 1 if self.opp_hq[0] > self.location[0] else -1 if self.opp_hq[0] < self.location[0] else 0
            dy = 1 if self.opp_hq[1] > self.location[1] else -1 if self.opp_hq[1] < self.location[1] else 0
            options = [(dx, dy), (dx, 0), (0, dy)]
            for dx, dy in options:
                loc = (self.location[0] + dx, self.location[1] + dy)
                if not can_sense_location(loc) or (self.opp_hq==self.my_hq and self.distance_2(loc, self.opp_hq) not in [4, 5, 8]):
                    continue
                if self.opp_hq!=self.my_hq and [(i.type, i.team) for i in sense()].count((RobotType.GUNNER, get_team())) < 2:
                    return
                if sense_location(loc).type == RobotType.NONE:
                    move(loc)
                    return
            
            backup = [(dx, 1), (dx, -1), (1, dy), (-1, dy), (0, 0)]
            backup = sorted(backup, key = lambda x: self.distance_2(self.opp_hq, (self.location[0]+x[0], self.location[1]+x[1])))
            for dx, dy in backup:
                loc = (self.location[0] + dx, self.location[1] + dy)
                if not can_sense_location(loc) or (self.opp_hq==self.my_hq and self.distance_2(loc, self.opp_hq) not in [4, 5, 8]):
                    continue
                if sense_location(loc).type == RobotType.NONE:
                    move(loc)
                    return
        return

    def distance_2(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class Gunner:
    def __init__(self):
        self.team = get_team()
        self.secret = 1 if get_team() == TeamColor.RED else 0
        self.my_hq = [i for i in get_blockchain(0) if i[0]==self.secret][0][1:3]
        self.opp_hq = (GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1])

    def try_attack(self):
        if get_oil() < GameConstants.GUNNER_ATTACK_COST:
            return False
        self.location = get_location()
        attackable = sorted(sense(), key = lambda e: self.distance_2(e.location, self.location))
        for curr in attackable:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.GUNNER_ATTACK_RANGE:
                attack(curr.location)
                return True
        return False

    def try_move(self):
        dx = 1 if self.opp_hq[0] > self.location[0] else -1 if self.opp_hq[0] < self.location[0] else 0
        dy = 1 if self.opp_hq[1] > self.location[1] else -1 if self.opp_hq[1] < self.location[1] else 0
        options = [(dx, dy), (dx, 0), (0, dy)]

        if [i.type for i in sense()].count(RobotType.GUNNER) < 1: return
        for dx, dy in options:
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


    def distance_2(self, p1, p2):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2


class Tank:
    def __init__(self):
        self.team = get_team()
        self.secret = 1 if get_team() == TeamColor.RED else 0
        self.my_hq = [i for i in get_blockchain(0) if i[0]==self.secret][0][1:3]
        self.opp_hq = (GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1])

    def try_attack(self):
        if get_oil() < GameConstants.TANK_ATTACK_COST:
            return False
        self.location = get_location()
        attackable = sorted(sense(), key = lambda e: self.distance_2(e.location, self.location))
        for curr in attackable:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.TANK_ATTACK_RANGE:
                attack(curr.location)
                return True
        return False

    def try_move(self):
        dx = 1 if self.opp_hq[0] > self.location[0] else -1 if self.opp_hq[0] < self.location[0] else 0
        dy = 1 if self.opp_hq[1] > self.location[1] else -1 if self.opp_hq[1] < self.location[1] else 0
        options = [(dx, dy), (dx, 0), (0, dy)]

        if [i.type for i in sense()].count(RobotType.TANK) < 3: return
        for dx, dy in options:
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
        self.secret = 1 if get_team() == TeamColor.RED else 0
        self.my_hq = [i for i in get_blockchain(0) if i[0]==self.secret][0][1:3]
        self.opp_hq = (GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1])

    def try_attack(self):
        if get_oil() < GameConstants.GRENADER_DAMAGE_COST:
            return False
        targets = sorted(sense(), key=lambda e: self.distance_2(e.location, self.location))
        for curr in targets:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.GRENADER_DAMAGE_RANGE:
                attack(curr.location)
                return True
        return False

    def try_stun(self):
        if get_oil() < GameConstants.GRENADER_STUN_COST:
            return False
        targets = sorted(sense(), key=lambda e: self.distance_2(e.location, self.location))
        for curr in targets:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.GRENADER_STUN_RANGE:
                stun(curr.location)
                return True
        return False

    def try_move(self):
        dx = 1 if self.opp_hq[0] > self.location[0] else -1 if self.opp_hq[0] < self.location[0] else 0
        dy = 1 if self.opp_hq[1] > self.location[1] else -1 if self.opp_hq[1] < self.location[1] else 0
        options = [(dx, dy), (dx, 0), (0, dy)]
        for dx, dy in options:
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
        if len(self.spawned)<3:
            robot = RobotType.TANK
            cost = GameConstants.TANK_COST
        elif len(self.spawned)<5:
            robot = RobotType.GUNNER
            cost = GameConstants.GUNNER_COST
        elif len(self.spawned)<=7:
            robot = RobotType.GRENADER
            cost = GameConstants.GRENADER_COST

        if get_oil() < 6 * cost:
            return False

        dxdy = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
        for (dx, dy) in dxdy:
            if dx == 0 and dy == 0:
                continue
            loc = (self.location[0] + dx, self.location[1] + dy)
            if not can_sense_location(loc):
                continue
            if sense_location(loc).type == RobotType.NONE:
                self.spawned.append(robot)
                if len(self.spawned)==8:
                    self.spawned=[]
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
        self.team = get_team()
        self.location = get_location()
        # TODO: get HQ loc using blockchain comms
        # self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        # self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]

    def run(self):
        if self.try_attack():
            return

    def try_attack(self):
        if get_oil() < GameConstants.TURRET_ATTACK_COST:
            return False
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