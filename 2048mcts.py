from py2048 import Py2048, Board, UP, DOWN, LEFT, RIGHT
from treesearch import Node, MonteCarloSearch
from gamenode import GameNode
import random


class GameSimulator:

    """
    Custom class for doing 2048 specific tree simulation
    """

    def __init__(self) -> None:
        self.over = False
        self.game_board = Board(4)

    def run(self, board: Board):
        self.over = False
        self.game_board.set(board.get())
        self.game_board.score = 0
        while not self.over:
            move = random.choice([UP, DOWN, LEFT, RIGHT])
            self.step(move)
        return self.game_board.score

    def step(self, dir):
        self.game_board.move(dir)
        self.over = not self.game_board.available()
        return self.over


class GameTree(MonteCarloSearch):

    """
    Custom class for doing 2048 specific tree expansion
    """

    def __init__(self, num_iters: int = 1, c: float = 1) -> None:
        super().__init__(num_iters, c)
        self.sim = GameSimulator()

    def simulate(self, node: Node) -> float:
        if not isinstance(node, GameNode):
            return 0
        return self.sim.run(node.state)

    def expand(self, node: Node) -> GameNode | None:
        if not isinstance(node, GameNode):
            return None
        while node.available_actions:
            # Try to expand tree by executing one possible actions
            action = node.available_actions.pop()
            # Copy parent node state to childe node (2048 specific)
            childe_state = Board(node.state.size)
            childe_state.set_all(node.state)
            # Execute current action on childe node state and observe next state (2048 specific)
            if childe_state.move(action):
                # if successful create new node
                return GameNode(childe_state, node, action, 0, not childe_state.available())
        return None


class Py2048BFS(Py2048):

    def __init__(self, board_size, max_tree_depth) -> None:
        super().__init__(board_size)
        self.tree = GameTree(max_tree_depth, 5)

    def loop(self):
        if not self.over:
            res = self.tree.search(
                GameNode(self.board, None, None, 0, not self.board.available())
            )
            if res:
                action, score = res
                self.step(action)


if __name__ == '__main__':
    Py2048BFS(4, 1000).loop_forever()
