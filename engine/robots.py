from robot_type import RobotType
import constants as GameConstants

class Robot:
    def __init__(self, id, location, team):
        self.id = id
        self.location = location
        self.id = team
    
    def run(self):
        pass


class HQ(Robot):
    def __init__(self, id, location, team):
        super.__init__(id, location, team)
        self.cooldown = 0
        self.type = RobotType.HQ
        self.moveable = False
    
    def run(self):
        self.cooldown -= GameConstants.HQ_COOLDOWN_REDUCTION
        if self.cooldown < 0:
            self.cooldown = 0

    def can_spawn_robot(self, robot_type, location):
        #TODO: Take robot location into consideration
        return self.cooldown == 0
    


class Moveable(Robot):
    def __init__(self, id, location, team):
        super.__init__(id, location, team)
        self.moveable = True
    
    def dist(self, loc1, loc2):
        return (loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1])

    def move(self, target_location):
        if self.dist(self.location, target_location) > self.range:
            return False
        self.location = target_location
        return True


class Gunner(Moveable):
    def __init__(self, id, location, team):
        super.__init__(id, location, team)
        self.health = GameConstants.GUNNER_HEALTH
        self.damage = GameConstants.GUNNER_DAMAGE
        self.movement_speed = GameConstants.GUNNER_MOVEMENT_SPEED
        self.range = GameConstants.GUNNER_RANGE


class Tank(Moveable):
    def __init__(self, id):
        super.__init__(id)
        self.health = GameConstants.GUNNER_HEALTH
        self.damage = GameConstants.GUNNER_DAMAGE
        self.movement_speed = GameConstants.GUNNER_MOVEMENT_SPEED
        self.range = GameConstants.GUNNER_RANGE
