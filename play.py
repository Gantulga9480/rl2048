from py2048bot import Py2048Bot


g = Py2048Bot(log=True, method='bfs',
              bfs_depth=2, bfs_sim_num=10,
              mcts_depth=6, mcts_sim_num=10)
g.mainloop()
