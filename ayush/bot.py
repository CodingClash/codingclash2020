
class Gunner:
    def __init__(self):
        self.team = get_team()
        self.my_hq = [i.location for i in sense() if i.type==RobotType.HQ and i.team==self.team][0]
        self.opp_hq = [BOARD_HEIGHT-self.my_hq[0], BOARD_WIDTH-self.my_hq[1]]



    def run(self):
        attackable = [(distance_2(sense.location, get_location()), e) for e in sense()]
        if len(attackable)>0:
            best = min(attackable)
            if best[0]<=GUNNER_RANGE:
                attack(best[1].location)
                return

        dx = self.opp_hq[0]-self.location[0]
        dy = self.opp_hq[1]-self.location[1]
        options = [(dx, dy), (dx, 0), (0, dy)]
        for i in options:
            if sense_location(i).RobotType==None:
                move(i)
                return


    def distance_2(self, p1, p2):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2


class Tank:
    def __init__(self):
        self.team = get_team()
        self.my_hq = [i.location for i in sense() if i.type==RobotType.HQ and i.team==self.team][0]
        self.opp_hq = [BOARD_HEIGHT-self.my_hq[0], BOARD_WIDTH-self.my_hq[1]]



    def run(self):
        attackable = [(distance_2(sense.location, get_location()), e) for e in sense()]
        if len(attackable)>0:
            best = min(attackable)
            if best[0]<=TANK_RANGE:
                attack(best[1].location)
                return

        dx = self.opp_hq[0]-self.location[0]
        dy = self.opp_hq[1]-self.location[1]
        options = [(dx, dy), (dx, 0), (0, dy)]
        for i in options:
            if sense_location(i).RobotType==None:
                move(i)
                return


    def distance_2(self, p1, p2):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

class HQ:
    def run():
        print("hello")

if get_type()==RobotType.GUNNER: robot = Gunner()
elif get_type()==RobotType.TANK: robot = Tank()
else: robot = HQ()

def turn():
    robot.run()
