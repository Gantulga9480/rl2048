from .Game import Game
from .game_core import Board, Engine
from .game_core import UP, DOWN, LEFT, RIGHT, UNDO, INPLACE
from .utils import Colors
import pygame as pg


class Py2048(Game):

    TITLE = r'2048'
    WIDTH = 410
    HEIGTH = WIDTH
    BOX_PAD = WIDTH % 100
    BOX = (WIDTH - BOX_PAD) // 4
    FPS = 60
    SPEED_FACTOR = 8  # higher value means faster animation
    SPEED_FAST = (WIDTH - BOX - BOX_PAD) // (FPS // SPEED_FACTOR)
    SPEED_MEDIUM = (WIDTH - BOX * 2 - BOX_PAD) // (FPS // SPEED_FACTOR)
    SPEED_SLOW = (WIDTH - BOX * 3 - BOX_PAD) // (FPS // SPEED_FACTOR)
    SPEEDS = [1, SPEED_SLOW, SPEED_MEDIUM, SPEED_FAST]
    POSITION = [[[BOX_PAD + BOX * 0, BOX_PAD + BOX * 0],
                 [BOX_PAD + BOX * 1, BOX_PAD + BOX * 0],
                 [BOX_PAD + BOX * 2, BOX_PAD + BOX * 0],
                 [BOX_PAD + BOX * 3, BOX_PAD + BOX * 0]],
                [[BOX_PAD + BOX * 0, BOX_PAD + BOX * 1],
                 [BOX_PAD + BOX * 1, BOX_PAD + BOX * 1],
                 [BOX_PAD + BOX * 2, BOX_PAD + BOX * 1],
                 [BOX_PAD + BOX * 3, BOX_PAD + BOX * 1]],
                [[BOX_PAD + BOX * 0, BOX_PAD + BOX * 2],
                 [BOX_PAD + BOX * 1, BOX_PAD + BOX * 2],
                 [BOX_PAD + BOX * 2, BOX_PAD + BOX * 2],
                 [BOX_PAD + BOX * 3, BOX_PAD + BOX * 2]],
                [[BOX_PAD + BOX * 0, BOX_PAD + BOX * 3],
                 [BOX_PAD + BOX * 1, BOX_PAD + BOX * 3],
                 [BOX_PAD + BOX * 2, BOX_PAD + BOX * 3],
                 [BOX_PAD + BOX * 3, BOX_PAD + BOX * 3]]]

    def __init__(self) -> None:
        super().__init__()
        self.title = self.TITLE
        self.size = (self.WIDTH, self.HEIGTH)
        self.fps = self.FPS
        self.font = pg.font.SysFont("arial", 30, True)
        self.over = False
        self.color = Colors()
        self.game_board = Board()
        self.game_engine = Engine()
        self.game_engine.get_possible_actions(self.game_board)

    def onEvent(self, event) -> None:
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                self.step(UP)
            elif event.key == pg.K_DOWN:
                self.step(DOWN)
            elif event.key == pg.K_LEFT:
                self.step(LEFT)
            elif event.key == pg.K_RIGHT:
                self.step(RIGHT)
            elif event.key == pg.K_u:
                self.step(UNDO)
            elif event.key == pg.K_r:
                self.reset()

    def step(self, dir):
        if dir in self.game_board.possible_actions:
            self.game_engine.move(self.game_board, dir)
        else:
            print('Impossible move!')
        self.over = not self.game_board.available()

    def reset(self):
        self.game_engine.reset()
        self.game_board.reset()
        self.game_engine.get_possible_actions(self.game_board)

    def onRender(self) -> None:
        self.window.fill(self.color.BG)
        self.draw_board(animation=True)
        if self.over:
            self.draw_end_screen()

    def draw_board(self, animation=False):
        if not animation or not self.game_engine.changed:
            for i in range(self.game_board.BOARD_SHAPE[0]):
                for j in range(self.game_board.BOARD_SHAPE[1]):
                    node_value = self.game_board[i, j]
                    pg.draw.rect(self.window, self.color[node_value],
                                 pg.Rect(*self.POSITION[i][j],
                                         self.BOX - self.BOX_PAD,
                                         self.BOX - self.BOX_PAD),
                                 0, 7)
                    if node_value != 0:
                        if node_value < 4096:
                            txt = self.font.render(str(node_value),
                                                   1, (0, 0, 0))
                        else:
                            txt = self.font.render(str(node_value),
                                                   1, (255, 255, 255))
                        self.window.blit(txt, [self.POSITION[i][j][0] + (self.BOX - self.BOX_PAD) // 2 - txt.get_width() // 2, self.POSITION[i][j][1] + (self.BOX - self.BOX_PAD) // 2 - txt.get_height() // 2])
            return
        animation_list = []
        for change in self.game_board.changes:
            distance = abs(change[0][0] - change[1][0]) + \
                abs(change[0][1] - change[1][1])
            speed = self.SPEEDS[distance]
            diraction = change[2]
            start_x = change[0][1] * self.BOX + self.BOX_PAD
            start_y = change[0][0] * self.BOX + self.BOX_PAD
            stop_x = change[1][1] * self.BOX + self.BOX_PAD
            stop_y = change[1][0] * self.BOX + self.BOX_PAD
            src = [start_x, start_y]
            dest = [stop_x, stop_y]
            animation_list.append([src, diraction, dest, speed])
        done = [False for _ in animation_list]
        while True:
            if all(done):
                self.game_engine.changed = False
                break
            self.window.fill(self.color.BG)
            for i in range(self.game_board.BOARD_SHAPE[0]):
                for j in range(self.game_board.BOARD_SHAPE[1]):
                    pg.draw.rect(self.window, self.color.BOX_EMPTY,
                                 pg.Rect(*self.POSITION[i][j],
                                         self.BOX - self.BOX_PAD,
                                         self.BOX - self.BOX_PAD),
                                 0, 7)
            for ind, blob in enumerate(animation_list):
                if not done[ind]:
                    if blob[1] == UP:
                        animation_list[ind][0][1] -= blob[3]
                    elif blob[1] == DOWN:
                        animation_list[ind][0][1] += blob[3]
                    elif blob[1] == LEFT:
                        animation_list[ind][0][0] -= blob[3]
                    elif blob[1] == RIGHT:
                        animation_list[ind][0][0] += blob[3]
                    elif blob[1] == INPLACE:
                        pass
                    xd = abs(animation_list[ind][2][0] - animation_list[ind][0][0])
                    yd = abs(animation_list[ind][2][1] - animation_list[ind][0][1])
                    if (xd + yd) < blob[3]:
                        done[ind] = True

                i = self.game_board.changes[ind][0][0]
                j = self.game_board.changes[ind][0][1]
                node_value = self.game_board.last_board[i, j]
                x = animation_list[ind][0][0]
                y = animation_list[ind][0][1]
                pg.draw.rect(self.window, self.color[node_value],
                             pg.Rect(x, y,
                                     self.BOX - self.BOX_PAD,
                                     self.BOX - self.BOX_PAD),
                             0, 7)
                if node_value < 4096:
                    txt = self.font.render(str(node_value),
                                           1, (0, 0, 0))
                else:
                    txt = self.font.render(str(node_value),
                                           1, (255, 255, 255))
                self.window.blit(txt, [x + (self.BOX - self.BOX_PAD) // 2 - txt.get_width() // 2, y + (self.BOX - self.BOX_PAD) // 2 - txt.get_height() // 2])
            pg.display.update()
            self.clock.tick(self.FPS)

    def draw_end_screen(self):
        txt = self.font.render('GAME OVER', 1, (0, 0, 0))
        self.window.blit(txt, [self.WIDTH // 2 - txt.get_width() // 2,
                               self.HEIGTH // 2 - txt.get_height() // 2])
