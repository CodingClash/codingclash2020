import random
#import time

class Gunner:
    def __init__(self):
        self.team = get_team()
        self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        self.opp_hq = [GameConstants.BOARD_HEIGHT - self.my_hq[0], GameConstants.BOARD_WIDTH - self.my_hq[1]]

    def run(self):
        dlog("Meme")
        self.location = get_location()
        attackable = [(self.distance_2(e.location, self.location), e) for e in sense()]
        attacker = []
        dists = []
        for curr in attackable:
            if curr[1].team == get_team():
                continue
            if curr[0] <= GameConstants.GUNNER_ATTACK_RANGE:
                dists.append(curr[0])
                attacker.append(curr)
        
        if len(attacker)>0:
            min_dist = min(dists)
            attacker = [i[1] for i in attacker if i[0]==min_dist]
            attacker = [(0, i) if i.type == RobotType.GUNNER else (1, i) for i in attacker]
            #time.sleep(.1)
            attack(min(attacker, key = lambda x: x[0])[1].location)
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


class Tank:
    def __init__(self):
        self.team = get_team()
        self.my_hq = [i.location for i in sense() if i.type == RobotType.HQ and i.team == self.team][0]
        self.opp_hq = [GameConstants.BOARD_HEIGHT-self.my_hq[0], GameConstants.BOARD_WIDTH-self.my_hq[1]]


    def run(self):
        self.location = get_location()
        attackable = sorted(sense(), key = lambda e: self.distance_2(e.location, self.location))
        for curr in attackable:
            if curr.team == get_team():
                continue
            if self.distance_2(curr.location, self.location) <= GameConstants.TANK_ATTACK_RANGE:
                attack(curr.location)
                return

        dx = 1 if self.opp_hq[0] > self.location[0] else -1 if self.opp_hq[0] < self.location[0] else 0
        dy = 1 if self.opp_hq[1] > self.location[1] else -1 if self.opp_hq[1] < self.location[1] else 0
        options = [(dx, dy), (dx, 0), (0, dy)]
        #if [i.type for i in sense()].count(RobotType.GUNNER)<2: return
        for dx, dy in options:
            loc = (self.location[0] + dx, self.location[1] + dy)
            if sense_location(loc).type == RobotType.NONE:
                move(loc)
                return


    def distance_2(self, p1, p2):
        if p1 is None or p2 is None:
            return float("inf")
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

class HQ:
    def __init__(self):
        self.spawned = []
        self.team = get_team()
        self.location = get_location()
        self.opp_hq = [GameConstants.BOARD_HEIGHT-self.location[0], GameConstants.BOARD_WIDTH-self.location[1]]

    def run(self):
        if get_cooldown() == 0:
            if len(self.spawned)<5:
                robot = RobotType.TANK
            elif self.spawned[len(self.spawned)-5:] == [RobotType.TANK]*5:
                robot = RobotType.GUNNER
            elif self.spawned[len(self.spawned)-5:] == [RobotType.GUNNER]*5: 
                robot = RobotType.TANK
            else:
                robot = self.spawned[-1]
            dxdy = sorted([(x, y) for x in range(-1,2) for y in range(-1, 2)], key = lambda d: self.distance_2((self.location[0]+d[0], self.location[1]+d[1]), tuple(self.opp_hq)))
            for (dx, dy) in dxdy:
                if dx == 0 and dy == 0:
                    continue
                loc = (self.location[0] + dx, self.location[1] + dy)
                if sense_location(loc).type == RobotType.NONE:
                    self.spawned.append(robot)
                    create(robot, loc)
                    if len(set(self.spawned[len(self.spawned)-5:]))==1:
                        add_to_blockchain([6, 69, 9])
                    return

    def distance_2(self, p1, p2):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

if get_type()==RobotType.GUNNER: robot = Gunner()
elif get_type()==RobotType.TANK: robot = Tank()
else: robot = HQ()

def turn():
    robot.run()
