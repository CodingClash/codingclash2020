from ..helpers import dist
from .robot import Robot

class Spawnable(Robot):
    def __init__(self, max_spawn_count, spawn_costs, spawn_radius):
        self.spawnable = True
        self.max_spawn_count = max_spawn_count
        self.costs = spawn_costs
        self.spawn_radius = spawn_radius
        self.num_spawned = 0


    def run(self):
        self.num_spawned = 0


    def can_spawn(self, robot_type, location):
        if not self.can_perform_action():
            return False
        if self.attacked or self.moved:
            return False
        if self.num_spawned >= self.max_spawn_count:
            return False
        if robot_type not in self.costs:
            return False
        if dist(self.location, location) > self.spawn_radius:
            return False
        return self.team.oil >= self.costs[robot_type]


    def attack(self, robot_type, target_location):
        self.team.oil -= self.costs[robot_type]
        self.spawned = True
        self.num_spawned += 1
