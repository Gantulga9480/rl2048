import numpy as np
from typing import Any
from collections import deque


class TreeNode:

    def __init__(self, parent, action) -> None:
        self.parent = parent
        self.action = action
        self.value = 0
        self.layer = 0
        self.visit_count = 0
        self.children = []
        if self.parent is not None:
            self.layer = parent.layer + 1

    def unroll(self):
        parents_value = self.score
        parent_action = [self.action]
        parent = self.parent
        while parent is not None:
            parents_value += parent.score
            parent_action.append(parent.action)
            parent = parent.parent
        parent_action.pop()
        parent_action.reverse()
        return parent_action, parents_value

    def has_child(self) -> bool:
        return True if self.children else False


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

    def get_layer(self, level):
        layer = [i
                 for i, node in enumerate(self.buffer)
                 if node.layer == level]
        return layer


class BredthFirstSearch(TreeSearch):

    def __init__(self,
                 root: Any,
                 executor: object,
                 target: Any = None,
                 max_depth: int = 0) -> None:
        super().__init__(root, executor, target, max_depth)

    def search(self):
        while True:
            node = self.get()
            if node is not None:
                if node.layer < self.max_depth:
                    self.expand1(node)
                    continue
                self.append(node)  # put back node to tree
            break
        return self.select1()

    def select(self):
        child_nodes = []
        scores = []
        while True:
            node = self.get()
            if node is not None:
                if node.possible_actions:
                    sim_score = self.simulate(node)
                    total_score = node.unroll()[1] + sim_score
                    scores.append(total_score)
                else:
                    scores.append(0)
                child_nodes.append(node)
                continue
            break
        if scores:
            actions, _ = child_nodes[np.argmax(scores)].unroll()
            return actions[0]
        return None


class MonteCarloTreeSearch(TreeSearch):

    def __init__(self,
                 root: Any,
                 executor: object,
                 target: Any = None,
                 max_depth: int = 0) -> None:
        super().__init__(root, executor, target, max_depth)

    def traverse(self, index=0):
        node = self.buffer[index]
        if node.visit_count == 0:
            sim_result = self.simulate(node)
            self.backprob(node, sim_result)
            return True
        elif node.visit_count != 0:
            if node.has_child():
                selected_node = self.select(index)
                return self.traverse(selected_node)
            elif node.visit_count == 1:  # just simulated
                return self.expand(index)
        return False

    def select(self):
        raise NotImplementedError
