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
            'get_team': lambda : self.get_team(),
            'get_type': lambda : self.get_type(),
            'get_health': lambda : self.get_health(),
            'get_location': lambda : self.get_location(),
            'get_oil': lambda : self.get_oil(),
            'sense': lambda : self.sense(),
            'can_sense_location': lambda loc : self.can_sense_location(loc),
            'sense_location': lambda loc : self.sense_location(loc),
            'move': lambda loc : self.move(loc),
            'create': lambda robot_type, loc : self.create(robot_type, loc),
            'attack': lambda loc : self.attack(loc),
            'stun': lambda loc: self.stun(loc),
            'get_blockchain': lambda round_num : self.get_blockchain(round_num),
            'add_to_blockchain': lambda data : self.add_to_blockchain(data),
            'dlog': lambda msg : self.dlog(msg)
        }

        self.enums = {
            'RobotType': RobotType,
            'Team': Team,
            'GameConstants': GameConstants
        }

        self.disallowed_enums = ['print']

        for key in self.disallowed_enums:
            del self.globals['__builtins__'][key]

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

    ## Translation of moderator methods
    
    # Basic getter methods

    def get_team(self):
        return self.robot.team

    def get_type(self):
        return self.robot.type

    def get_health(self):
        return self.robot.health

    def get_location(self):
        return self.robot.location
    
    def get_oil(self):
        return self.robot.team.oil

    # Sensing

    def sense(self):
        return self.moderator.sense(self.robot)

    def can_sense_location(self, location):
        return self.moderator.can_sense_location(self.robot, location)

    def sense_location(self, location):
        return self.moderator.sense_location(self.robot, location)

    # Creating robots

    def create(self, robot_type, location):
        return self.moderator.create(self.robot, robot_type, self.robot.team, location)

    # Robot actions (can only do one per turn)

    def move(self, location):
        return self.moderator.move(self.robot, location)
    
    def attack(self, location):
        return self.moderator.attack(self.robot, location)
    
    def stun(self, location):
        return self.moderator.stun(self.robot, location)

    # Blockchain

    def add_to_blockchain(self, data):
        return self.moderator.add_to_blockchain(self.robot, data)

    def get_blockchain(self, round_num):
        return self.moderator.get_blockchain(self.robot, round_num)

    # Logging

    def dlog(self, message):
        self.moderator.dlog(self.robot, message)

