from engine.supervisor import Supervisor
from engine.visualizer.visualizer import Visualizer

game = Supervisor("example/ayush/bot.py", "example/ayush/bot.py")
#game = Supervisor("example/example1/bot.py", "example/example2/bot.py")

vis = Visualizer()
#game.run_visualized(vis)
game.run()