import random
from .team import Team
from .helpers import squares_within_distance
from .robot_type import RobotType
from . import constants as GameConstants
from .robots import Robot, HQ, Gunner, Tank, SensedRobot

class Moderator:
    def __init__(self):
        self.round_count = 1
        self.board_width = GameConstants.BOARD_WIDTH
        self.board_height = GameConstants.BOARD_HEIGHT
        self.board = [[RobotType.NONE for i in range(self.board_height)] for j in range(self.board_width)]
        self.ids = set()
        self.HQs = { 
            Team.RED: self.create_hq(Team.RED),
            Team.BLUE: self.create_hq(Team.BLUE)
        }
        self.robots = [self.HQs[Team.RED], self.HQs[Team.BLUE]]

    
    ## Helper methods

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


    ## Game State methods (player inputs)
    def get_team(self, robot: Robot):
        return robot.team


    def get_type(self, robot: Robot):
        return robot.type


    def get_health(self, robot: Robot):
        return robot.health


    def get_location(self, robot: Robot):
        return robot.location


    def sense(self, robot: Robot):
        sense_range = robot.sense_range
        squares = squares_within_distance(sense_range)
        robot_location = robot.location
        sensed_list = []

        for dx, dy in squares:
            loc = (robot_location[0] + dx, robot_location[1] + dy)
            sensed = self.sense_location(robot, loc)
            if sensed and sensed.type != RobotType.NONE:
                sensed_list.append(sense_location())

        return sensed_list


    def can_sense_location(self, robot: Robot, location: tuple):
        if not self.inbounds(location):
            return False
        return robot.can_sense_location(location)


    def sense_location(self, robot: Robot, location: tuple):
        if not self.can_sense_location(robot, location):
            # The location you are trying to sense is not within your sensor range
            return None
        
        robot = self.get_robot(location)
        sensed = None
        if robot == RobotType.NONE:
            sensed = SensedRobot(RobotType.NONE, None, None, None)
        else:
            sensed = SensedRobot(robot.type, robot.team, robot.location, robot.health)
        
        return sensed


    ## Game Action methods (player outputs)

    """
    Creates a new robot in a specified location.
    Returns the True if the robot moved successfully, otherwise False
    """
    def move(self, robot: Robot, location: tuple) -> bool:
        # TODO: Make this raise exceptions instead of returning False
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
        self.put_robot(hq, location)
        self.ids.add(id)
        return hq
    
    """
    Creates a new robot in a specified location.
    Returns the robot object if the creation is valid, otherwise returns None
    """
    def create(self, robot: Robot, robot_type: RobotType, team: Team, location: tuple) -> Robot or None:
        # TODO: Make this raise exceptions instead of returning None
        # Check if spawn is valid
        if not self.inbounds(location):
            return None
        if self.location_occupied(location):
            return None
        if robot.type != RobotType.HQ:
            return None
        assert(robot == self.HQs[team])
        if not robot.can_spawn_robot(robot_type, location):
            return None

        # Spawn the new robot
        robot = None
        id = random.random()
        if robot_type == RobotType.TANK:
            robot = Tank(id, location, team)
            self.ids.add(id)
        elif robot_type == RobotType.GUNNER:
            robot = Gunner(id, location, team)
            self.ids.add(id)
        else:
            return None
        
        self.put_robot(robot, location)
        self.robots.append(robot)


    """
    Attacks the robot in a specified location.
    Returns True if the attack was possible, else False
    """
    def attack(self, robot: Robot, target_location: tuple) -> bool:
        # TODO: Make this raise exceptions instead of returning None
        # Check if the attack is valid
        if not self.inbounds(target_location):
            # Given location not on map
            return False
        if not robot.attackable:
            # This robot can't attack
            return False
        target_robot = self.get_robot(target_location)
        if target_robot == RobotType.NONE:
            # Enemy robot not found at given location
            return False
        if target_robot.team == robot.team:
            # Can't attack teammate
            return False
        
        # Actually attack
        target_robot.health -= robot.damage
        if target_robot.health <= 0:
            self.kill(target_robot)


    """
    Wipes a robot out of existence
    """
    def kill(self, robot: Robot):
        try:
            self.robots.remove(robot)
        except:
            print("Robot that you're trying to kill not found: " + str(robot.id))
            return
        location = robot.location
        self.remove_robot(location)

