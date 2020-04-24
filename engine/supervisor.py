import threading
from .game.team import Team
from .game.moderator import Moderator
from .game.robot_type import RobotType
from .container.interfacer import Interfacer

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


    def run(self, max_rounds=50):
        for i in range(max_rounds):
            print("Turn", i)
            self.run_turn()

    
    def get_visualizable_board(self, moderator_board, visualizer):
        board = []
        for row in moderator_board:
            temp = []
            for robot in row:
                piece = visualizer.robot_to_str[RobotType.NONE]
                if robot != RobotType.NONE:
                    piece = visualizer.robot_to_str[(robot.team, robot.type)]
                temp.append(piece)
            board.append(temp)
        return board


    def run_visualized(self, visualizer, max_rounds=50, delay=0.5):
        self.visualized_boards = [visualizer.copy(self.moderator.board)]
        vis_thread = threading.Thread(target=self.vis_helper, args=(visualizer, delay))
        vis_thread.daemon = True
        vis_thread.start()
        for i in range(max_rounds):
            print("Turn", i)
            self.run_turn()
            self.visualized_boards.append(visualizer.copy(self.moderator.board))
        while True:
            pass



    def vis_helper(self, visualizer, delay):
        idx = 0
        while True:
            print(idx, len(self.visualized_boards))
            if idx >= len(self.visualized_boards):
                continue
            visualized = self.get_visualizable_board(self.visualized_boards[idx], visualizer)
            visualizer.view(visualized, delay)
            idx += 1
