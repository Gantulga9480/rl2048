import numpy as np
import random
import copy
from collections import deque


class Node:

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
                 root,
                 executor: object,
                 target=None,
                 max_depth: int = 0) -> None:
        self.root = root
        self.executor = executor
        self.target = target
        self.max_depth = max_depth
        self.depth = 0
        self.buffer = deque()
        self.buffer.append(self.root)

    def search(self):
        raise NotImplementedError

    def expand(self):
        raise NotImplementedError

    def create(self, parent, action):
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
                 root,
                 executor: object,
                 target=None,
                 max_depth: int = 0) -> None:
        super().__init__(root, executor, target, max_depth)
        self.simulator = None

    def search(self):
        while True:
            node = self.get()
            if node is not None:
                if node.layer < self.max_depth:
                    self.expand(node)
                    continue
                self.append(node)  # put back node to tree
            break
        return self.select()

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

    def expand(self, parent):
        for action in parent.possible_actions:
            if self.executor.move(copy.deepcopy(parent), action):
                self.append(self.create(parent, action))

    def simulate(self, node):
        return self.simulator.run(node)


class MonteCarloTreeSearch(TreeSearch):

    def __init__(self,
                 root,
                 executor: object,
                 target=None,
                 max_depth: int = 0) -> None:
        super().__init__(root, executor, target, max_depth)
        self.simulator = None

    def search(self):
        self.depth = 0
        self.expand(0)
        while self.depth < self.max_depth:
            if self.traverse():
                continue
            break
        next_layer = self.get_layer(self.root.layer + 1)
        score = [self.buffer[i].value for i in next_layer]
        best_node = self.buffer[next_layer[np.argmax(score)]]
        return best_node.unroll()[0][0]

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

    def select(self, index):
        node = self.buffer[index]
        children = node.children
        parent_visit = node.visit_count
        scores = []
        for i in children:
            child = self.buffer[i]
            child_visit = child.visit_count
            value = child.value
            ucb_score = self.UCB1(parent_visit, child_visit, value)
            scores.append(ucb_score)
        if scores.count(scores[0]) == len(scores):
            return random.choice(children)
        return children[np.argmax(scores)]

    def expand(self, parent_index):
        parent = self.buffer[parent_index]
        parent.children.clear()
        if parent.possible_actions:
            for action in parent.possible_actions:
                if self.executor.move(copy.deepcopy(parent), action):
                    self.append(self.create(parent, action))
                    parent.children.append(len(self.buffer) - 1)
            self.depth = self.buffer[-1].layer
            return True
        return False

    def simulate(self, node):
        return self.simulator.run(node)

    def backprob(self, node, value):
        while node is not None:
            node.value += value
            node.visit_count += 1
            node = node.parent

    def UCB1(self, N, n, value, C=10):
        return 1_000_000 if n == 0 else (value + C * np.sqrt(np.log(N) / (n)))
