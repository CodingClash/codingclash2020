from engine.supervisor import Supervisor

game = Supervisor("example/example1/bot.py", "example/example1/bot.py")
#game = Supervisor("example/example1/bot.py", "example/example2/bot.py")
game.run_turn()
game.run()
