import pygame
import random
import numpy as np
import copy


class Utils:

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    WIDTH = 410
    HEIGTH = WIDTH
    BOX_PAD = WIDTH % 100
    BOX = (WIDTH - BOX_PAD)//4
    START_BOX = 2

    POSITION = [[[BOX_PAD+BOX*0, BOX_PAD+BOX*0],
                 [BOX_PAD+BOX*1, BOX_PAD+BOX*0],
                 [BOX_PAD+BOX*2, BOX_PAD+BOX*0],
                 [BOX_PAD+BOX*3, BOX_PAD+BOX*0]],
                [[BOX_PAD+BOX*0, BOX_PAD+BOX*1],
                 [BOX_PAD+BOX*1, BOX_PAD+BOX*1],
                 [BOX_PAD+BOX*2, BOX_PAD+BOX*1],
                 [BOX_PAD+BOX*3, BOX_PAD+BOX*1]],
                [[BOX_PAD+BOX*0, BOX_PAD+BOX*2],
                 [BOX_PAD+BOX*1, BOX_PAD+BOX*2],
                 [BOX_PAD+BOX*2, BOX_PAD+BOX*2],
                 [BOX_PAD+BOX*3, BOX_PAD+BOX*2]],
                [[BOX_PAD+BOX*0, BOX_PAD+BOX*3],
                 [BOX_PAD+BOX*1, BOX_PAD+BOX*3],
                 [BOX_PAD+BOX*2, BOX_PAD+BOX*3],
                 [BOX_PAD+BOX*3, BOX_PAD+BOX*3]]]


class Color:

    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    BG = pygame.Color(187, 173, 160)
    BOX_EMPTY = pygame.Color(214, 205, 196)
    BOX_2 = pygame.Color(238, 228, 216)
    BOX_4 = pygame.Color(236, 224, 200)
    BOX_8 = pygame.Color(242, 177, 121)
    BOX_16 = pygame.Color(246, 148, 99)
    BOX_32 = pygame.Color(245, 124, 95)
    BOX_64 = pygame.Color(246, 93, 61)
    BOX_128 = pygame.Color(237, 206, 113)
    BOX_256 = pygame.Color(237, 204, 97)
    BOX_512 = pygame.Color(236, 200, 80)
    BOX_1024 = pygame.Color(237, 197, 63)
    BOX_2048 = pygame.Color(237, 197, 46)


class Node:

    def __init__(self, value) -> None:
        self.value = 0
        self.color = Color.BOX_EMPTY
        self.modified = False
        self.setValue(value)

    def __eq__(self, o: object) -> bool:
        return o.value == self.value

    def __repr__(self) -> str:
        return str(self.value)

    def setValue(self, value : int):
        self.value = value
        if self.value == 0:
            self.color = Color.BOX_EMPTY
        elif self.value == 2:
            self.color = Color.BOX_2
        elif self.value == 4:
            self.color = Color.BOX_4
        elif self.value == 8:
            self.color = Color.BOX_8
        elif self.value == 16:
            self.color = Color.BOX_16
        elif self.value == 32:
            self.color = Color.BOX_32
        elif self.value == 64:
            self.color = Color.BOX_64
        elif self.value == 128:
            self.color = Color.BOX_128
        elif self.value == 256:
            self.color = Color.BOX_256
        elif self.value == 512:
            self.color = Color.BOX_512
        elif self.value == 1024:
            self.color = Color.BOX_512
        elif self.value == 2048:
            self.color = Color.BOX_512
        else:
            self.color = Color.BLACK


class Board:

    def __init__(self) -> None:
        self.modified = False
        self.reset()
        for _ in range(Utils.START_BOX):
            self.generate()

    def get_board(self):
        board = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                board[i, j] = self.board[i][j].value
        return board.copy()

    def reset(self):
        self.board = [[Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)]]

    def generate(self):
        done = False
        while not done:
            pos_x = random.randint(0, 3)
            pos_y = random.randint(0, 3)
            if self.board[pos_y][pos_x].value == 0:
                odd = random.randint(0, 3)
                if odd == 3:
                    self.board[pos_y][pos_x].setValue(4)
                else:
                    self.board[pos_y][pos_x].setValue(2)
                done = True

    def check(self) -> bool:
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i+1][j] or \
                        self.board[i][j].value == 0:
                    return False
        for i in range(4):
            for j in range(3):
                if self.board[i][j] == self.board[i][j+1] or \
                        self.board[i][j].value == 0:
                    return False
        if self.board[3][3].value == 0:
            return False
        return True

    def is_full(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j].value == 0:
                    return False
        return True

    def right(self):
        self.modified = False
        for i in range(2, -1, -1):
            for j in range(4):
                if self.board[j][i].value != 0:
                    self.move_right(j, i)
        self.mod_reset()
        return self.modified

    def move_right(self, x, y):
        if self.board[x][y] == self.board[x][y+1] and \
                not self.board[x][y+1].modified:
            self.board[x][y+1].setValue(self.board[x][y].value*2)
            self.board[x][y].setValue(0)
            self.board[x][y+1].modified = True
            self.modified = True
        elif self.board[x][y+1].value == 0:
            self.board[x][y+1].setValue(self.board[x][y].value)
            self.board[x][y].setValue(0)
            self.modified = True
            if y+1 != 3:
                self.move_right(x, y+1)

    def left(self):
        self.modified = False
        for i in range(1, 4):
            for j in range(4):
                if self.board[j][i].value != 0:
                    self.move_left(j, i)
        self.mod_reset()
        return self.modified

    def move_left(self, x, y):
        if self.board[x][y] == self.board[x][y-1] and \
                not self.board[x][y-1].modified:
            self.board[x][y-1].setValue(self.board[x][y].value*2)
            self.board[x][y].setValue(0)
            self.board[x][y-1].modified = True
            self.modified = True
        elif self.board[x][y-1].value == 0:
            self.board[x][y-1].setValue(self.board[x][y].value)
            self.board[x][y].setValue(0)
            self.modified = True
            if y-1 != 0:
                self.move_left(x, y-1)

    def up(self):
        self.modified = False
        for i in range(4):
            for j in range(1, 4):
                if self.board[j][i].value != 0:
                    self.move_up(j, i)
        self.mod_reset()
        return self.modified

    def move_up(self, x, y):
        if self.board[x][y] == self.board[x-1][y] and \
                not self.board[x-1][y].modified:
            self.board[x-1][y].setValue(self.board[x][y].value*2)
            self.board[x][y].setValue(0)
            self.board[x-1][y].modified = True
            self.modified = True
        elif self.board[x-1][y].value == 0:
            self.board[x-1][y].setValue(self.board[x][y].value)
            self.board[x][y].setValue(0)
            self.modified = True
            if x-1 != 0:
                self.move_up(x-1, y)

    def down(self):
        self.modified = False
        for i in range(4):
            for j in range(2, -1, -1):
                if self.board[j][i].value != 0:
                    self.move_down(j, i)
        self.mod_reset()
        return self.modified

    def move_down(self, x, y):
        if self.board[x][y] == self.board[x+1][y] and \
                not self.board[x+1][y].modified:
            self.board[x+1][y].setValue(self.board[x][y].value*2)
            self.board[x][y].setValue(0)
            self.board[x+1][y].modified = True
            self.modified = True
        elif self.board[x+1][y].value == 0:
            self.board[x+1][y].setValue(self.board[x][y].value)
            self.board[x][y].setValue(0)
            self.modified = True
            if x+1 != 3:
                self.move_down(x+1, y)

    def mod_reset(self):
        for i in range(4):
            for j in range(4):
                self.board[i][j].modified = False


class Game:

    def __init__(self) -> None:
        pygame.init()                               # Initialize pygame module
        self.clock = pygame.time.Clock()                    # Game clock
        self.font = pygame.font.SysFont("arial", 30, True)  # Game font
        self.win = pygame.display.set_mode((Utils.WIDTH,
                                            Utils.HEIGTH))  # Initialize main window
        self.run = True                                     # Game running flag
        self.over = False
        self.is_moved = False
        self.board = Board()
        self.last_board = None

    def display(self) -> None:
        """
        Display game visual to main window
        """
        self.win.fill(Color.BG)
        self.drawNums()
        if self.over:
            self.game_over_screen()
        pygame.display.flip()              # draw main window to display
        self.clock.tick(60)                # 60 frames per second clock tick

    def eventHandler(self) -> None:
        """
        Event handler for main window
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False                            # Close game window
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move(Utils.UP)
                elif event.key == pygame.K_LEFT:
                    self.move(Utils.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.move(Utils.RIGHT)
                elif event.key == pygame.K_DOWN:
                    self.move(Utils.DOWN)
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_u:
                    self.undo()

    def move(self, dir : int):
        if dir == Utils.UP and not self.over:
            l_board = copy.deepcopy(self.board.board)
            if self.board.up():
                self.is_moved = True
                self.last_board = copy.deepcopy(l_board)
        elif dir == Utils.RIGHT and not self.over:
            l_board = copy.deepcopy(self.board.board)
            if self.board.right():
                self.is_moved = True
                self.last_board = copy.deepcopy(l_board)
        elif dir == Utils.DOWN and not self.over:
            l_board = copy.deepcopy(self.board.board)
            if self.board.down():
                self.is_moved = True
                self.last_board = copy.deepcopy(l_board)
        elif dir == Utils.LEFT and not self.over:
            l_board = copy.deepcopy(self.board.board)
            if self.board.left():
                self.is_moved = True
                self.last_board = copy.deepcopy(l_board)

        if self.is_moved:
            if not self.board.is_full() and not self.over:
                self.board.generate()
            self.is_moved = False
            self.over = self.board.check()

    def undo(self):
        self.over = False
        self.board.board = copy.deepcopy(self.last_board)

    def reset(self) -> None:
        del self.board
        self.board = Board()
        self.over = False

    def drawNums(self) -> None:
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.win, self.board.board[i][j].color,
                                 pygame.Rect(*Utils.POSITION[i][j],
                                             Utils.BOX-Utils.BOX_PAD,
                                             Utils.BOX-Utils.BOX_PAD),
                                 0, 7)
                if self.board.board[i][j].value != 0:
                    if self.board.board[i][j].value < 4096:
                        txt = self.font.render(str(self.board.board[i][j].value),
                                               1, Color.BLACK)
                    else:
                        txt = self.font.render(str(self.board.board[i][j].value),
                                               1, Color.WHITE)

                    self.win.blit(txt, [Utils.POSITION[i][j][0]+(Utils.BOX-Utils.BOX_PAD)//2 - txt.get_width()//2,
                                        Utils.POSITION[i][j][1]+(Utils.BOX-Utils.BOX_PAD)//2 - txt.get_height()//2])

    def game_over_screen(self) -> None:
        txt = self.font.render('GAME OVER', 1, Color.BLACK)
        self.win.blit(txt, [Utils.WIDTH//2 - txt.get_width()//2,
                            Utils.HEIGTH//2 - txt.get_height()//2])
