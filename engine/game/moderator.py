import random
from .team import Team
from .team_color import TeamColor
from .helpers import squares_within_distance
from .robot_type import RobotType
from . import constants as GameConstants
from .robots import Robot, HQ, Refinery, Barracks, Turret, Builder, Gunner, Tank, Grenader, SensedRobot

ROBOT_MAP = {
    RobotType.REFINERY: Refinery,
    RobotType.BARRACKS: Barracks,
    RobotType.TURRET: Turret,
    RobotType.BUILDER: Builder,
    RobotType.GUNNER: Gunner,
    RobotType.TANK: Tank,
    RobotType.GRENADER: Grenader,
}


class Moderator:
    def __init__(self):
        self.board_width = GameConstants.BOARD_WIDTH
        self.board_height = GameConstants.BOARD_HEIGHT
        self.board = [[RobotType.NONE for i in range(self.board_height)] for j in range(self.board_width)]
        self.ids = set()
        self.red, self.blue = Team(TeamColor.RED), Team(TeamColor.BLUE)
        self.HQs = { 
            TeamColor.RED: self.create_hq(self.red),
            TeamColor.BLUE: self.create_hq(self.blue)
        }
        self.robots = [self.HQs[TeamColor.RED], self.HQs[TeamColor.BLUE]]
        self.game_over = False
        self.winner = None
        self.debug, self.info = [], []
        self.ledger = []
        self.round_num = 0


    def update_info(self):
        for robot in self.robots:
            # Format: [INFO] [ID] X Y HEALTH
            self.info.append("[INFO] [{}] {} {} {}".format(robot.id, robot.location[0], robot.location[1], robot.health))
        if self.ledger:
            self.info.append("[BCHAIN] {}".format(';'.join([str(i) for i in self.ledger[-1]])))


    def start_next_round(self):
        self.ledger.append([])

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

    def dlog(self, robot: Robot, message: str):
        self.debug.append("[DLOG] [{}] {}".format(robot.id, message))


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
            sensed = SensedRobot(robot.type, robot.team.color, robot.location, robot.health)
        return sensed


    def in_between(self, pointa, pointb, pointc):
        dx = pointb[0]-pointa[0]
        dy = pointb[1]-pointa[1]

        ranx = sorted([pointa[0], pointb[0]])
        rany = sorted([pointa[1], pointb[1]])

        if not (ranx[0]<pointc[0]<ranx[1] and rany[0]<pointc[1]<rany[1]): return False

        linex = lambda x: pointa[1]+dy/dx*(x-pointa[0])

        if dx == 0:
            r = sorted([pointa[1], pointb[1]])
            if pointc[0]==pointa[0] and r[0]<pointc[1]<r[1]: return True

        elif (linex(pointc[0])<=pointc[1] and linex(pointc[0])+1>pointc[1]) or (linex(pointc[0])>=pointc[1] and linex(pointc[0])+1<pointc[1]):
                return True

        return False

    ## Game Action methods (player outputs)

    """
    Creates a new robot in a specified location.
    Returns the True if the robot moved successfully, otherwise False
    """
    def move(self, robot: Robot, location: tuple) -> bool:
        if not robot.moveable:
            raise Exception("Robot of type {} is not moveable".format(robot.type))
        if self.get_robot(location) != RobotType.NONE:
            raise Exception("Robot is present at {} location".format(location))
        if not self.inbounds(location):
            raise Exception("Given location of {} is not inbounds".format(location))
        if not robot.can_move(location):
            raise Exception("Can't move to {} for some other reason".format(location))
        curr_location = robot.location
        robot.move(location)
        self.put_robot(robot, location)
        self.remove_robot(curr_location)
        return True
    

    def create_hq(self, team: Team) -> HQ:
        id = random.random()
        if team.color == TeamColor.RED:
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
        if not robot.can_spawn_robot(robot_type, location):
            raise Exception("Some other reason as to why you can't spawn {} at {}".format(robot_type, location))

        robot.spawn(robot_type)
        # Spawn the new robot
        assert(robot_type in ROBOT_MAP)
        new_robot_type = ROBOT_MAP[robot_type]
        id = random.random()
        new_robot = new_robot_type(id, location, team)
        
        self.ids.add(id)
        self.put_robot(new_robot, location)
        if new_robot.type != RobotType.WALL:
            self.robots.append(new_robot)
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

        target_robots = []
        squares = squares_within_distance(robot.attack_aoe)
        for dx, dy in squares:
            loc = (target_location[0] + dx, target_location[1] + dy)
            worked = True
            target_robot = self.get_robot(loc)
            if target_robot == RobotType.NONE:
                worked = False
            if target_robot.team.color == robot.team.color:
                worked = False
            for i in self.sense(robot):
                if i.team.color != robot.team.color and self.in_between(robot.location, loc, i.location):
                    worked = False
            if worked:
                target_robots.append(target_robot)
        filtered = robot.can_attack(target_robots):
        if not filtered:
            raise Exception("No valid enemy robots to attack around that location {}".format(target_location))
        
        # Actually attack
        robot.attack()
        for target_robot in filtered:
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
            raise Exception("Robot that you're trying to kill not found: " + str(robot.id))
        if robot.type == RobotType.HQ:
            self.game_over = True
            #print("Killed", robot.team)
            self.winner = TeamColor.RED if robot.team.color == TeamColor.BLUE else TeamColor.BLUE
        location = robot.location
        self.remove_robot(location)


    """
    Adds message to blockchain board
    @param data: a list of length 5 w/ bytes (ints from 0 to 255) 
    """
    def add_to_blockchain(self, robot: Robot, data: list):
        if robot.added_blockchain:
            raise Exception("Robot can only add to blockchain once per round")
        if not isinstance(data, list) or not isinstance(data[0], int) or len(data) != GameConstants.BLOCKCHAIN_BYTE_COUNT:
            raise Exception("Blockchain requires a list of ints of length {}".format(GameConstants.BLOCKCHAIN_BYTE_COUNT))
        for byt in data:
            if byt > GameConstants.BLOCKCHAIN_MAX_NUM_SIZE or byt < GameConstants.BLOCKCHAIN_MIN_NUM_SIZE:
                raise Exception("Blockchain ints must be between {} and {}, but received int of {}".format(GameConstants.BLOCKCHAIN_MIN_NUM_SIZE, GameConstants.BLOCKCHAIN_MAX_NUM_SIZE, byt))
        
        self.ledger[-1].append(data)
    
    
    def get_blockchain(self, robot: Robot, round_num: int):
        if round_num < 0:
            raise Exception("There's no blockchain prior to the first round")
        if round_num >= len(self.ledger) - 1:
            raise Exception("Round {} has not finished yet".format(round_num))
        return self.ledger[round_num].copy()
