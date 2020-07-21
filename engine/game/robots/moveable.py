from ..helpers import dist
from .robot import Robot

class Moveable(Robot):
    def __init__(self, speed):
        self.moveable = True
        self.speed = speed


    def run(self):
        pass


    def can_move(self, target_location):
        if not self.can_perform_action():
            return False
        if self.attacked or self.moved or self.spawned:
            return False
        if dist(self.location, target_location) > self.speed:
            return False
        return True


    def move(self, target_location):
        self.location = target_location
        self.moved = True
