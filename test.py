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
            sample = self.get()
            if sample.layer != self.max_depth:
                # print(sample.layer)
                self.expand(sample)
            else:
                self.buffer.insert(0, sample)
                break
        return self.select()

    def select(self):
        layer_num = self.buffer[-1].layer
        child_nodes = []
        scores = []
        while True:
            try:
                if self.buffer[-1].layer == self.max_depth:
                    child = self.get()
                    scores.append(self.simulate(child))
                    child_nodes.append(child)
                else:
                    break
            except IndexError:
                break
        if len(scores) > 0:
            # action = child_nodes[np.argmax(scores)].parent_action
            action = child_nodes[np.argmax(scores)].unroll()
            print('Tree traversal:', action)
            return action[0]
        return None

    def expand(self, parent: BoardTree):
        for action in parent.possible_moves:
            if self.executor.move(copy.deepcopy(parent), action):
                new_node = BoardTree(parent, action)
                new_node.set(self.executor.board.get())
                new_node.score = self.executor.board.score
                new_node.possible_moves = parent.possible_moves.copy()
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
        self.tree = MCTS(root=bt, executor=game.Engine(), max_depth=3)

    def loop_start(self):
        if not self.over:
            try:
                action = self.tree.search()
                # action = random.choice(self.game_board.possible_moves)
                self.LOG(f'Selected action: {action}')
                self.step(action)
            except Exception:
                self.over = True
                # self.running = False
            if self.over:
                self.LOG(f'Final score: {self.game_board.score}')
            self.LOG(f'Possible moves: {self.game_board.possible_moves}')
            new_root = BoardTree()
            new_root.set(self.game_board.get())
            new_root.possible_moves = self.game_board.possible_moves.copy()
            new_root.score = self.game_board.score
            self.tree.append(new_root)


t = Test()
t.mainloop()
