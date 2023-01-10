import tensorflow as tf
from py2048 import Py2048
import numpy as np


class Deep2048Bot(Py2048):

    def __init__(self) -> None:
        super().__init__()
        self.model = tf.keras.models.load_model('deepmodel/model.h5')

    def loop(self):
        state = self.game_board.get().flatten()
        action_values = self.model.predict(np.expand_dims(state, axis=0))[0]
        action = self.get_masked_action(action_values)
        self.step(action)

    def get_masked_action(self, q_vals):
        a_min = np.min(q_vals) - 1
        # not include UNDO
        for i in range(4):
            try:
                self.game_board.possible_actions.index(i)
            except ValueError:
                q_vals[i] = a_min
        return np.argmax(q_vals)


if __name__ == '__main__':
    t = Deep2048Bot()
    t.mainloop()
