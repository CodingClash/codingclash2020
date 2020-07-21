from ..helpers import dist
from .robot import Robot

class Attackable(Robot):
    def __init__(self, damage, attack_range, attack_cost, attack_aoe):
        self.attackable = True
        self.damage = damage
        self.attack_range = attack_range
        self.attack_cost = attack_cost
        self.attack_aoe = attack_aoe


    def run(self):
        pass


    def can_attack(self, target_robots):
        if not self.can_perform_action():
            return []
        if self.attacked or self.moved or self.spawned:
            return []
        if self.team.oil < self.attack_cost:
            return []
        filtered = []
        for target in target_robots:
            if dist(self.location, target.loc) <= self.attack_range:
                filtered.append(target)
        return filtered


    def attack(self):
        self.team.oil -= self.attack_cost
        self.attacked = True
