from typing import Any
from collections import deque


class TreeSearch:

    def __init__(self,
                 root: Any,
                 executor: object,
                 target: Any = None,
                 max_depth: int = 0) -> None:
        self.root = root
        self.executor = executor
        self.target = target
        self.max_depth = max_depth
        self.buffer = deque()
        self.buffer.append(self.root)

    def search(self):
        raise NotImplementedError

    def expand(self):
        raise NotImplementedError

    def unroll(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def append(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def get_layer(self):
        raise NotImplementedError


class BredthFirstSearch(TreeSearch):

    def __init__(self,
                 root: Any,
                 executor: object,
                 target: Any = None,
                 max_depth: int = 0) -> None:
        super().__init__(root, executor, target, max_depth)

    def select(self):
        ...

    def get(self):
        try:
            return self.buffer.popleft()
        except IndexError:
            return None

    def append(self, node):
        self.buffer.append(node)

    def reset(self, root=None):
        self.buffer.clear()
        self.root = None
        if root is not None:
            self.root = root
            self.append(self.root)
