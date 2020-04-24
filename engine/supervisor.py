from .container.interfacer import Interfacer
from .game.moderator import Moderator
from .game.team import Team


class Supervisor:
    def __init__(self, filename1, filename2):
        self.code1 = self.read_code(filename1)
        self.code2 = self.read_code(filename2)
        self.moderator = Moderator()
        self.interfacers = []
        self.robot_ids = set()


    def read_code(self, filename):
        file = open(filename, 'r')
        code = file.read().strip()
        return code


    def update_interfacers(self):
        for robot in self.moderator.robots:
            if robot.id in self.robot_ids:
                continue
            code = self.code1 if robot.team == Team.BLUE else self.code2
            interfacer = Interfacer(self.moderator, code, robot, robot.id)
            interfacer.init_code()
            self.interfacers.append(interfacer)
            self.robot_ids.add(robot.id)
            print("Creation")


    def run_turn(self):
        self.update_interfacers()
        to_remove = []
        for interfacer in self.interfacers:
            if interfacer.robot not in self.moderator.robots:
                # The robot died this turn
                to_remove.append(interfacer)
                continue
            interfacer.run()

        for interfacer in to_remove:
            self.interfacers.remove(interfacer)


    def run(self):
        for i in range(10):
            print("Turn", i)
            self.run_turn()
