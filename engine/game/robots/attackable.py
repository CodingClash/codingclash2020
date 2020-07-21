from ..helpers import dist
from .robot import Robot

class Attackable(Robot):
    def __init__(self, damage, attack_range, attack_cost):
        self.attackable = True
        self.damage = damage
        self.attack_range = attack_range
        self.attack_cost = attack_range


    def run(self):
        pass


    def can_attack(self, target_location):
        if not self.can_perform_action():
            return False
        if self.attacked or self.moved or self.spawned:
            return False
        if dist(self.location, target_location) > self.attack_range:
            return False
        return self.team.oil >= self.attack_cost


    def attack(self, target_location):
        self.team.oil -= self.attack_cost
        self.attacked = True
