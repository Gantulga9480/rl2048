from py2048bot import Py2048Bot, Py2048


g = Py2048Bot(log=False, method='bfs',
              bfs_depth=2, bfs_sim_num=5,
              mcts_depth=3, mcts_sim_num=20)
g.mainloop()
