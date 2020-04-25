from ..game.team import Team
from ..game.robot_type import RobotType
from ..game import constants as GameConstants

# TODO: Don't let troops perform multiple actions

class Interfacer:
    def __init__(self, moderator, code, robot, id):
        self.moderator = moderator
        self.code = code
        self.robot = robot
        self.id = id
        self.locals = {}
        self.globals = {
            '__builtins__': __builtins__.copy(),
            '__name__': '__main__'
            }

        self.game_methods = {
            'get_team': self.get_team,
            'get_type': self.get_type,
            'get_health': self.get_health,
            'get_location': self.get_location,
            'get_cooldown': self.get_cooldown,
            'sense': self.sense,
            'can_sense_location': self.can_sense_location,
            'sense_location': self.sense_location,
            'move': self.move,
            'create': self.create,
            'attack': self.attack
        }

        self.enums = {
            'RobotType': RobotType,
            'Team': Team,
            'GameConstants': GameConstants
        }

        for key in self.game_methods:
            self.globals['__builtins__'][key] = self.game_methods[key]

        for key in self.enums:
            self.globals['__builtins__'][key] = self.enums[key]
        

    def init_code(self):
        exec(self.code, self.globals, self.locals)
        for key in self.locals:
            self.globals[key] = self.locals[key]

    def run(self):
        self.robot.run()
        exec(self.locals['turn'].__code__, self.globals, self.locals)

    # Translation of moderator methods
    
    def get_team(self):
        return self.robot.team

    def get_type(self):
        return self.robot.type

    def get_health(self):
        return self.robot.health

    def get_location(self):
        return self.robot.location
    
    def get_cooldown(self):
        if self.robot.type == RobotType.HQ:
            return self.robot.cooldown
        print(str(self.robot.type) + " has no method 'get_cooldown'")
        raise Exception
        return None

    def sense(self):
        return self.moderator.sense(self.robot)
    
    def can_sense_location(self, location):
        return self.moderator.can_sense_location(self.robot, location)

    def sense_location(self, location):
        return self.moderator.sense_location(self.robot, location)
    
    def move(self, location):
        if not self.robot.moveable:
            print(str(self.robot.type) + " is not moveable")
            raise Exception
            return None
        return self.moderator.move(self.robot, location)
    
    def create(self, robot_type, location):
        if self.robot.type != RobotType.HQ:
            print(str(self.robot.type) + " can't create robots")
            raise Exception
            return None
        return self.moderator.create(self.robot, robot_type, self.robot.team, location)

    def attack(self, location):
        return self.moderator.attack(self.robot, location)

