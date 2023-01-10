from py2048 import Py2048, UP, DOWN, LEFT, RIGHT, UNDO
import pygame as pg
import numpy as np


class Deep2048(Py2048):

    ACTION_SPACE = [UP, DOWN, LEFT, RIGHT, UNDO]
    STATE_SPACE = [0, ] * 17

    def __init__(self) -> None:
        super().__init__()
        self.set_title(self.title)
        self.set_window()

    def onEvent(self, event) -> None:
        super().onEvent(event)
        if event.type == pg.KEYUP:
            if event.key == pg.K_q:
                self.over = True
                self.running = False
            elif event.key == pg.K_SPACE:
                self.rendering = not self.rendering

    def reset(self):
        super().reset()
        state = self.game_board.get().flatten().tolist()
        state.append(-1)
        return state

    def step(self, dir):
        last_score = self.game_board.score
        super().step(dir)
        self.loop_once()
        reward = self.game_board.score - last_score
        state = self.game_board.get().flatten().tolist()
        state.append(dir)
        return state, reward, self.over

    def get_masked_action(self, q_vals):
        a_min = np.min(q_vals) - 1
        # not include UNDO
        for i in range(len(self.ACTION_SPACE)):
            try:
                self.game_board.possible_actions.index(i)
            except ValueError:
                q_vals[i] = a_min
        return np.argmax(q_vals)


if __name__ == '__main__':
    Deep2048().loop_forever()
