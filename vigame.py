from game import Game, Utils
import copy
import json
import numpy as np


BAD = -1000


class ViGame(Game):

    def __init__(self, animate: bool) -> None:
        super().__init__(animate)
        self.q_table = dict()
        self.epsilon = 0.2
        self.epsilon_decay = 0.999
        self.lr = 1
        self.gamma = 0.99

    def step(self, action):
        self.display()
        self.eventHandler()
        return self.move(action)

    def load_table(self, file: str):
        self.q_table = json.load(file)

    def save_table(self, file: str):
        with open(f'{file}.json', 'w') as data:
            json.dump(self.q_table, data)

    def get_action(self, state):
        if np.random.random() > self.epsilon and state in self.q_table:
            return np.argmax(self.q_table[state])
        else:
            # self.epsilon = max(0.01, self.epsilon * self.epsilon_decay)
            p_actions, mask = self.get_possible_moves()
            self.q_table[state] = [0 if item else BAD for item in mask]
            return np.random.choice(p_actions)

    def update(self, t, s, a, r, n_s):
        if not t:
            if n_s in self.q_table:
                max_f_q = max(self.q_table[n_s])
                current_q = self.q_table[s][a]
                self.q_table[s][a] = current_q + self.lr * (r + self.gamma * max_f_q - current_q)
            else:
                current_q = self.q_table[s][a]
                self.q_table[s][a] = current_q + self.lr * (r - current_q)
        else:
            self.q_table[s][a] = r

    def get_state(self):
        state = ''
        for i in range(4):
            for j in range(4):
                state += str(self.board.board[i][j]) + ','
        return state

    def move(self, action: int):
        prev_score = self.board.score
        reward = 0
        l_board = copy.deepcopy(self.board.board)
        if action == Utils.UP:
            self.is_moved = self.board.up()
        elif action == Utils.RIGHT:
            self.is_moved = self.board.right()
        elif action == Utils.DOWN:
            self.is_moved = self.board.down()
        elif action == Utils.LEFT:
            self.is_moved = self.board.left()
        elif action == Utils.UNDO:
            self.is_moved = self.undo()
        if self.is_moved:
            self.move_count += 1
            new_score = self.board.score - prev_score
            if action != Utils.UNDO:
                self.last_board = copy.deepcopy(l_board)
                if not self.board.is_full() and not self.over:
                    self.board.generate()
                self.over = self.board.check()
                if self.over:
                    reward = -1 * self.board.score
                else:
                    reward = new_score
            else:
                reward = -1 * self.last_reward
            self.last_reward = reward
            return self.over, self.get_state(), reward
        else:
            return False
