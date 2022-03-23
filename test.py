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
        if self.children_indexs:
            return True
        else:
            return False

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


class MCTS(BredthFirstSearch):

    def __init__(self,
                 root: BoardTree,
                 executor: game.Engine,
                 target=None,
                 max_depth=0,
                 sim_num=-1) -> None:
        super().__init__(root, executor, target, max_depth)
        self.simulator = Py2048Simulator(sim_num)
        self.depth = 0

    def search(self):
        self.depth = 0
        self.expand(0)  # expand root first
        while self.depth < self.max_depth:
            if not self.traverse(0):  # start from top node
                break
        next_layer = self.get_layer(self.root.layer + 1)
        score = [self.buffer[i].value for i in next_layer]
        best_node = self.buffer[next_layer[np.argmax(score)]]
        return best_node.unroll()[0][0]

    def traverse(self, index):
        print('Traverse')
        node = self.buffer[index]
        if node.visit_count == 0:
            print('Simulate')
            sim_result = self.simulate(node)
            self.backprob(node, sim_result)
            return True
        elif node.visit_count != 0:
            if node.has_child():
                selected_node = self.select(index)
                return self.traverse(selected_node)
            elif node.visit_count == 1:  # just simulated
                print('Expand')
                self.expand(index)
                return True
            else:
                return False
        return False

    def select(self, index):
        # print('select')
        node = self.buffer[index]
        ind = node.children_indexs
        scores = []
        for i in ind:
            child = self.buffer[i]
            p_N = node.visit_count
            c_n = child.visit_count
            val = child.value
            ucb = self.UCB1(p_N, c_n, val)
            # print(p_N, c_n, val, ucb)
            scores.append(ucb)
        same = True
        for score in scores:
            if score != scores[0]:
                same = False
        # print(score)
        if not same:
            return ind[np.argmax(scores)]
        else:
            return random.choice(ind)

    def expand(self, parent_index):
        parent = self.buffer[parent_index]
        parent.children_indexs.clear()
        for action in parent.possible_moves:
            parent_tmp = copy.deepcopy(parent)
            if self.executor.move(parent_tmp, action):
                new_node = BoardTree(parent=parent,
                                     parent_index=parent_index,
                                     action=action)
                new_node.set_all(parent_tmp)
                self.depth = new_node.layer
                self.append(new_node)
                parent.children_indexs.append(self.buffer.__len__() - 1)

    def backprob(self, node, value):
        parent = node
        while parent is not None:
            parent.value = parent.value + value
            parent.visit_count += 1
            parent = parent.parent

    def UCB1(self, N, n, value, C=0):
        result = value / (n+0.000000001) + \
            C * np.sqrt(2 * np.log(N) / (n+0.000000001))
        return result

    def get_layer(self, level):
        layer = []
        for i in range(self.buffer.__len__()):
            if self.buffer[i].layer == level:
                layer.append(i)
        return layer

    def search1(self):
        while True:
            node = self.get()
            if node is not None:
                if node.layer < self.max_depth:
                    self.expand1(node)
                else:
                    self.append(node)  # put back node to tree
                    break
            else:
                break
        return self.select1()

    def select1(self):
        child_nodes = []
        scores = []
        while True:
            node = self.get()
            if node is not None:
                if node.possible_moves:
                    sim_score = self.simulate(node)
                    total_score = node.unroll()[1] + sim_score
                    scores.append(total_score)
                else:
                    scores.append(0)
                child_nodes.append(node)
            else:
                break
        if scores:
            actions, _ = child_nodes[np.argmax(scores)].unroll()
            print('Tree traversal:', actions)
            return actions[0]
        return None

    def expand1(self, parent: BoardTree):
        for action in parent.possible_moves:
            parent_tmp = copy.deepcopy(parent)
            if self.executor.move(parent_tmp, action):
                new_node = BoardTree(parent=parent, action=action)
                new_node.set_all(parent_tmp)
                self.append(new_node)

    def simulate(self, node: BoardTree):
        return self.simulator.run(node)


class Test(game.Py2048):

    def __init__(self, render: bool = True) -> None:
        super().__init__(render=render)
        root = BoardTree()
        root.visit_count = 1
        root.set_all(self.game_board)
        self.tree = MCTS(root=root, executor=game.Engine(),
                         max_depth=5, sim_num=10)
        self.count = 0
        self.log = True

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
