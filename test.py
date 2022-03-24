import Py2048 as game
from treesearch import TreeSearch, TreeNode
from simulator import Py2048Simulator
import numpy as np
import copy
import random


class BoardNode(TreeNode, game.Board):

    def __init__(self, parent, action) -> None:
        super().__init__(parent, action)

    def __init__(self, parent=None, action=None, ref=None) -> None:
        if parent is not None:
            super().__init__(parent.get())
        else:
            super().__init__(None)
        if ref is not None:
            self.set_all(ref)


class MCTS(TreeSearch):

    def __init__(self,
                 root: BoardNode,
                 executor: game.Engine,
                 target=None,
                 max_depth=0,
                 sim_num=-1) -> None:
        super().__init__(root, executor, target, max_depth)
        self.simulator = Py2048Simulator(sim_num)
        self.depth = 0

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
                    parent.children.append(len(self.buffer) - 1)
                    self.append(BoardNode(parent=parent,
                                          action=action,
                                          ref=self.executor.board))
            self.depth = self.buffer[-1].layer
            return True
        return False

    def backprob(self, node, value):
        while node is not None:
            node.value += value
            node.visit_count += 1
            node = node.parent

    def UCB1(self, N, n, value, C=10):
        return 1_000_000 if n == 0 else (value + C * np.sqrt(np.log(N) / (n)))

    def expand1(self, parent: BoardNode):
        for action in parent.possible_actions:
            if self.executor.move(copy.deepcopy(parent), action):
                self.append(BoardNode(parent=parent,
                                      action=action,
                                      ref=self.executor.board))

    def simulate(self, node: BoardNode):
        return self.simulator.run(node)


class Test(game.Py2048):

    def __init__(self, render: bool = True) -> None:
        super().__init__(render=render)
        root = BoardNode()
        root.visit_count = 1
        root.set_all(self.game_board)
        self.tree = MCTS(root=root, executor=game.Engine(),
                         max_depth=4, sim_num=2)
        self.count = 0
        self.log = False

    def loop_start(self):
        if not self.over:
            if self.count > 2:
                self.count = 0
                # action = random.choice(self.game_board.possible_actions)
                action = self.tree.search()
                if not action:
                    action = random.choice(self.game_board.possible_actions)
                self.LOG(f'Selected action: {action}')
                self.step(action)
                if self.over:
                    self.LOG(f'Final score: {self.game_board.score}')
                else:
                    self.LOG(f'Next moves: {self.game_board.possible_actions}')
                    new_root = BoardNode()
                    new_root.set_all(self.game_board)
                    self.tree.reset(new_root)
            else:
                self.count += 1


t = Test()
t.mainloop()
