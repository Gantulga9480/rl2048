from Py2048 import Py2048, Engine, Board
from treesearch import Node, MonteCarloTreeSearch, BredthFirstSearch
from simulator import Py2048Simulator
import random


__all__ = ['Py2048Bot']


class BoardNode(Node, Board):

    def __init__(self, parent=None, action=None, ref=None) -> None:
        super().__init__(parent, action)
        if parent is not None:
            super(Node, self).__init__(parent.get())
        else:
            super(Node, self).__init__(None)
        super().__init__(parent, action)
        if ref is not None:
            self.set_all(ref)


class MCTS(MonteCarloTreeSearch):

    def __init__(self, root, executor,
                 target=None, max_depth=0, sim_num=-1) -> None:
        super().__init__(root, executor, target, max_depth)
        self.simulator = Py2048Simulator(sim_num)

    def create(self, parent, action):
        return BoardNode(parent=parent, action=action, ref=self.executor.board)


class BFS(BredthFirstSearch):

    def __init__(self, root, executor,
                 target=None, max_depth=0, sim_num=-1) -> None:
        super().__init__(root, executor, target, max_depth)
        self.simulator = Py2048Simulator(sim_num)

    def create(self, parent, action):
        return BoardNode(parent=parent, action=action, ref=self.executor.board)

    def simulate(self, node):
        return self.simulator.run(node)


class Py2048Bot(Py2048):

    def __init__(self, method,
                 mcts_depth=1, mcts_sim_num=-1, bfs_depth=2, bfs_sim_num=-1,
                 render=True, log=False) -> None:
        super().__init__(render=render)
        self.log = log
        self.method = method
        root = BoardNode()
        root.visit_count = 1
        root.set_all(self.game_board)
        self.count = 0
        self.mcts = MCTS(root=root, executor=Engine(),
                         max_depth=mcts_depth, sim_num=mcts_sim_num)
        self.bfs = BFS(root=root, executor=Engine(),
                       max_depth=bfs_depth, sim_num=bfs_sim_num)

    def loop_start(self):
        if not self.over:
            if self.count > 2:
                self.count = 0
                if self.method == 'mcts':
                    action = self.mcts.search()
                elif self.method == 'bfs':
                    action = self.bfs.search()
                else:
                    action = random.choice(self.game_board.possible_actions)
                self.LOG(f'Selected action: {action}')
                self.step(action)
                if self.over:
                    self.LOG(f'Final score: {self.game_board.score}')
                else:
                    self.LOG(f'Next moves: {self.game_board.possible_actions}')
                    new_root = BoardNode()
                    new_root.set_all(self.game_board)
                    if self.method == 'mcts':
                        self.mcts.reset(new_root)
                    elif self.method == 'bfs':
                        self.bfs.reset(new_root)
            else:
                self.count += 1


if __name__ == '__main__':
    t = Py2048Bot(mcts=False, mcts_depth=2, mcts_sim_num=0,
                  bfs=False, bfs_depth=2)
    t.mainloop()
