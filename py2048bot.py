from py2048 import Py2048, Board
from treesearch import Node, MonteCarloTreeSearch, BredthFirstSearch
import random


class Py2048Simulator:

    def __init__(self, sim_number) -> None:
        self.over = False
        self.game_board = Board()
        self.sim_number = sim_number
        self.counter = 0

    def run(self, board=None):
        self.counter = 0
        self.over = False
        if board is not None:
            self.game_board.set_all(board)
        while self.counter != self.sim_number and not self.over:
            self.counter += 1
            move = random.choice([0, 1, 2, 3])
            self.step(move)
        return self.scoring()

    def step(self, dir):
        self.game_board.move(self.game_board, dir)
        self.over = not self.game_board.available()
        return not self.over

    def scoring(self):
        final_score = 0
        empty_tile_score = 0
        game_score = self.game_board.score
        final_score = empty_tile_score + game_score
        return final_score


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
                 mcts_depth=1, mcts_sim_num=-1, bfs_depth=2, bfs_sim_num=-1) -> None:
        super().__init__()
        self.count = 0
        self.method = method
        root = BoardNode(ref=self.game_board)
        if self.method == 'mcts':
            self.tree = MCTS(root=root, executor=Engine(),
                             max_depth=mcts_depth, sim_num=mcts_sim_num)
        elif self.method == 'bfs':
            self.tree = BFS(root=root, executor=Engine(),
                            max_depth=bfs_depth, sim_num=bfs_sim_num)

    def loop(self):
        if self.count > 2:
            self.count = 0
            if self.method:
                action = self.tree.search()
            else:
                action = random.choice(self.game_board.possible_actions)
            self.step(action)
            if self.method:
                self.tree.reset(BoardNode(ref=self.game_board))
        else:
            self.count += 1


if __name__ == '__main__':
    t = Py2048Bot(log=True, method='bfs',
                  bfs_depth=2, bfs_sim_num=10,
                  mcts_depth=6, mcts_sim_num=10)
    t.mainloop()
