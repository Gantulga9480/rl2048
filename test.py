import Py2048 as game
from treesearch import BredthFirstSearch
from simulator import Py2048Simulator
import numpy as np
import copy
import random


class BoardTree(game.Board):

    def __init__(self, parent=None, action=None) -> None:
        if parent is not None:
            super().__init__(parent.get())
        else:
            super().__init__(None)
        self.parent = parent
        self.parent_action = action
        self.layer = 0
        if self.parent is not None:
            self.layer = parent.layer + 1

    def unroll(self):
        parents_value = [self.score]
        parent_action = [self.parent_action]
        parent = self.parent
        while parent is not None:
            parents_value.append(parent.score)
            parent_action.append(parent.parent_action)
            parent = parent.parent
        parent_action.pop()
        parents_value.pop()
        parents_value.reverse()
        parent_action.reverse()
        return parent_action


class MCTS(BredthFirstSearch):

    def __init__(self,
                 root: BoardTree,
                 executor: game.Engine,
                 target=None,
                 max_depth=0) -> None:
        super().__init__(root, executor, target, max_depth)
        self.simulator = Py2048Simulator()

    def search(self):
        while True:
            node = self.get()
            if node is not None:
                if node.layer < self.max_depth:
                    if node.possible_moves:
                        self.expand(node)
                else:
                    self.buffer.insert(0, node)
                    break
            else:
                break
        return self.select()

    def select(self):
        child_nodes = []
        scores = []
        while True:
            node = self.get()
            if node is not None:
                if node.possible_moves:
                    scores.append(self.simulate(node))
                else:
                    scores.append(0)
                child_nodes.append(node)
            else:
                break
        if scores:
            actions = child_nodes[np.argmax(scores)].unroll()
            print('Tree traversal:', actions)
            return actions
        return None

    def expand(self, parent: BoardTree):
        for action in parent.possible_moves:
            parent_tmp = copy.deepcopy(parent)
            if self.executor.move(parent_tmp, action):
                new_node = BoardTree(parent, action)
                new_node.set_all(parent_tmp)
                self.append(new_node)

    def simulate(self, node: BoardTree):
        return self.simulator.run(node, 10)


class Test(game.Py2048):

    def __init__(self, render: bool = True) -> None:
        super().__init__(render=render)
        self.game_engine.get_possible_moves(self.game_board)
        bt = BoardTree()
        bt.set(self.game_board.get())
        bt.possible_moves = self.game_board.possible_moves.copy()
        self.tree = MCTS(root=bt, executor=game.Engine(), max_depth=1)
        self.actions = []

    def loop_start(self):
        if not self.over:
            # action = random.choice(self.game_board.possible_moves)
            if not self.actions:
                self.actions = self.tree.search()
            if not self.actions:
                action = random.choice(self.game_board.possible_moves)
            action = self.actions.pop(0)
            self.LOG(f'Selected action: {action}')
            self.step(action)
            if self.over:
                self.LOG(f'Final score: {self.game_board.score}')
            else:
                self.LOG(f'Possible moves: {self.game_board.possible_moves}')
                new_root = BoardTree()
                new_root.set_all(self.game_board)
                self.tree.append(new_root)


t = Test()
t.mainloop()
