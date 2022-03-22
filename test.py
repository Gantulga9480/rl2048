import Py2048 as game
from treesearch import BredthFirstSearch
from simulator import Py2048Simulator
import numpy as np
import copy
import random


class BoardTree(game.Board):

    def __init__(self, parent=None, parent_index=0, action=None) -> None:
        if parent is not None:
            super().__init__(parent.get())
        else:
            super().__init__(None)
        self.parent = parent
        self.action = action
        self.parent_index = parent_index
        self.children_indexs = []
        self.visit_count = 0
        self.layer = 0
        self.value = 0
        if self.parent is not None:
            self.layer = parent.layer + 1

    def has_child(self) -> bool:
        print('Child', self.children_indexs)
        if self.children_indexs:
            return True
        else:
            return False

    def unroll(self):
        parents_value = [self.score]
        parent_action = [self.action]
        parent = self.parent
        while parent is not None:
            parents_value.append(parent.score)
            parent_action.append(parent.action)
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
        self.depth = 0

    def search(self):
        while self.depth < self.max_depth:
            print('Depth:', self.depth)
            if not self.traverse(0):  # start from top node
                break
        leaf_layer = self.get_layer(self.depth)
        score = [self.buffer[i].value for i in leaf_layer]
        best_node = self.buffer[leaf_layer[np.argmax(score)]]
        return best_node.unroll()

    def traverse(self, index):
        try:
            print('Traversing on', index)
            node = self.buffer[index]
            print('Visit count', node.visit_count)
            if node.visit_count == 0 and node.layer != 0:
                print('Simulating')
                sim_result = self.simulate(node)
                node.visit_count += 1
                self.backprob(node, sim_result)
                return True
            elif node.has_child() and node.visit_count != 0:
                print('Traversing')
                node.visit_count += 1
                selected_node = self.select(index)
                return self.traverse(selected_node)
            elif not node.has_child() and node.visit_count != 0:
                return False
            else:
                print('Expanding')
                self.expand(node, index)
                node.visit_count += 1
        except IndexError:
            return False

    def select(self, index):
        node = self.buffer[index]
        ind = node.children_indexs
        scores = []
        for i in ind:
            child = self.buffer[i]
            p_N = node.visit_count
            c_n = child.visit_count
            val = child.value
            scores.append(self.UCB1(p_N, c_n, val))
        return ind[np.argmax(scores)]

    def expand(self, parent, parent_index):
        # parent = self.buffer[parent_index]
        parent.children_indexs.clear()
        for action in parent.possible_moves:
            parent_tmp = copy.deepcopy(parent)
            if self.executor.move(parent_tmp, action):
                new_node = BoardTree(parent=parent,
                                     parent_index=parent_index,
                                     action=action)
                self.depth = new_node.layer
                new_node.set_all(parent_tmp)
                self.append(new_node)
                parent.children_indexs.append(self.buffer.__len__() - 1)
            print(' --> Expand', self.buffer.__len__())

    def simulate(self, node: BoardTree):
        return self.simulator.run(node, 5)

    def backprob(self, node, value):
        parent = node
        while parent is not None:
            parent.value = parent.value + value
            parent = parent.parent

    def UCB1(self, N, n, value, C=2):
        result = value + C * np.sqrt(np.log(N) / (n+0.000000001))
        return result

    def get_layer(self, level):
        layer = []
        for i in range(self.buffer.__len__()):
            if self.buffer[i].layer == level:
                layer.append(i)
        return layer

    # def select(self):
    #     child_nodes = []
    #     scores = []
    #     while True:
    #         node = self.get()
    #         if node is not None:
    #             if node.possible_moves:
    #                 scores.append(self.simulate(node))
    #             else:
    #                 scores.append(0)
    #             child_nodes.append(node)
    #         else:
    #             break
    #     if scores:
    #         actions = child_nodes[np.argmax(scores)].unroll()
    #         print('Tree traversal:', actions)
    #         return actions[0]
    #     return None

    # def expand(self, parent: BoardTree):
    #     for action in parent.possible_moves:
    #         parent_tmp = copy.deepcopy(parent)
    #         if self.executor.move(parent_tmp, action):
    #             new_node = BoardTree(parent, action)
    #             new_node.set_all(parent_tmp)
    #             self.append(new_node)


class Test(game.Py2048):

    def __init__(self, render: bool = True) -> None:
        super().__init__(render=render)
        self.game_engine.get_possible_moves(self.game_board)
        root = BoardTree()
        root.set_all(self.game_board)
        self.tree = MCTS(root=root, executor=game.Engine(), max_depth=3)
        self.count = 0
        self.log = False

    def loop_start(self):
        if not self.over:
            if self.count > 2:
                self.count = 0
                # action = random.choice(self.game_board.possible_moves)
                action = self.tree.search()
                # print(action)
                if not action:
                    action = random.choice(self.game_board.possible_moves)
                self.LOG(f'Selected action: {action}')
                self.step(action)
                if self.over:
                    self.LOG(f'Final score: {self.game_board.score}')
                else:
                    self.LOG(f'Next moves: {self.game_board.possible_moves}')
                    new_root = BoardTree()
                    new_root.set_all(self.game_board)
                    self.tree.reset(new_root)
            else:
                self.count += 1


t = Test()
t.mainloop()
