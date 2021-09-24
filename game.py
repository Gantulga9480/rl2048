import pygame
import numpy as np


class Utils:

    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'

    WIDTH = 410
    HEIGTH = 410
    BOX = 100
    BOX_PAD = 10

    POSITION = [[[BOX_PAD+BOX*0, BOX_PAD+BOX*0], [BOX_PAD+BOX*1, BOX_PAD+BOX*0], [BOX_PAD+BOX*2, BOX_PAD+BOX*0], [BOX_PAD+BOX*3, BOX_PAD+BOX*0]],
                [[BOX_PAD+BOX*0, BOX_PAD+BOX*1], [BOX_PAD+BOX*1, BOX_PAD+BOX*1], [BOX_PAD+BOX*2, BOX_PAD+BOX*1], [BOX_PAD+BOX*3, BOX_PAD+BOX*1]],
                [[BOX_PAD+BOX*0, BOX_PAD+BOX*2], [BOX_PAD+BOX*1, BOX_PAD+BOX*2], [BOX_PAD+BOX*2, BOX_PAD+BOX*2], [BOX_PAD+BOX*3, BOX_PAD+BOX*2]],
                [[BOX_PAD+BOX*0, BOX_PAD+BOX*3], [BOX_PAD+BOX*1, BOX_PAD+BOX*3], [BOX_PAD+BOX*2, BOX_PAD+BOX*3], [BOX_PAD+BOX*3, BOX_PAD+BOX*3]]]


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
        self.setValue(value)

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
        self.board = [[Node(0), Node(4096), Node(0), Node(0)],
                      [Node(128), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)],
                      [Node(0), Node(0), Node(0), Node(0)]]

    def board_right(self):
        for i in range(2, 0, -1):
            for j in range(4):
                if self.board[j][i].value != 0:
                    if self.board[j][i+1].value == self.board[j][i]:
                        self.board[j][i+1] *= 2

    def move_right(self, x, y):
        if self.board[x][y] != 0 and y + 1 < 4:
            if self.board[x][y] == self.board[x][y+1]:
                self.board[x][y+1] *= 2
        else:
            return

    def check_row_(self, x : int, y : int, dir : str):
        if dir == 'left':
            ...


class Game:

    def __init__(self) -> None:
        pygame.init()                                       # Initialize pygame module
        self.clock = pygame.time.Clock()                    # Game clock
        self.font = pygame.font.SysFont("arial", 30, True)  # Game font
        self.win = pygame.display.set_mode((Utils.WIDTH,
                                            Utils.HEIGTH))  # Initialize main window
        self.run = True                                     # Game running flag
        self.board = Board()

    def display(self):
        """
        Display game visual to main window
        """
        self.win.fill(Color.BG)
        # self.grid()
        self.drawNums()
        pygame.display.flip()                               # draw main window to display
        self.clock.tick(60)                                 # 60 frames per second clock tick

    def eventHandler(self):
        """
        Event handler for main window
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False                            # Close game window
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ...
                elif event.key == pygame.K_LEFT:
                    ...
                elif event.key == pygame.K_RIGHT:
                    ...
                elif event.key == pygame.K_DOWN:
                    ...

    def move(self, dir : str):
        for i in range(4):
            for j in range(4):
                if dir == Utils.UP:
                    ...
                elif dir == Utils.LEFT:
                    ...
                elif dir == Utils.RIGHT:
                    ...
                elif dir == Utils.DOWN:
                    ...

    def drawNums(self):
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.win, self.board.board[i][j].color,
                                 pygame.Rect(*Utils.POSITION[i][j],
                                             Utils.BOX-Utils.BOX_PAD,
                                             Utils.BOX-Utils.BOX_PAD),
                                 0, 7)
                if self.board.board[i][j].value != 0:
                    if self.board.board[i][j].value < 4096:
                        txt = self.font.render(str(self.board.board[i][j].value), 1, Color.BLACK)
                    else:
                        txt = self.font.render(str(self.board.board[i][j].value), 1, Color.WHITE)

                    self.win.blit(txt, [Utils.POSITION[i][j][0]+(Utils.BOX-Utils.BOX_PAD)//2 - txt.get_width()//2,
                                        Utils.POSITION[i][j][1]+(Utils.BOX-Utils.BOX_PAD)//2 - txt.get_height()//2])

    def grid(self):
        for i in range(5):
            pygame.draw.line(self.win, Color.WHITE,
                             (i*Utils.BOX, 0), (i*Utils.BOX, Utils.HEIGTH))
            pygame.draw.line(self.win, Color.WHITE,
                             (i*Utils.BOX+Utils.BOX_PAD, 0),
                             (i*Utils.BOX+Utils.BOX_PAD, Utils.HEIGTH))
            pygame.draw.line(self.win, Color.WHITE,
                             (0, i*Utils.BOX), (Utils.HEIGTH, i*Utils.BOX))
            pygame.draw.line(self.win, Color.WHITE,
                             (0, i*Utils.BOX+Utils.BOX_PAD),
                             (Utils.HEIGTH, i*Utils.BOX+Utils.BOX_PAD))