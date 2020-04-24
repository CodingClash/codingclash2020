from engine.supervisor import Supervisor

game = Supervisor("example/bot.py", "example/bot.py")
game.run_turn()
print("HAI")
game.run_turn()
