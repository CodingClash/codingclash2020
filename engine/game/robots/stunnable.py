from ..helpers import dist
from .robot import Robot

class Stunnable(Robot):
    def __init__(self, stun_turns, stun_range, stun_cost, stun_aoe):
        self.stunnable = True
        self.stun_turns = stun_turns
        self.stun_range = stun_range
        self.stun_cost = stun_cost
        self.stun_aoe = stun_aoe


    def run(self):
        pass


    def can_stun(self, target_robots):
        if not self.can_perform_action():
            return []
        if self.attacked or self.moved or self.spawned:
            return []
        if self.team.oil < self.stun_cost:
            return []
        filtered = []
        for target in target_robots:
            if dist(self.location, target.loc) <= self.stun_range:
                filtered.append(target)
        return filtered


    def stun(self):
        self.team.oil -= self.stun_cost
        self.attacked = True
