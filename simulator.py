from Py2048.game_core import Board, Engine
import random


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
            move = random.choice(self.game_board.possible_actions)
            self.step(move)
        return self.scoring()

    def step(self, dir):
        if dir in self.game_board.possible_actions:
            self.game_engine.move(self.game_board, dir)
        self.over = not self.game_board.available()
        return not self.over

    def scoring(self):
        final_score = 0
        empty_tile_score = 0
        game_score = self.game_board.score
        final_score = empty_tile_score + game_score
        return final_score
