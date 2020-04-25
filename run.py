from engine.supervisor import Supervisor
from engine.visualizer.visualizer import Visualizer

game = Supervisor("example/ayush/bot.py", "example/gunsblazin/bot.py")
#game = Supervisor("example/example1/bot.py", "example/example2/bot.py")

vis = Visualizer()
game.run_visualized(vis, max_rounds=200, delay=0.2)
#game.run(max_rounds=200)