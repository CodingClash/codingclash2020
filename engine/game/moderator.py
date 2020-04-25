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
        self.game_over = False
        self.winner = None

    
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

    def sense(self, robot: Robot):
        sense_range = robot.sense_range
        squares = squares_within_distance(sense_range)
        robot_location = robot.location
        sensed_list = []

        for dx, dy in squares:
            loc = (robot_location[0] + dx, robot_location[1] + dy)
            sensed = self.sense_location(robot, loc)
            if sensed and sensed.type != RobotType.NONE:
                sensed_list.append(sensed)

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
        if not robot.moveable:
            raise Exception("Robot of type {} is not moveable".format(robot.type))
        if robot.performed_action:
            raise Exception("This robot already performed an action")
        if not self.inbounds(location):
            raise Exception("Given location of {} is not inbounds".format(location))
        if self.get_robot(location) != RobotType.NONE:
            raise Exception("Robot is present at {} location".format(location))
        curr_location = robot.location
        if robot.move(location):
            robot.performed_action = True
            self.put_robot(robot, location)
            self.remove_robot(curr_location)
            return True
    

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
    def create(self, robot: Robot, robot_type: RobotType, team: Team, location: tuple) -> bool:
        if not self.inbounds(location):
            raise Exception("Target creation location of {} is not inbounds".format(location))
        if self.location_occupied(location):
            raise Exception("Target creation location of {} is occupied".format(location))
        if robot.type != RobotType.HQ:
            raise Exception("Robot of type {} can't create other robots".format(robot_type))
        assert(robot == self.HQs[team])
        if not robot.can_spawn_robot(robot_type, location):
            raise Exception("Some other reason")

        # Spawn the new robot
        new_robot = None
        id = random.random()
        if robot_type == RobotType.TANK:
            new_robot = Tank(id, location, team)
        elif robot_type == RobotType.GUNNER:
            new_robot = Gunner(id, location, team)
        else:
            raise Exception("Tryna create an unknown robot type")
        
        self.ids.add(id)
        self.put_robot(new_robot, location)
        self.robots.append(new_robot)
        robot.spawn(robot_type)
        return True


    """
    Attacks the robot in a specified location.
    Returns True if the attack was possible, else False
    """
    def attack(self, robot: Robot, target_location: tuple) -> bool:
        if not self.inbounds(target_location):
            raise Exception("Target attack location of {} is not on the map".format(target_location))
        if not robot.attackable:
            raise Exception("Robot of type {} can't attack".format(robot.type))
        if robot.performed_action:
            raise Exception("This robot already performed an action")
        target_robot = self.get_robot(target_location)
        if target_robot == RobotType.NONE:
            raise Exception("Enemy robot not found at {}".format(target_location))
        if target_robot.team == robot.team:
            raise Exception("Can't attack teammate at {}".format(target_location))
        
        # Actually attack
        robot.performed_action = True
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
        if robot.type == RobotType.HQ:
            self.game_over = True
            self.winner = Team.RED if robot.team == Team.BLUE else Team.BLUE
        location = robot.location
        self.remove_robot(location)

