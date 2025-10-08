from py2048 import Py2048, Board, UP, DOWN, LEFT, RIGHT
from treesearch import Node, BredthFirstSearch
from gamenode import GameNode


class GameTree(BredthFirstSearch):

    """
    Custom BredthFirstSearch class for doing 2048 specific tree expansion
    """

    def __init__(self, max_depth: int = 1) -> None:
        """
        Parameters
        ----------
        max_depth : int
            Maximum tree depth to reach
        """
        super().__init__(max_depth)

    def expand(self, node: Node) -> bool:
        is_expanded = False
        if not isinstance(node, GameNode):
            return is_expanded
        # Try to expand tree by executing all possible actions
        for action in [UP, DOWN, LEFT, RIGHT]:
            # Copy parent node state to childe node (2048 specific)
            childe_state = Board(node.state.size)
            childe_state.set_all(node.state)
            # Execute current action on childe node state and observe next state (2048 specific)
            is_moved = childe_state.move(action)
            if is_moved:
                # if moved expand tree by inserting new node to current parent node
                self.append(GameNode(childe_state, node, action, childe_state.score, False))
                is_expanded = True
        # Must return boolean flag indicating tree expansion
        return is_expanded


class Py2048BFS(Py2048):

    def __init__(self, board_size, max_tree_depth) -> None:
        super().__init__(board_size)
        self.tree = GameTree(max_tree_depth)

    def loop(self):
        res = self.tree.search(GameNode(self.board, None, None, self.board.score, False))
        if res is not None:
            actions, score = res
            self.step(actions[0])


if __name__ == '__main__':
    Py2048BFS(4, 5).loop_forever()
