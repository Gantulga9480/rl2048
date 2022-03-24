from Py2048.game_core import Board, Engine
import random
import numpy as np


class Py2048Simulator:

    def __init__(self, sim_number) -> None:
        self.over = False
        self.game_board = Board()
        self.game_engine = Engine()
        self.sim_number = sim_number
        self.counter = 0

    def run(self, board=None):
        self.counter = 0
        self.over = False
        if board is not None:
            self.game_board.set_all(board)
        while self.counter != self.sim_number and not self.over:
            self.counter += 1
            try:
                move = random.choice(self.game_board.possible_actions)
                self.step(move)
            except IndexError:
                break
        return self.game_board.score

    def step(self, dir):
        if dir in self.game_board.possible_actions:
            self.game_engine.move(self.game_board, dir)
        self.over = not self.game_board.available()
        return self.over

    def scoring(self):
        final_score = 0
        max_tile_score = 0
        # board = self.game_board.get()
        # max_tile_value = np.max(board)
        # if board[3][0] == max_tile_value:
        #     max_tile_score = 1000
        #     for i in range(4):
        #         for j in range(4):
        #             if i != 3 and j != 0:
        #                 if board[i][j] == max_tile_value:
        #                     max_tile_score = 0
        #     if board[3][0] >= board[3][1] and board[3][1] >= board[3][2] and \
        #             board[3][2] >= board[3][3]:
        #         max_tile_score += 100
        empty_tile_score = len(self.game_board.empty_boxes) * 2
        game_score = self.game_board.score - self.game_board.last_score
        final_score = empty_tile_score + game_score + max_tile_score
        return final_score
