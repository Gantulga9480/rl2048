from py2048bot import Py2048Bot
from deep2048bot import Deep2048Bot
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--rl', action='store_true')
args = parser.parse_args()

if args.rl:
    g = Deep2048Bot()
else:
    g = Py2048Bot(log=True, method='bfs',
                  bfs_depth=3, bfs_sim_num=5,
                  mcts_depth=6, mcts_sim_num=10)
g.mainloop()
