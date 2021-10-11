from game import Game
import os
import numpy as np
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from keras.models import load_model



game = Game(animate=False)
model = load_model('model_14752_2021-09-30_deep6_undo_failed.h5')

count = 0

while game.running:
    state = game.reset()
    while not game.over:
        game.display()
        game.eventHandler()
        count += 1
        if count == 50:
            action = game.get_model_moves(model.predict(np.expand_dims(state, axis=0))[0])
            _, state, _ = game.move(action=action)
            count = 0
