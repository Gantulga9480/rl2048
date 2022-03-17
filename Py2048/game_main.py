from PyGame import PyGame
from PyGame.utils import INFO, WARNING, ERROR, DEBUG
from .game_core import Node, Board, Engine
from .game_core import UP, DOWN, LEFT, RIGHT, UNDO, INPLACE
from .utils import Colors, pygame


class Py2048(PyGame):

    TITLE = r'2048'
    WIDTH = 410
    HEIGTH = WIDTH
    BOX_PAD = WIDTH % 100
    BOX = (WIDTH - BOX_PAD) // 4
    FPS = 120
    SPEED_FAST = (WIDTH - BOX - BOX_PAD) // (FPS//10)
    SPEED_MEDIUM = (WIDTH - BOX * 2 - BOX_PAD) // (FPS//10)
    SPEED_SLOW = (WIDTH - BOX * 3 - BOX_PAD) // (FPS//10)
    SPEEDS = [1, SPEED_SLOW, SPEED_MEDIUM, SPEED_FAST]
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

    def __init__(self,
                 title: str = TITLE,
                 width: int = WIDTH,
                 height: int = HEIGTH,
                 fps: int = FPS,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)
        self.font = pygame.font.SysFont("arial", 30, True)
        self.over = False
        self.game_board = Board()
        self.game_engine = Engine()
        self.color = Colors()

    def USR_setup(self):
        self.backgroundColor = self.color.BG
        self.game_engine.get_possible_moves(self.game_board)

    def USR_eventHandler(self):
        for event in self.events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.step(UP)
                elif event.key == pygame.K_DOWN:
                    self.step(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.step(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.step(RIGHT)
                elif event.key == pygame.K_u:
                    self.step(UNDO)
                elif event.key == pygame.K_r:
                    self.game_board.reset()

    def step(self, dir):
        if dir in self.game_board.possible_moves:
            self.game_engine.move(self.game_board, dir)
        else:
            self.LOG('Impossible move!')
        self.over = not self.game_board.available()

    def USR_render(self):
        if self.rendering:
            if not self.over:
                self.draw_board(animation=True)
            elif self.over:
                self.draw_end_screen()

    def draw_board(self, animation=False):
        if not animation or self.game_board.changes.__len__() == 0:
            for i in range(self.game_board.BOARD_SHAPE[0]):
                for j in range(self.game_board.BOARD_SHAPE[1]):
                    node_value = self.game_board[i, j]
                    pygame.draw.rect(self.game_window, self.color[node_value],
                                     pygame.Rect(*self.POSITION[i][j],
                                                 self.BOX-self.BOX_PAD,
                                                 self.BOX-self.BOX_PAD),
                                     0, 7)
                    if node_value != 0:
                        if node_value < 4096:
                            txt = self.font.render(str(node_value),
                                                   1, self.color.BLACK)
                        else:
                            txt = self.font.render(str(node_value),
                                                   1, self.color.WHITE)
                        self.game_window.blit(txt, [self.POSITION[i][j][0] +
                                                    (self.BOX-self.BOX_PAD)//2
                                                    - txt.get_width()//2,
                                                    self.POSITION[i][j][1] +
                                                    (self.BOX-self.BOX_PAD)//2
                                                    - txt.get_height()//2])
            return
        animation_list = []
        for change in self.game_board.changes:
            distance = abs(change[0][0] - change[1][0]) + \
                abs(change[0][1] - change[1][1])
            speed = self.SPEEDS[distance]
            diraction = change[2]
            start_x = change[0][1]*self.BOX + self.BOX_PAD
            start_y = change[0][0]*self.BOX + self.BOX_PAD
            stop_x = change[1][1]*self.BOX + self.BOX_PAD
            stop_y = change[1][0]*self.BOX + self.BOX_PAD
            src = [start_x, start_y]
            dest = [stop_x, stop_y]
            animation_list.append([src, diraction, dest, speed])
        done = [False for _ in animation_list]
        while True:
            if all(done):
                self.game_board.changes.clear()
                break
            self.game_window.fill(self.color.BG)
            for i in range(self.game_board.BOARD_SHAPE[0]):
                for j in range(self.game_board.BOARD_SHAPE[1]):
                    pygame.draw.rect(self.game_window, self.color.BOX_EMPTY,
                                     pygame.Rect(*self.POSITION[i][j],
                                                 self.BOX-self.BOX_PAD,
                                                 self.BOX-self.BOX_PAD),
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
                    xd = abs(animation_list[ind][2][0] -
                             animation_list[ind][0][0])
                    yd = abs(animation_list[ind][2][1] -
                             animation_list[ind][0][1])
                    if (xd + yd) < blob[3]:
                        done[ind] = True

                i = self.game_board.changes[ind][0][0]
                j = self.game_board.changes[ind][0][1]
                node_value = self.game_board.last_board[i, j]
                x = animation_list[ind][0][0]
                y = animation_list[ind][0][1]
                pygame.draw.rect(self.game_window, self.color[node_value],
                                 pygame.Rect(x, y,
                                             self.BOX-self.BOX_PAD,
                                             self.BOX-self.BOX_PAD),
                                 0, 7)
                if node_value < 4096:
                    txt = self.font.render(str(node_value),
                                           1, self.color.BLACK)
                else:
                    txt = self.font.render(str(node_value),
                                           1, self.color.WHITE)
                self.game_window.blit(txt, [x + (self.BOX-self.BOX_PAD)//2
                                            - txt.get_width()//2,
                                            y + (self.BOX-self.BOX_PAD)//2
                                            - txt.get_height()//2])
            pygame.display.update()
            self.clock.tick(self.FPS)

    def draw_end_screen(self):
        txt = self.font.render('GAME OVER', 1, self.color.BLACK)
        self.game_window.blit(txt, [self.WIDTH//2 - txt.get_width()//2,
                                    self.HEIGTH//2 - txt.get_height()//2])
