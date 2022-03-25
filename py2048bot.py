from Py2048 import Py2048, Engine, Board
from treesearch import Node, MonteCarloTreeSearch, BredthFirstSearch
from simulator import Py2048Simulator
import random


class BoardNode(Node, Board):

    def __init__(self, parent=None, action=None, ref=None) -> None:
        super().__init__(parent, action)
        super(Node, self).__init__(None)
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


class Py2048Bot(Py2048):

    def __init__(self, method=None,
                 mcts_depth=1, mcts_sim_num=-1, bfs_depth=2, bfs_sim_num=-1,
                 render=True, log=False) -> None:
        super().__init__(render=render)
        self.count = 0
        self.log = log
        self.method = method
        root = BoardNode(ref=self.game_board)
        if self.method == 'mcts':
            self.tree = MCTS(root=root, executor=Engine(),
                             max_depth=mcts_depth, sim_num=mcts_sim_num)
        elif self.method == 'bfs':
            self.tree = BFS(root=root, executor=Engine(),
                            max_depth=bfs_depth, sim_num=bfs_sim_num)

    def loop_start(self):
        # if not self.over:
        if self.count > 2:
            self.count = 0
            if self.method:
                action = self.tree.search()
            else:
                action = random.choice(self.game_board.possible_actions)
            self.LOG(f'Selected action: {action}')
            self.step(action)
            self.LOG(f'Next moves: {self.game_board.possible_actions}')
            if self.method:
                self.tree.reset(BoardNode(ref=self.game_board))
            if self.over:
                self.LOG(f'Final score: {self.game_board.score}')
        else:
            self.count += 1


if __name__ == '__main__':
    t = Py2048Bot(mcts=False, mcts_depth=2, mcts_sim_num=0,
                  bfs=False, bfs_depth=2)
    t.mainloop()
