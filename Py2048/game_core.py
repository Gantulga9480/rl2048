import numpy as np
import random
import copy
from .utils import *


class Node:

    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __o) -> bool:
        if isinstance(__o, Node):
            return __o.value == self.value
        elif isinstance(__o, int):
            return __o == self.value

    def __ne__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return __o.value != self.value
        elif isinstance(__o, int):
            return __o != self.value

    def __repr__(self) -> str:
        return str(self.value)


class Board:

    ODDS = 10      # odds to generate 4 instead of 2
    START_BOX = 2  # Boself.current_boardes to generate at start
    BOARD_SHAPE = (4, 4)

    def __init__(self, board=None) -> None:
        """
        If board is present, initialize game board from pre-defined values.
        Otherwise will generate new board.
        Input shape must be (4, 4).
        """
        self.reset()
        if board is not None:
            self.set(board)
        else:
            for _ in range(self.START_BOX):
                self.generate()

    def __repr__(self) -> str:
        return (f'{self.board[0][0]} {self.board[0][1]} {self.board[0][2]}'
                f' {self.board[0][3]}\n'
                f'{self.board[1][0]} {self.board[1][1]} {self.board[1][2]}'
                f' {self.board[1][3]}\n'
                f'{self.board[2][0]} {self.board[2][1]} {self.board[2][2]}'
                f' {self.board[2][3]}\n'
                f'{self.board[3][0]} {self.board[3][1]} {self.board[3][2]}'
                f' {self.board[3][3]}\n')

    def __getitem__(self, indices):
        """
        Access game board Node values by indexing Board class instanse.
        """
        if not isinstance(indices, tuple):
            return [node.value for node in self.board[indices]]
        return self.board[indices[0]][indices[1]].value

    def __setitem__(self, indices, new_value):
        if isinstance(new_value, Node):
            self.board[indices[0]][indices[1]] = new_value
        else:
            self.board[indices[0]][indices[1]].value = new_value

    def reset(self):
        self.filled = False
        self.board = [[Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)]]

    def set(self, b):
        self.board = [[Node(b[0, 0]), Node(b[0, 1]),
                       Node(b[0, 2]), Node(b[0, 3])],
                      [Node(b[1, 0]), Node(b[1, 1]),
                       Node(b[1, 2]), Node(b[1, 3])],
                      [Node(b[2, 0]), Node(b[2, 1]),
                       Node(b[2, 2]), Node(b[2, 3])],
                      [Node(b[3, 0]), Node(b[3, 1]),
                       Node(b[3, 2]), Node(b[3, 3])]]

    def get(self):
        board = np.zeros(self.BOARD_SHAPE)
        for i in range(self.BOARD_SHAPE[0]):
            for j in range(self.BOARD_SHAPE[1]):
                board[i, j] = self.board[i][j].value
        return board.copy()

    def generate(self):
        if not self.is_full():
            done = False
            while not done:
                pos_x = random.randint(0, 3)
                pos_y = random.randint(0, 3)
                if self.board[pos_y][pos_x].value == 0:
                    odd = random.randint(1, (100 // self.ODDS))
                    if odd == (100 // self.ODDS):
                        self.board[pos_y][pos_x].value = 4
                    else:
                        self.board[pos_y][pos_x].value = 2
                    done = True
        return not self.filled

    def is_full(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j].value == 0:
                    self.filled = False
                    return self.filled
        self.filled = True
        return self.filled


class Engine:

    def __init__(self) -> None:
        self.last_board = None
        self.current_board = None
        self.changes = []

    def move(self, board: Board, move_dir) -> None:
        self.changes.clear()
        self.last_board = copy.deepcopy(board)
        self.current_board = board
        if move_dir == UP:
            self.up()
        elif move_dir == DOWN:
            self.down()
        elif move_dir == LEFT:
            self.left()
        elif move_dir == RIGHT:
            self.right()

    def up(self):
        for j in range(1, 4, 1):
            row_modif = False
            for i in range(4):
                if self.current_board[j, i] != 0:
                    modif = False
                    start_index = [j, i]
                    stop_index = [j, i]
                    while True:
                        if j >= 1:
                            if j == 1 and row_modif and not modif:
                                break
                            elif self.current_board[j-1, i] == \
                                    self.current_board[j, i] and not modif:
                                self.current_board[j-1, i] = \
                                    self.current_board[j, i]*2
                                self.current_board[j, i] = 0
                                modif = True
                                row_modif = True
                                stop_index = [j-1, i]
                            elif self.current_board[j-1, i] == 0:
                                self.current_board[j-1, i] = \
                                    self.current_board[j, i]
                                self.current_board[j, i] = 0
                                stop_index = [j-1, i]
                            j -= 1
                        else:
                            break
                    if start_index[0] != stop_index[0] or \
                            start_index[1] != stop_index[1]:
                        self.changes.append([start_index, stop_index, UP])

    def down(self):
        for j in range(3, -1, -1):
            row_modif = False
            for i in range(4):
                if self.current_board[j, i] != 0:
                    modif = False
                    start_index = [j, i]
                    stop_index = [j, i]
                    while True:
                        try:
                            if i == 1 and row_modif and not modif:
                                break
                            elif self.current_board[j+1, i] == \
                                    self.current_board[j, i] and not modif:
                                self.current_board[j+1, i] = \
                                    self.current_board[j, i]*2
                                self.current_board[j, i] = 0
                                modif = True
                                row_modif = True
                                stop_index = [j+1, i]
                            elif self.current_board[j+1, i] == 0:
                                self.current_board[j+1, i] = \
                                    self.current_board[j, i]
                                self.current_board[j, i] = 0
                                stop_index = [j+1, i]
                            j += 1
                        except IndexError:
                            break
                    if start_index[0] != stop_index[0] or \
                            start_index[1] != stop_index[1]:
                        self.changes.append([start_index, stop_index, DOWN])

    def right(self):
        for j in range(4):
            row_modif = False
            for i in range(1, 4, 1):
                if self.current_board[j, i] != 0:
                    modif = False
                    start_index = [j, i]
                    stop_index = [j, i]
                    while True:
                        if i >= 1:
                            if i == 1 and row_modif and not modif:
                                break
                            elif self.current_board[j, i-1] == \
                                    self.current_board[j, i] and not modif:
                                self.current_board[j, i-1] = \
                                    self.current_board[j, i]*2
                                self.current_board[j, i] = 0
                                modif = True
                                row_modif = True
                                stop_index = [j, i-1]
                            elif self.current_board[j, i-1] == 0:
                                self.current_board[j, i-1] = \
                                    self.current_board[j, i]
                                self.current_board[j, i] = 0
                                stop_index = [j, i-1]
                            i -= 1
                        else:
                            break
                    if start_index[0] != stop_index[0] or \
                            start_index[1] != stop_index[1]:
                        self.changes.append([start_index, stop_index, RIGHT])

    def left(self):
        for j in range(4):
            row_modif = False
            for i in range(3, -1, -1):
                if self.current_board[j, i] != 0:
                    modif = False
                    start_index = [j, i]
                    stop_index = [j, i]
                    while True:
                        try:
                            if i == 2 and row_modif and not modif:
                                break
                            elif self.current_board[j, i+1] == \
                                    self.current_board[j, i] and not modif:
                                self.current_board[j, i+1] = \
                                    self.current_board[j, i] * 2
                                self.current_board[j, i] = 0
                                modif = True
                                row_modif = True
                                stop_index = [j, i+1]
                            elif self.current_board[j, i+1] == 0:
                                self.current_board[j, i+1] = \
                                    self.current_board[j, i]
                                self.current_board[j, i] = 0
                                stop_index = [j, i+1]
                            i += 1
                        except IndexError:
                            break
                    if start_index[0] != stop_index[0] or \
                            start_index[1] != stop_index[1]:
                        self.changes.append([start_index, stop_index, LEFT])
