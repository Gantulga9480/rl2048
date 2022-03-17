from old_game.game import Game, Utils
import numpy as np
import copy


class DeepGame(Game):

    def __init__(self, animate: bool) -> None:
        super().__init__(animate)

    def get_model_moves(self, q_vals):
        _, mask = self.get_possible_moves()
        # selected_action = np.argmax(q_vals)
        # return selected_action, mask[selected_action]
        q_vals = Utils.mask_array(q_vals, mask)
        return np.argmax(q_vals), True

    def get_state(self):
        return self.board.get_board().flatten()

    def move(self, action: int) -> tuple:
        prev_score = self.board.score
        reward = 0
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
                if not self.board.is_full():
                    self.board.generate()
                self.over = self.board.check()
                if self.over:
                    reward = -1 * self.board.score
                    # reward = 0
                else:
                    reward = self.board.score - prev_score
            else:
                reward = -1 * self.last_reward
            self.last_reward = reward
            return self.over, self.get_state(), reward
        return False
