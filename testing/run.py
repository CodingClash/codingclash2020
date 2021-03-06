#python run.py example/gunsblazin example/bunsblazin --save timertest.txt
#cd /cygdrive/c/Users/Srikar/Documents/Projects/CodingClash/CodingClash2020
#python3 run.py example/srikar example/srikar --save srikar.txt

import os
import argparse
from codingclash2020.supervisor import Supervisor

parser = argparse.ArgumentParser()
parser.add_argument('folders', nargs='+', help='Folder name of the first bot')
#parser.add_argument('--live', default=False, type=bool, help='Use this tag to view the game live')
#parser.add_argument('--delay', default=0.3, type=int, help='Set the playback delay (only applies if live is True)')
parser.add_argument('--max-rounds', default=200, type=int, help='Set the maximum round number')
parser.add_argument('--save', default=None, type=str, help='Save the replay')
args = parser.parse_args()

filename1 = os.path.join(args.folders[0], "bot.py")
filename2 = os.path.join(args.folders[1], "bot.py")

print(filename1)

game = Supervisor(filename1, filename2)
#game = Supervisor("example/example1/bot.py", "example/example2/bot.py")

game.run(max_rounds=args.max_rounds)

if args.save:
    replay = game.get_replay()
    with open(args.save, "w+") as file:
        file.write("\n".join(replay))
    print("Saved")
