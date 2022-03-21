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

    def expand(self):
        raise NotImplementedError

    def search(self):
        raise NotImplementedError

    def unroll(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class BredthFirstSearch(TreeSearch):

    def __init__(self,
                 root: Any,
                 executor: object,
                 target: Any = None,
                 max_depth: int = 0) -> None:
        super().__init__(root, executor, target, max_depth)

    def get(self):
        return self.buffer.popleft()

    def append(self, node):
        self.buffer.append(node)
