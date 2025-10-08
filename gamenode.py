from treesearch import Node
from py2048 import Board
from typing import Any


class GameNode(Node):

    """
    Custom Node class for 2048 tree search. Stores game board state for tree
    expansion.
    """

    def __init__(self,
                 state: Board,
                 parent: Node | None,
                 edge: Any = None,
                 value: float = 0,
                 is_leaf: bool = False) -> None:
        """
        Parameters
        ----------
        state : Board
            2048 specific state object
        parent : Node | None
            The parent node of this new node
        edge : Any
            Parent to current child node connection value (default is None)
        value : float
            Value of current state or Node (default is 0)
        is_leaf : bool
            (default is False)
        """
        super().__init__(parent, edge, value, is_leaf)
        self.state = state
