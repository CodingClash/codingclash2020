from .container.code_container import CodeContainer
from .game.moderator import Moderator

class Supervisor:
    def __init__(self, filename1, filename2):
        self.container1 = CodeContainer(filename1)
        self.contianer2 = CodeContainer(filename2)
        self.moderator = Moderator()
    

    def run(self):
        print("HI")

