class Interfacer:
    def __init__(self, moderator, code, robot):
        self.code_input = None
        self.code_output = None
        self.moderator = moderator
        self.code = code
        self.robot = robot
        self.game_methods = {
            'get_team': self.get_team,
            'get_type': self.get_type,
            'get_health': self.get_health,
            'get_location': self.get_location,
            'sense': self.sense,
            'can_sense_location': self.can_sense_location,
            'sense_location': self.sense_location,
            'move': self.move,
            'create': self.create,
            'attack': self.attack
        }
        self.globals = {
            '__builtins__': __builtins__,
            '__name__': '__main__'
            }

        for key in self.game_methods:
            self.globals['__builtins__'][key] = self.game_methods[key]

        self.locals = {}


    def run(self):
        exec(self.code, self.globals, self.locals)

    # Translation of moderator methods
    
    def get_team(self):
        return self.moderator.get_team(self.robot)

    def get_type(self):
        return self.moderator.get_type(self.robot)

    def get_health(self):
        return self.moderator.get_health(self.robot)

    def get_location(self):
        return self.moderator.get_location(self.robot)

    def sense(self):
        return self.moderator.sense(self.robot)
    
    def can_sense_location(self, location):
        return self.moderator.can_sense_location(self.robot, location)

    def sense_location(self, location):
        return self.moderator.sense_location(self.robot, location)
    
    def move(self, location):
        return self.moderator.move(self.robot, location)
    
    def create(self, robot_type, location):
        return self.moderator.create(self.robot, robot_type, self.robot.team, location)

    def attack(self, location):
        return self.moderator.attack(self.robot, location)

