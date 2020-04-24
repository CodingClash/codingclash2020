
class Gunner:
    def run():
        attackable = [(distance_2(sense.location, get_location()), e) for e in sense()]
        if len(attackable)>0:
            best = min(attackable)
            if best[0]<=GUNNER_RANGE:
                attack(best[1].location)
                return
        

    def distance_2((r1, c1), (r2, c2)):
        return (r1-r2)**2 + (c1-c2)**2


class Tank:
    def run():
        print("hello")

class HQ:
    def run():
        print("hello")

if get_type()==RobotType.GUNNER: robot = Gunner()
elif get_type()==RobotType.TANK: robot = Tank()
else: robot = HQ()

def turn():
    robot.run()
