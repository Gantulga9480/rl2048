import tensorflow as tf
from tensorflow.keras.layers import Dense, Input, Dropout, Activation
from tensorflow.keras.models import Sequential, load_model, save_model
from tensorflow.keras.optimizers import Adam
from collections import deque
from matplotlib import pyplot as plt
import random
import numpy as np
import os
from datetime import datetime as dt
from old_game.deepgame import DeepGame, Utils

# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Limit GPU memory usage
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)


class ReplayBuffer:

    def __init__(self, size: int) -> None:
        self.size = size
        self.buffer = deque(maxlen=self.size)

    def sample(self, size: int) -> list:
        return random.sample(self.buffer, size)

    def insert(self, state: list) -> None:
        self.buffer.append(state)


class DeepAgent:

    def __init__(self, visual: bool, animate=True) -> None:
        self.visual = visual
        self.game = DeepGame(animate=animate)
        self.epsilon = 0
        self.main_nn = None
        self.target_nn = None

        self.episode = 1

    def step(self, action: int) -> tuple:
        if self.visual:
            self.game.display()
        self.game.eventHandler()
        return self.game.move(action=action)

    def policy(self, state):
        moves, _ = self.game.get_possible_moves()
        if random.random() < self.epsilon and not self.episode % 10:
            return random.choice(moves), True
        return self.game.get_model_moves(self.main_nn.predict(np.expand_dims(state, axis=0))[0])


class Trainer(DeepAgent):

    def __init__(self, visual: bool, animate: bool) -> None:
        super().__init__(visual=visual, animate=animate)
        self.target_net_update = 30
        self.epochs = 20
        self.batch_size = 512
        self.min_buffer_size = 1000
        self.learning_rate = 0.001
        self.min_epsilon = 0
        self.ep_decay = 0.9999
        self.gamma = 0.7
        self.input_shape = 16
        self.output_shape = Utils.ACTION_SPACE

        self.fit_count = 0
        self.ep_reward_hist = []
        self.ep_reward = 0

        policy = tf.keras.mixed_precision.Policy('mixed_float16')
        tf.keras.mixed_precision.set_global_policy(policy)
        print('Compute dtype: %s' % policy.compute_dtype)
        print('Variable dtype: %s' % policy.variable_dtype)

        self.update_count = 0

    def create_model(self, name: str) -> Sequential:
        model = Sequential(name=name)
        model.add(Input(shape=(self.input_shape, ),
                        batch_size=self.batch_size))
        model.add(Dense(128))
        model.add(Activation('tanh'))
        model.add(Dense(64))
        model.add(Activation('tanh'))
        model.add(Dense(32))
        model.add(Activation('tanh'))
        model.add(Dense(16))
        model.add(Activation('tanh'))
        model.add(Dense(self.output_shape))
        model.add(Activation('linear', dtype='float32'))
        model.compile(loss='mse',
                      optimizer=Adam(learning_rate=self.learning_rate),
                      metrics=['accuracy'])
        model.summary()
        return model

    def fit(self, data) -> None:
        self.main_nn.fit(np.array(data[0]), np.array(data[1]),
                         epochs=self.epochs, batch_size=self.batch_size,
                         shuffle=False, verbose=2)

    def set_weight(self):
        self.target_nn.set_weights(self.main_nn.get_weights())

    def prepare_data(self, samples: list) -> tuple:
        state = np.array([item[0] for item in samples])
        state_ = np.array([item[2] for item in samples])
        current_q = self.main_nn.predict(state)
        future_q = self.target_nn.predict(state_)

        x = []
        y = []
        for index, (state, action, _, reward, done) in enumerate(samples):
            if not done:
                new_q = reward + self.gamma * np.max(future_q[index])
            else:
                new_q = reward

            current_qs = current_q[index]
            current_qs[action] = new_q

            x.append(state)
            y.append(current_qs)
        return x, y


def main():
    buffer = ReplayBuffer(5000)
    trainer = Trainer(visual=True, animate=False)

    try:
        trainer.main_nn = load_model('main.h5')
        trainer.target_nn = load_model('main.h5')
        print('LOADING MODEL')
    except Exception:
        trainer.main_nn = trainer.create_model('main')
        trainer.target_nn = trainer.create_model('target')
        trainer.set_weight()

    while trainer.game.running:
        state = trainer.game.reset()
        trainer.ep_reward = 0
        trainer.epsilon = 0
        trainer.episode += 1
        while not trainer.game.over:
            action, _ = trainer.policy(state)
            over, state_, reward = trainer.step(action=action)
            buffer.insert([state, action, state_, reward/2048, over])
            state = state_
            # trainer.epsilon = max(trainer.min_epsilon, trainer.epsilon*trainer.ep_decay)
            # trainer.epsilon += 0.001
            trainer.ep_reward += reward
            if len(buffer.buffer) >= trainer.min_buffer_size:
                trainer.fit(trainer.prepare_data(buffer.sample(trainer.batch_size)))
                trainer.fit_count += 1
            # if over:
            if trainer.fit_count == trainer.target_net_update:
                trainer.set_weight()
                trainer.fit_count = 0
                # trainer.update_count = 0
            trainer.game.set_caption('eps: ' + str(trainer.epsilon) + ' ep_r: ' + str(trainer.ep_reward) + ' ep: ' + str(trainer.episode))
        trainer.ep_reward_hist.append(trainer.ep_reward)

    plt.plot(trainer.ep_reward_hist)
    plt.ylabel('REWARD')
    plt.xlabel('EPISODE')
    plt.show()

    save_model(trainer.main_nn, 'model_' + str(trainer.episode) + '_' + str(max(trainer.ep_reward_hist)) + '_' + str(dt.now()).split(' ')[0] + '.h5')


if __name__ == '__main__':
    main()
