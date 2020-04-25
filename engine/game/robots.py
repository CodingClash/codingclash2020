from .team import Team
from .helpers import dist
from .robot_type import RobotType
from . import constants as GameConstants

class Robot:
    def __init__(self, id, location, team):
        self.id = id
        self.location = location
        self.team = team
    
    def run(self):
        pass

    def can_sense_location(self, location: tuple):
        return dist(self.location, location) <= self.sense_range


class HQ(Robot):
    def __init__(self, id, location, team):
        super().__init__(id, location, team)
        self.cooldown = 0
        self.type = RobotType.HQ
        self.sense_range = GameConstants.HQ_SENSE_RANGE
        self.moveable = False
        self.attackable = False
        self.health = GameConstants.HQ_HEALTH
    
    def run(self):
        super().run()
        self.cooldown -= GameConstants.HQ_COOLDOWN_REDUCTION
        if self.cooldown < 0:
            self.cooldown = 0

    def can_spawn_robot(self, robot_type, location):
        if dist(self.location, location) > GameConstants.SPAWN_RADIUS:
            return False
        if robot_type not in [RobotType.GUNNER, RobotType.TANK]:
            return False
        return self.cooldown == 0
    
    def spawn(self, robot_type):
        if robot_type == RobotType.GUNNER:
            self.cooldown += GameConstants.GUNNER_SPAWN_COOLDOWN
        if robot_type == RobotType.TANK:
            self.cooldown += GameConstants.TANK_SPAWN_COOLDOWN


class Moveable(Robot):
    def __init__(self, id, location, team):
        super().__init__(id, location, team)
        self.moveable = True
        self.performed_action = False
    
    def run(self):
        super().run()
        self.performed_action = False

    def move(self, target_location):
        if dist(self.location, target_location) > self.movement_speed:
            raise Exception("Robot at {} can't go to {}".format(self.location, target_location))
            return False
        self.location = target_location
        return True


class Gunner(Moveable):
    def __init__(self, id, location, team):
        super().__init__(id, location, team)
        self.type = RobotType.GUNNER
        self.sense_range = GameConstants.GUNNER_SENSE_RANGE
        self.health = GameConstants.GUNNER_HEALTH
        self.damage = GameConstants.GUNNER_DAMAGE
        self.movement_speed = GameConstants.GUNNER_MOVEMENT_SPEED
        self.attack_range = GameConstants.GUNNER_ATTACK_RANGE
        self.attackable = True
    
    def run(self):
        super().run()
        pass


class Tank(Moveable):
    def __init__(self, id, location, team):
        super().__init__(id, location, team)
        self.type = RobotType.TANK
        self.sense_range = GameConstants.TANK_SENSE_RANGE
        self.health = GameConstants.TANK_HEALTH
        self.damage = GameConstants.TANK_DAMAGE
        self.movement_speed = GameConstants.TANK_MOVEMENT_SPEED
        self.attack_range = GameConstants.TANK_ATTACK_RANGE
        self.attackable = True
    
    def run(self):
        super().run()
        pass


class SensedRobot:
    def __init__(self, robot_type: RobotType, team: Team, location: tuple, health: int):
        self.type = robot_type
        self.team = team
        self.location = location
        self.health = health

