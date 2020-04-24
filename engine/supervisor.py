from .container.interfacer import Interfacer
from .game.moderator import Moderator
from .game.team import Team


class Supervisor:
    def __init__(self, filename1, filename2):
        self.code1 = self.read_code(filename1)
        self.code2 = self.read_code(filename2)
        self.moderator = Moderator()


    def read_code(self, filename):
        file = open(filename, 'r')
        code = file.read().strip()
        return code


    def run_turn(self):
        for robot in self.moderator.robots:
            code = self.code1 if robot.team == Team.BLUE else self.code2
            interfacer = Interfacer(self.moderator, code, robot)
            interfacer.run()

