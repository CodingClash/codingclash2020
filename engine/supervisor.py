# Local imports
from .game.team import Team
from .game.moderator import Moderator
from .game.robot_type import RobotType
from .container.interfacer import Interfacer
from .game import constants as GameConstants

# Imports used for setting time limit on method
import signal
from contextlib import contextmanager

# Exception when time limit is exceeded
class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
#    signal.alarm(seconds)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class Supervisor:
    def __init__(self, filename1, filename2):
        self.filename1 = filename1
        self.filename2 = filename2
        self.code1 = self.read_code(filename1)
        self.code2 = self.read_code(filename2)
        self.moderator = Moderator()
        self.interfacers = []
        self.robot_ids = set()
        # Used for visualization
        self.robot_to_str = {(Team.RED, RobotType.GUNNER): "G", (Team.RED, RobotType.TANK): "T", (Team.RED, RobotType.HQ): "H",
							       (Team.BLUE, RobotType.GUNNER): "g", (Team.BLUE, RobotType.TANK): "t", (Team.BLUE, RobotType.HQ): "h",
								   RobotType.NONE: "n"}
        self.boards = []


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

    
    def run_turn(self):
        self.update_interfacers()
        to_remove = []
        for interfacer in self.interfacers:
            if interfacer.robot not in self.moderator.robots:
                # The robot died this turn
                to_remove.append(interfacer)
                continue
            try:
                with time_limit(GameConstants.TIME_LIMIT):
                    interfacer.run()
            except Exception as e:
                error_str = "[ERROR] [{}] [{}] [{}]: {}".format(interfacer.robot.id, interfacer.robot.team, interfacer.robot.type, e)
                print(error_str)
                self.errors.append(error_str)
            signal.alarm(0)

            if self.moderator.game_over:
                break

        for interfacer in to_remove:
            self.interfacers.remove(interfacer)


    def run(self, max_rounds):
        self.boards = [[row.copy() for row in self.moderator.board]]
        self.moderator.update_info()
        self.comments = {0: self.moderator.info + self.moderator.debug.copy()}
        self.errors = []
        for i in range(max_rounds):
            print("Turn", i)
            self.moderator.debug, self.moderator.info, self.errors = [], [], []
            self.moderator.start_next_round()
            self.run_turn()
            self.moderator.update_info()
            self.comments[i + 1] = self.moderator.info + self.moderator.debug.copy() + self.errors
            self.boards.append([row.copy() for row in self.moderator.board])
            if self.moderator.game_over:
                break
        print("Winner: {}".format(self.filename1 if self.moderator.winner == Team.BLUE else self.filename2))

    
    def get_replayable_board(self, moderator_board):
        board = []
        for row in moderator_board:
            temp = []
            for robot in row:
                piece = self.robot_to_str[RobotType.NONE]
                if robot != RobotType.NONE:
                    piece = self.robot_to_str[(robot.team, robot.type)]
                temp.append(piece)
            board.append(temp)
        return board


    def board_to_string(self, board):
        bout = [j for sub in board for j in sub]
        return "#"+"".join(bout)


    def save(self, filename):
        #print(self.boards)
        data = []
        for i, board in enumerate(self.boards):
            data.append(self.board_to_string(self.get_replayable_board(board)))
            if i in self.comments:
                for comment in self.comments[i]:
                    data.append(comment)

        with open(filename, "w+") as file:
            file.write("|blue: {}\n".format(self.filename1))
            file.write("|red: {}\n".format(self.filename2))
            file.write("\n".join(data))
            file.write("\n|Winner: {}".format(self.filename1 if self.moderator.winner == Team.BLUE else self.filename2))
            file.write("\n|Winner color: {}".format("blue" if self.moderator.winner == Team.BLUE else "red"))
