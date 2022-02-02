from deepgame import DeepGame
import os
import numpy as np
from keras.models import load_model
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


game = DeepGame(animate=True)
model = load_model('model_934_6080_2021-12-07.h5')

count = 0

while game.running:
    state = game.reset()
    while not game.over:
        game.display()
        game.eventHandler()
        count += 1
        if count == 50:
            action, _ = game.get_model_moves(model.predict(np.expand_dims(state, axis=0))[0])
            _, state, _ = game.move(action=action)
            count = 0
