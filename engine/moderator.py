import random
from team import Team
from robot_type import RobotType
import constants as GameConstants
from robots import Robot, HQ, Gunner, Tank

class Moderator:
    def __init__(self):
        self.board = []
        self.board_width = GameConstants.BOARD_WIDTH
        self.board_height = GameConstants.BOARD_HEIGHT
        self.robots = [[RobotType.NONE for i in range(self.board_height)] for j in range(self.board_width)]
        self.HQs = { 
            Team.RED: self.create_hq(Team.RED),
            Team.BLUE: self.create_hq(Team.BLUE)
        }

    
    def get_robot(self, location: tuple):
        return self.board[location[0]][location[1]]


    def put_robot(self, robot: Robot, location: tuple):
        self.board[location[0]][location[1]] = robot


    def remove_robot(self, location: tuple):
        self.board[location[0]][location[1]] = RobotType.NONE


    def inbounds(self, location: tuple):
        return location[0] >= 0 and location[0] < self.board_width and location[1] >= 0 and location[1] < self.board_height


    def location_occupied(self, location: tuple) -> bool:
        if not self.inbounds(location):
            return False
        return self.get_robot(location) != RobotType.NONE


    def move(self, robot: Robot, location: tuple) -> bool:
        if not robot.moveable:
            return False
        if not self.inbounds(location):
            return False
        curr_location = robot.location
        if robot.move(location):
            self.put_robot(robot, location)
            self.remove_robot(curr_location)
            return True
        return False
    

    def create_hq(self, team: Team) -> HQ:
        id = random.random()
        if team == Team.RED:
            location = GameConstants.RED_HQ_LOCATION
        else:
            location = GameConstants.BLUE_HQ_LOCATION
        hq = HQ(id, location, team)
        self.put_robot(location, hq)
        return hq
    
    """
    Creates a new robot in a specified location.
    Returns the robot object if the creation is valid, otherwise returns None
    """
    def create(self, robot_type: RobotType, team: Team, location: tuple) -> Robot or None:
        id = random.random()
        robot = None
        # Check if spawn is valid
        # If so spawn robot, put robot in given location, and set HQ cooldown
        if robot_type == RobotType.TANK:
            robot = Tank()
        elif robot_type == RobotType.GUNNER:
            robot = Gunner()
        else:
            return None


