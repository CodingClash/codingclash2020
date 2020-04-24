import random

class HQ:
    def __init__(self):
        self.team = get_team()
        self.location = get_location()
        print("HQ created")
    
    def run(self):
        if get_cooldown() == 0:
            robot = RobotType.TANK
            if random.randint(0, 1) == 0:
                robot = RobotType.GUNNER
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    loc = (self.location[0] + dx, self.location[1] + dy)
                    create(robot, loc)


class Gunner:
    def __init__(self):
        print("Gunner created")
        self.team = get_team()
        self.location = get_location()

    def run(self):
        print("Running gunner at", self.team, self.location)

class Tank:
    def __init__(self):
        print("Tank created")
        self.team = get_team()
        self.location = get_location()

    def run(self):
        print("Running tank at", self.team, self.location)



my_type = get_type()
my_robot = HQ() if my_type == RobotType.HQ else Gunner() if my_type == RobotType.GUNNER else Tank()

def turn():
    my_robot.run()