import math

def dist(loc1, loc2):
    return (loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1])

def squares_within_distance(radius_squared):
    radius = math.ceil(math.sqrt(radius_squared))
    squares = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dist((0,0), (dx, dy)) <= radius_squared:
                squares.append((dx, dy))
    return squares