from py2048 import Py2048, Board, UP, DOWN, LEFT, RIGHT
from treesearch import Node, MonteCarloSearch
from gamenode import GameNode
import random
from graphviz import Digraph


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

    def expand(self, node: Node) -> list[GameNode] | None:
        if not isinstance(node, GameNode):
            return None
        new_nodes = []
        while node.available_actions:
            # Try to expand tree by executing one possible actions
            action = node.available_actions.pop()
            # Copy parent node state to childe node (2048 specific)
            childe_state = Board(node.state.size)
            childe_state.set_all(node.state)
            # Execute current action on childe node state and observe next state (2048 specific)
            if childe_state.move(action):
                # if successful create new node
                new_nodes.append(GameNode(childe_state, node, action, childe_state.score, not childe_state.available()))
        return new_nodes

    def visualize_tree(self, root: Node, filename="mcts_tree"):
        dot = Digraph(comment="MCTS Tree")
        dot.attr('node', shape='circle', fontsize='10')

        def add_nodes_edges(node: Node, depth=0):
            # create label for node
            label = f"V={(node.value):.0f}\nN={node.visit_count}\nD={depth}"
            label += f"\nA={node.edge}"

            # add node
            dot.node(str(id(node)), label)

            # add edges recursively
            if node.has_child:
                for child in node.children:
                    dot.edge(str(id(node)), str(id(child)))
                    add_nodes_edges(child, depth + 1)

        add_nodes_edges(root)
        dot.render(filename, view=False, format='png')


class Py2048MCS(Py2048):

    def __init__(self, board_size, max_tree_depth) -> None:
        super().__init__(board_size)
        self.tree = GameTree(max_tree_depth, 0)

    def loop(self):
        if not self.over:
            root_node = GameNode(self.board, None, None, self.board.score, not self.board.available())
            res = self.tree.search(root_node)
            self.tree.visualize_tree(root_node)
            if res:
                action, score = res
                self.step(action)
            # self.over = True


if __name__ == '__main__':
    Py2048MCS(4, 100).loop_forever()
