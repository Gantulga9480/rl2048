from Py2048.game_core import Board, Engine
import random


class Py2048Simulator:

    def __init__(self) -> None:
        self.over = False
        self.game_board = Board()
        self.game_engine = Engine()

    def run(self, board, itr=0):
        counter = 0
        self.over = False
        self.game_board.set_all(board)
        while counter != itr and not self.over:
            counter += 1
            move = random.choice(self.game_board.possible_moves)
            self.step(move)
        return self.game_board.score

    def step(self, dir):
        if dir in self.game_board.possible_moves:
            self.game_engine.move(self.game_board, dir)
        self.over = not self.game_board.available()
        return self.over
