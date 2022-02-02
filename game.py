import pygame
import random
import numpy as np
import copy
import math  # test


class Utils:

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    UNDO = 4

    ACTION_SPACE = 4

    WIDTH = 410
    HEIGTH = WIDTH
    BOX_PAD = WIDTH % 100
    BOX = (WIDTH - BOX_PAD) // 4
    START_BOX = 2

    FPS = 100

    SPEED_FAST = (WIDTH - BOX - BOX_PAD) // (FPS//10)
    SPEED_MEDIUM = (WIDTH - BOX * 2 - BOX_PAD) // (FPS//10)
    SPEED_SLOW = (WIDTH - BOX * 3 - BOX_PAD) // (FPS//10)

    MOVED = 1
    ADDED = 2
    INPLACE = 0

    ODD = 10

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

    @staticmethod
    def mask_array(array, mask):
        a_min = np.min(array) - 1
        for i, item in enumerate(mask):
            if not item:
                array[i] = a_min
        return array


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

    def __init__(self, value: int) -> None:
        self.value = 0
        self.color = Color.BOX_EMPTY
        self.modified = False
        self.setValue(value)

    def __eq__(self, o: object) -> bool:
        return o.value == self.value

    def __repr__(self) -> str:
        return str(self.value)

    def setValue(self, value: int):
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
        self.score = 0
        self.modified = False
        self.modified_x = 0
        self.modified_y = 0
        self.modified_board = []
        self.generated_box = []
        self.action = Utils.INPLACE
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
                odd = random.randint(1, (100 // Utils.ODD))
                if odd == (100 // Utils.ODD):
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
        self.modified_board = []
        for i in range(3, -1, -1):
            for j in range(4):
                if self.board[j][i].value != 0:
                    self.modified_x = j
                    self.modified_y = i
                    self.action = Utils.INPLACE
                    if i <= 2:
                        self.move_right(j, i)
                    self.modified_board.append([[j, i], [self.modified_x,
                                                         self.modified_y],
                                                Utils.RIGHT,
                                                self.action])
        self.mod_reset()
        return self.modified

    def move_right(self, x: int, y: int) -> None:
        if self.board[x][y] == self.board[x][y+1] and \
                not self.board[x][y+1].modified:
            self.board[x][y+1].modified = True
            self.board[x][y+1].setValue(self.board[x][y].value*2)
            self.board[x][y].setValue(0)
            self.modified = True
            self.modified_x = x
            self.modified_y = y + 1
            self.action = Utils.ADDED
            self.score += self.board[x][y+1].value
        elif self.board[x][y+1].value == 0:
            self.board[x][y+1].setValue(self.board[x][y].value)
            self.board[x][y].setValue(0)
            self.modified = True
            self.modified_x = x
            self.modified_y = y + 1
            self.action = Utils.MOVED
            if y <= 1:
                self.move_right(x, y+1)

    def left(self):
        self.modified = False
        self.modified_board = []
        for i in range(4):
            for j in range(4):
                if self.board[j][i].value != 0:
                    self.modified_x = j
                    self.modified_y = i
                    self.action = Utils.INPLACE
                    if i >= 1:
                        self.move_left(j, i)
                    self.modified_board.append([[j, i], [self.modified_x,
                                                         self.modified_y],
                                                Utils.LEFT,
                                                self.action])
        self.mod_reset()
        return self.modified

    def move_left(self, x: int, y: int):
        if self.board[x][y] == self.board[x][y-1] and \
                not self.board[x][y-1].modified:
            self.board[x][y-1].setValue(self.board[x][y].value*2)
            self.board[x][y].setValue(0)
            self.board[x][y-1].modified = True
            self.modified = True
            self.modified_x = x
            self.modified_y = y - 1
            self.action = Utils.ADDED
            self.score += self.board[x][y-1].value
        elif self.board[x][y-1].value == 0:
            self.board[x][y-1].setValue(self.board[x][y].value)
            self.board[x][y].setValue(0)
            self.modified = True
            self.modified_x = x
            self.modified_y = y - 1
            self.action = Utils.MOVED
            if y >= 2:
                self.move_left(x, y-1)

    def up(self):
        self.modified = False
        self.modified_board = []
        for i in range(4):
            for j in range(4):
                if self.board[j][i].value != 0:
                    self.modified_x = j
                    self.modified_y = i
                    self.action = Utils.INPLACE
                    if j >= 1:
                        self.move_up(j, i)
                    self.modified_board.append([[j, i], [self.modified_x,
                                                         self.modified_y],
                                                Utils.UP,
                                                self.action])
        self.mod_reset()
        return self.modified

    def move_up(self, x: int, y: int):
        if self.board[x][y] == self.board[x-1][y] and \
                not self.board[x-1][y].modified:
            self.board[x-1][y].modified = True
            self.board[x-1][y].setValue(self.board[x][y].value*2)
            self.board[x][y].setValue(0)
            self.modified = True
            self.modified_x = x - 1
            self.modified_y = y
            self.action = Utils.ADDED
            self.score += self.board[x-1][y].value
        elif self.board[x-1][y].value == 0:
            self.board[x-1][y].setValue(self.board[x][y].value)
            self.board[x][y].setValue(0)
            self.modified = True
            self.modified_x = x - 1
            self.modified_y = y
            self.action = Utils.MOVED
            if x >= 2:
                self.move_up(x-1, y)

    def down(self):
        self.modified = False
        self.modified_board = []
        for i in range(4):
            for j in range(3, -1, -1):
                if self.board[j][i].value != 0:
                    self.modified_x = j
                    self.modified_y = i
                    self.action = Utils.INPLACE
                    if j <= 2:
                        self.move_down(j, i)
                    self.modified_board.append([[j, i], [self.modified_x,
                                                         self.modified_y],
                                                Utils.DOWN,
                                                self.action])
        self.mod_reset()
        return self.modified

    def move_down(self, x: int, y: int):
        if self.board[x][y] == self.board[x+1][y] and \
                not self.board[x+1][y].modified:
            self.board[x+1][y].modified = True
            self.board[x+1][y].setValue(self.board[x][y].value*2)
            self.board[x][y].setValue(0)
            self.modified = True
            self.modified_x = x + 1
            self.modified_y = y
            self.action = Utils.ADDED
            self.score += self.board[x+1][y].value
        elif self.board[x+1][y].value == 0:
            self.board[x+1][y].setValue(self.board[x][y].value)
            self.board[x][y].setValue(0)
            self.modified = True
            self.modified_x = x + 1
            self.modified_y = y
            self.action = Utils.MOVED
            if x <= 1:
                self.move_down(x+1, y)

    def mod_reset(self):
        for i in range(4):
            for j in range(4):
                self.board[i][j].modified = False


class Game:

    def __init__(self, animate: bool) -> None:
        pygame.init()                               # Initialize pygame module
        self.clock = pygame.time.Clock()                    # Game clock
        self.font = pygame.font.SysFont("arial", 30, True)  # Game font
        self.win = pygame.display.set_mode((Utils.WIDTH,
                                            Utils.HEIGTH))
        self.running = True
        self.over = False
        self.is_moved = False
        self.board = Board()
        self.last_board = None
        self.last_reward = 0
        self.episode = 0
        self.move_count = 0
        self.is_drawing = True
        self.animate = animate

    def display(self) -> None:
        """
        Display game visual to main window
        """
        if self.is_drawing:
            self.win.fill(Color.BG)
            self.drawNums()
            if self.over:
                self.game_over_screen()
            pygame.display.flip()              # draw main window to display
            self.clock.tick(Utils.FPS)

    def eventHandler(self) -> None:
        """
        Event handler for main window
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.over = True
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
                elif event.key == pygame.K_SPACE:
                    self.is_drawing = not self.is_drawing

    def move(self, action: int) -> None:
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
            if action != Utils.UNDO:
                self.last_board = copy.deepcopy(l_board)
                if not self.board.is_full() and not self.over:
                    self.board.generate()
                self.over = self.board.check()

    def reset(self):
        del self.board
        self.board = Board()
        self.last_board = None
        self.last_reward = 0
        self.over = False
        self.move_count = 0
        self.episode += 1
        return self.get_state()

    def get_state(self):
        raise NotImplementedError

    def get_possible_moves(self):
        """ Return index of posible moves with mask """
        moves = []
        mask = []
        l_board = copy.deepcopy(self.board.board)
        for i in range(Utils.ACTION_SPACE):
            is_move = False
            if i == Utils.UP and not self.over:
                is_move = self.board.up()
            elif i == Utils.RIGHT and not self.over:
                is_move = self.board.right()
            elif i == Utils.DOWN and not self.over:
                is_move = self.board.down()
            elif i == Utils.LEFT and not self.over:
                is_move = self.board.left()
            elif i == Utils.UNDO:
                is_move = True if self.last_board is not None else False
            if is_move:
                moves.append(i)
            mask.append(is_move)
            self.board.board = copy.deepcopy(l_board)
        return moves, mask

    def undo(self) -> None:
        if self.last_board is not None:
            self.board.score -= self.last_reward
            self.over = False
            self.board.board = copy.deepcopy(self.last_board)
            self.last_board = None
            return True
        else:
            return False

    def drawNums(self) -> None:
        if not self.is_moved or not self.animate:
            self.is_moved = False
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
        elif self.is_moved and self.animate:
            self.is_moved = False
            animate_list = []
            done = False
            for item in self.board.modified_board:
                speed = 0
                dirs = item[2]
                dist = abs(item[0][0] - item[1][0]) + \
                    abs(item[0][1] - item[1][1])
                if dist == 3:
                    speed = Utils.SPEED_FAST
                elif dist == 2:
                    speed = Utils.SPEED_MEDIUM
                elif dist == 1:
                    speed = Utils.SPEED_SLOW
                start_x = item[0][1]*Utils.BOX + Utils.BOX_PAD
                start_y = item[0][0]*Utils.BOX + Utils.BOX_PAD
                end_x = item[1][1]*Utils.BOX + Utils.BOX_PAD
                end_y = item[1][0]*Utils.BOX + Utils.BOX_PAD
                if speed != 0:
                    animate_list.append([start_x, start_y, end_x,
                                         end_y, speed, dirs, False])
                else:
                    animate_list.append([start_x, start_y, end_x,
                                         end_y, speed, dirs, True])
            while not done:
                done_count = 0
                self.win.fill(Color.BG)
                for i in range(4):
                    for j in range(4):
                        pygame.draw.rect(self.win, Color.BOX_EMPTY,
                                         pygame.Rect(*Utils.POSITION[i][j],
                                                     Utils.BOX-Utils.BOX_PAD,
                                                     Utils.BOX-Utils.BOX_PAD),
                                         0, 7)
                for i, item in enumerate(animate_list):
                    if item[4] != 0:
                        if item[5] == Utils.UP:
                            if not animate_list[i][6]:
                                animate_list[i][1] -= item[4]
                                if abs(item[3] - animate_list[i][1]) < item[4]:
                                    animate_list[i][6] = True
                                    done_count += 1
                            else:
                                done_count += 1
                        elif item[5] == Utils.DOWN:
                            if not animate_list[i][6]:
                                animate_list[i][1] += item[4]
                                if abs(item[3] - animate_list[i][1]) < item[4]:
                                    animate_list[i][6] = True
                                    done_count += 1
                            else:
                                done_count += 1
                        elif item[5] == Utils.RIGHT and not animate_list[i][6]:
                            if not animate_list[i][6]:
                                animate_list[i][0] += item[4]
                                if abs(item[2] - animate_list[i][0]) < item[4]:
                                    animate_list[i][6] = True
                                    done_count += 1
                            else:
                                done_count += 1
                        elif item[5] == Utils.LEFT and not animate_list[i][6]:
                            if not animate_list[i][6]:
                                animate_list[i][0] -= item[4]
                                if abs(item[2] - animate_list[i][0]) < item[4]:
                                    animate_list[i][6] = True
                                    done_count += 1
                            else:
                                done_count += 1
                    else:
                        done_count += 1
                    pygame.draw.rect(self.win, self.last_board[self.board.modified_board[i][0][0]][self.board.modified_board[i][0][1]].color,
                                     pygame.Rect(animate_list[i][0], animate_list[i][1],
                                                 Utils.BOX-Utils.BOX_PAD,
                                                 Utils.BOX-Utils.BOX_PAD), 0, 7)
                    if self.last_board[self.board.modified_board[i][0][0]][self.board.modified_board[i][0][1]].value != 0:
                        if self.last_board[self.board.modified_board[i][0][0]][self.board.modified_board[i][0][1]].value < 4096:
                            txt = self.font.render(str(self.last_board[self.board.modified_board[i][0][0]][self.board.modified_board[i][0][1]].value),
                                                   1, Color.BLACK)
                        else:
                            txt = self.font.render(str(self.last_board[self.board.modified_board[i][0][0]][self.board.modified_board[i][0][1]].value),
                                                   1, Color.WHITE)

                        self.win.blit(txt, [animate_list[i][0]+(Utils.BOX-Utils.BOX_PAD)//2 - txt.get_width()//2,
                                            animate_list[i][1]+(Utils.BOX-Utils.BOX_PAD)//2 - txt.get_height()//2])
                if done_count == len(animate_list):
                    done = True
                    self.board.modified_board = []
                pygame.display.flip()
                self.clock.tick(Utils.FPS)

    def game_over_screen(self) -> None:
        txt = self.font.render('GAME OVER', 1, Color.BLACK)
        self.win.blit(txt, [Utils.WIDTH//2 - txt.get_width()//2,
                            Utils.HEIGTH//2 - txt.get_height()//2])

    def set_caption(self, msg: str):
        pygame.display.set_caption(msg)
