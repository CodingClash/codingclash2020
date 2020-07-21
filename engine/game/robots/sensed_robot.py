from ..robot_type import RobotType
from ..team_color import TeamColor

class SensedRobot:
    def __init__(self, robot_type: RobotType, team_color: TeamColor, location: tuple, health: int):
        self.type = robot_type
        self.team_color = team_color
        self.location = location
        self.health = health