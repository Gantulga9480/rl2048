import numpy as np
import random
import copy

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
UNDO = 4  # Experimantal
ACTION_SPACE = 5  # 5 for +UNDO
INPLACE = 5  # For animation


class Node:

    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __o: object) -> bool:
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
    START_BOX = 2  # Boxes to generate at start
    BOARD_SHAPE = (4, 4)

    def __init__(self, board=None) -> None:
        """
        If board is present, game board from pre-defined values.
        Otherwise will generate new board.
        Input shape must be (4, 4).
        """
        self.reset(board)

    def __repr__(self) -> str:
        return (f'{self.board[0][0]} {self.board[0][1]} {self.board[0][2]} '
                f'{self.board[0][3]}\n'
                f'{self.board[1][0]} {self.board[1][1]} {self.board[1][2]} '
                f'{self.board[1][3]}\n'
                f'{self.board[2][0]} {self.board[2][1]} {self.board[2][2]} '
                f'{self.board[2][3]}\n'
                f'{self.board[3][0]} {self.board[3][1]} {self.board[3][2]} '
                f'{self.board[3][3]}\n')

    def __eq__(self, __o: object) -> bool:
        for i in range(4):
            for j in range(4):
                try:
                    if self.board[i][j].value != __o[i][j].value:
                        return False
                except TypeError:
                    return False
        return True

    def __ne__(self, __o: object) -> bool:
        for i in range(4):
            for j in range(4):
                if self.board[i][j].value != __o[i][j].value:
                    return True
        return False

    def __getitem__(self, indices):
        """
        Access game board Node values by indexing Board class instanse.
        """
        return self.board[indices[0]][indices[1]].value

    def __setitem__(self, indices, new_value):
        if isinstance(new_value, Node):
            self.board[indices[0]][indices[1]] = new_value
        else:
            self.board[indices[0]][indices[1]].value = new_value

    def reset(self, board: 'Board' = None):
        self.board = [[Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)]]
        self.last_board = None
        self.score = 0
        self.last_score = 0
        self.possible_actions = []
        self.changes = []
        self.empty_boxes = []
        if board is not None:
            self.set(board)
        else:
            for _ in range(self.START_BOX):
                self.empty_boxes = self.get_empty()
                self.generate()

    def set(self, b) -> None:
        self.board = [[Node(b[0, 0]), Node(b[0, 1]),
                       Node(b[0, 2]), Node(b[0, 3])],
                      [Node(b[1, 0]), Node(b[1, 1]),
                       Node(b[1, 2]), Node(b[1, 3])],
                      [Node(b[2, 0]), Node(b[2, 1]),
                       Node(b[2, 2]), Node(b[2, 3])],
                      [Node(b[3, 0]), Node(b[3, 1]),
                       Node(b[3, 2]), Node(b[3, 3])]]

    def set_all(self, board):
        self.set(board.get())
        self.score = board.score
        self.last_score = board.last_score
        self.possible_actions = board.possible_actions.copy()
        self.changes = board.changes.copy()
        self.empty_boxes = board.empty_boxes.copy()
        self.last_board = copy.deepcopy(board.last_board)

    def get(self) -> np.ndarray:
        board = np.zeros(self.BOARD_SHAPE, dtype=np.int32)
        for i in range(self.BOARD_SHAPE[0]):
            for j in range(self.BOARD_SHAPE[1]):
                board[i, j] = self.board[i][j].value
        return board.copy()

    def generate(self):
        if self.empty_boxes.__len__() > 0:
            pos = random.choice(self.empty_boxes)
            odd = random.randint(1, (100 // self.ODDS))
            if odd == (100 // self.ODDS):
                self.board[pos[0]][pos[1]].value = 4
            else:
                self.board[pos[0]][pos[1]].value = 2

    def get_empty(self):
        empty_box = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j].value == 0:
                    empty_box.append([i, j])
        if empty_box.__len__() > 0:
            return empty_box.copy()
        return None

    def is_full(self):
        self.empty_boxes = self.get_empty()
        if self.empty_boxes.__len__() > 0:
            return False
        else:
            return True

    def available(self):
        if self.board[3][3].value == 0:
            return True
        for i in range(3):
            for j in range(4):
                if self.board[i][j].value == self.board[i + 1][j].value or \
                        self.board[i][j].value == 0:
                    return True
        for i in range(4):
            for j in range(3):
                if self.board[i][j].value == self.board[i][j + 1].value or \
                        self.board[i][j].value == 0:
                    return True
        return False


class Engine:

    def __init__(self) -> None:
        self.board = None
        self.changed = False

    def reset(self) -> None:
        self.board = None
        self.changed = False

    def move(self, board: Board, dir) -> bool:
        self.board = board
        if dir != UNDO:
            # required for not exceeding maximum recursion depth
            self.board.last_board = None
            self.board.last_board = copy.deepcopy(board)
        self.board.changes.clear()
        self.board.last_score = self.board.score
        if dir == UP:
            self.board.score += self.up()
        elif dir == DOWN:
            self.board.score += self.down()
        elif dir == LEFT:
            self.board.score += self.left()
        elif dir == RIGHT:
            self.board.score += self.right()
        elif dir == UNDO:
            return self.undo()
        if self.changed:
            if not self.board.is_full():
                self.board.generate()
            self.get_possible_actions()
            return True
        self.board.score = 0
        return False

    def undo(self):
        if self.board.last_board is not None:
            self.board.set_all(self.board.last_board)
            self.board.last_board = None  # Delete last board after UNDO
            self.get_possible_actions()
            return True
        return False

    def up(self):
        __score = 0
        self.changed = False
        self.board.changes.clear()
        for i in range(4):
            row_modif = False
            for j in range(1, 4, 1):
                if self.board[j, i] != 0:
                    modif = False
                    start_index = [j, i]
                    stop_index = [j, i]
                    while True:
                        if j >= 1:
                            if j == 1 and row_modif and not modif:
                                break
                            elif j == 2 and row_modif and not modif and \
                                    self.board[j - 1, i] == self.board[j, i]:
                                break
                            elif self.board[j - 1, i] == \
                                    self.board[j, i] and not modif:
                                self.board[j - 1, i] = \
                                    self.board[j, i] * 2
                                __score += self.board[j, i] * 2
                                self.board[j, i] = 0
                                modif = True
                                row_modif = True
                                stop_index = [j - 1, i]
                            elif self.board[j - 1, i] == 0:
                                self.board[j - 1, i] = \
                                    self.board[j, i]
                                self.board[j, i] = 0
                                stop_index = [j - 1, i]
                            j -= 1
                        else:
                            break
                    if start_index[0] != stop_index[0] or \
                            start_index[1] != stop_index[1]:
                        self.changed = True
                        self.board.changes.append([start_index,
                                                   stop_index, UP])
                    else:
                        self.board.changes.append([start_index,
                                                   stop_index, INPLACE])
        return __score

    def down(self):
        __score = 0
        self.changed = False
        self.board.changes.clear()
        for i in range(4):
            row_modif = False
            for j in range(3, -1, -1):
                if self.board[j, i] != 0:
                    modif = False
                    start_index = [j, i]
                    stop_index = [j, i]
                    while True:
                        try:
                            if j == 2 and row_modif and not modif:
                                break
                            elif j == 1 and row_modif and not modif and \
                                    self.board[j + 1, i] == self.board[j, i]:
                                break
                            elif self.board[j + 1, i] == \
                                    self.board[j, i] and not modif:
                                self.board[j + 1, i] = \
                                    self.board[j, i] * 2
                                __score += self.board[j, i] * 2
                                self.board[j, i] = 0
                                modif = True
                                row_modif = True
                                stop_index = [j + 1, i]
                            elif self.board[j + 1, i] == 0:
                                self.board[j + 1, i] = \
                                    self.board[j, i]
                                self.board[j, i] = 0
                                stop_index = [j + 1, i]
                            j += 1
                        except IndexError:
                            break
                    if start_index[0] != stop_index[0] or \
                            start_index[1] != stop_index[1]:
                        self.changed = True
                        self.board.changes.append([start_index,
                                                   stop_index, DOWN])
                    else:
                        self.board.changes.append([start_index,
                                                   stop_index, INPLACE])
        return __score

    def left(self):
        __score = 0
        self.changed = False
        self.board.changes.clear()
        for j in range(4):
            row_modif = False
            for i in range(1, 4, 1):
                if self.board[j, i] != 0:
                    modif = False
                    start_index = [j, i]
                    stop_index = [j, i]
                    while True:
                        if i >= 1:
                            if i == 1 and row_modif and not modif:
                                break
                            elif i == 2 and row_modif and not modif and \
                                    self.board[j, i - 1] == self.board[j, i]:
                                break
                            elif self.board[j, i - 1] == \
                                    self.board[j, i] and not modif:
                                self.board[j, i - 1] = \
                                    self.board[j, i] * 2
                                __score += self.board[j, i] * 2
                                self.board[j, i] = 0
                                modif = True
                                row_modif = True
                                stop_index = [j, i - 1]
                            elif self.board[j, i - 1] == 0:
                                self.board[j, i - 1] = \
                                    self.board[j, i]
                                self.board[j, i] = 0
                                stop_index = [j, i - 1]
                            i -= 1
                        else:
                            break
                    if start_index[0] != stop_index[0] or \
                            start_index[1] != stop_index[1]:
                        self.changed = True
                        self.board.changes.append([start_index,
                                                   stop_index, LEFT])
                    else:
                        self.board.changes.append([start_index,
                                                   stop_index, INPLACE])
        return __score

    def right(self):
        __score = 0
        self.changed = False
        self.board.changes.clear()
        for j in range(4):
            row_modif = False
            for i in range(3, -1, -1):
                if self.board[j, i] != 0:
                    modif = False
                    start_index = [j, i]
                    stop_index = [j, i]
                    while True:
                        try:
                            if i == 2 and row_modif and not modif:
                                break
                            elif i == 1 and row_modif and not modif and \
                                    self.board[j, i + 1] == self.board[j, i]:
                                break
                            elif self.board[j, i + 1] == \
                                    self.board[j, i] and not modif:
                                self.board[j, i + 1] = \
                                    self.board[j, i] * 2
                                __score += self.board[j, i] * 2
                                self.board[j, i] = 0
                                modif = True
                                row_modif = True
                                stop_index = [j, i + 1]
                            elif self.board[j, i + 1] == 0:
                                self.board[j, i + 1] = \
                                    self.board[j, i]
                                self.board[j, i] = 0
                                stop_index = [j, i + 1]
                            i += 1
                        except IndexError:
                            break
                    if start_index[0] != stop_index[0] or \
                            start_index[1] != stop_index[1]:
                        self.changed = True
                        self.board.changes.append([start_index,
                                                   stop_index, RIGHT])
                    else:
                        self.board.changes.append([start_index,
                                                   stop_index, INPLACE])
        return __score

    def get_possible_actions(self, board: Board = None):
        moves = []
        if board:
            self.board = board
        changes_tmp = self.board.changes.copy()  # preserve changes
        start = self.board.get()  # Get copy of main board values
        changed_state_tmp = self.changed  # preserve changed state
        for action in range(ACTION_SPACE):
            if action == UP:
                self.up()
            elif action == DOWN:
                self.down()
            elif action == LEFT:
                self.left()
            elif action == RIGHT:
                self.right()
            elif action == UNDO:
                self.changed = False
                if self.board.last_board is not None:
                    self.changed = True
            if self.changed:
                moves.append(action)
            self.board.set(start)  # Revert back to main board values
        self.board.changes = changes_tmp.copy()  # set back to main changes
        self.changed = changed_state_tmp
        if len(moves) > 0:
            self.board.possible_actions = moves.copy()
            return moves
        self.board.possible_actions = []
        return []
