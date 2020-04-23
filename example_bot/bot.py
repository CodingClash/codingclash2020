from stubs import get_team, get_type, get_id, RobotType

class HQ:
	def __init__(self):
		self.type = RobotType.HQ

	def run(self):
		print("Running HQ")

class Gunner:
	def __init__(self):
		self.type = RobotType.GUNNER

	def run(self):
		print("Running gunner")

class Tank:
	def __init__(self):
		self.type = RobotType.TANK
	
	def run(self):
		print("Running tank")


robot = None
if get_type() == RobotType.HQ:
	robot = HQ()
elif get_type() == RobotType.GUNNER:
	robot = HQ()
elif get_type() == RobotType.TANK:
	robot = HQ()

## This method is required!
def run():
	robot.run()