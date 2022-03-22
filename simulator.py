from Py2048.game_core import Board, Engine
import random


class Py2048Simulator:

    def __init__(self, sim_number) -> None:
        self.over = False
        self.game_board = Board()
        self.game_engine = Engine()
        self.sim_number = sim_number

    def run(self, board):
        counter = 0
        self.over = False
        self.game_board.set_all(board)
        while counter != self.sim_number and not self.over:
            counter += 1
            try:
                move = random.choice(self.game_board.possible_moves)
                self.step(move)
            except IndexError:
                break
        return self.game_board.score

    def step(self, dir):
        if dir in self.game_board.possible_moves:
            self.game_engine.move(self.game_board, dir)
        self.over = not self.game_board.available()
        return self.over
