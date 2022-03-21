from collections import deque
from itertools import zip_longest


class dummy:

    def __init__(self, iteration=None, parent=None, parent_action=None) -> None:
        self.iteration = iteration
        self.parent = parent
        self.actions = ['1', '2']
        self.parent_action = parent_action
        self.depth = 0
        if parent is not None:
            self.depth = parent.depth + 1


class tree:

    def __init__(self, executer: dummy) -> None:
        self.buff = deque()
        self.target = '121122212121212'
        self.buff.append(executer)

    def expand(self, node: dummy):
        for action in node.actions:
            self.buff.append(self.create_child(node, action))

    def create_child(self, parent: dummy, action):
        return dummy(parent=parent, iteration=parent.iteration + action, parent_action=action)

    def search(self):
        while True:
            sample = self.buff.popleft()
            if sample.iteration == self.target or sample.depth == len(self.target)+1:
                return sample
            else:
                self.expand(sample)


d = dummy(iteration='', parent_action='')
t = tree(executer=d)
solution = t.search()
path, actions = solution.unroll()
for iter, act in zip_longest(path, actions):
    print(iter, act)

print('solution depth: ', solution.depth)
