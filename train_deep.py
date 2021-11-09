import tensorflow as tf
from tensorflow.keras.layers import Dense, Input, Dropout, Activation
from tensorflow.keras.models import Sequential, load_model, save_model
from tensorflow.keras.optimizers import Adam
from collections import deque
from matplotlib import pyplot as plt
import random
import numpy as np
from datetime import datetime as dt
from deepgame import DeepGame, Utils


class ReplayBuffer:

    def __init__(self, size: int) -> None:
        self.size = size
        self.buffer = deque(maxlen=self.size)

    def sample(self, size: int) -> list:
        return random.sample(self.buffer, size)

    def insert(self, state: list) -> None:
        self.buffer.append(state)


class Agent:

    def __init__(self, visual: bool, event: bool, animate=True) -> None:
        self.visual = visual
        self.event = event
        self.game = DeepGame(animate=animate)
        self.epsilon = 1
        self.main_nn = None
        self.target_nn = None

    def step(self, action: int) -> tuple:
        if self.visual:
            self.game.display()
        if self.event:
            self.game.eventHandler()
        return self.game.move(action=action)

    def get_action(self, state):
        moves, mask = self.game.get_possible_moves()
        if random.random() < self.epsilon:
            return moves[random.randint(0, len(moves)-1)]
        else:
            return self.game.get_model_moves(self.main_nn.predict(np.expand_dims(state, axis=0))[0])


class Trainer(Agent):

    def __init__(self, visual: bool, event: bool, animate: bool) -> None:
        super().__init__(visual=visual, event=event, animate=animate)
        self.target_net_update = 10
        self.epochs = 10
        self.batch_size = 128
        self.min_buffer_size = 1000
        self.learning_rate = 0.001
        self.min_epsilon = 0
        self.ep_decay = 0.9999
        self.gamma = 0.9
        self.input_shape = 16
        self.output_shape = Utils.ACTION_SPACE

        policy = tf.keras.mixed_precision.Policy('mixed_float16')
        tf.keras.mixed_precision.set_global_policy(policy)
        print('Compute dtype: %s' % policy.compute_dtype)
        print('Variable dtype: %s' % policy.variable_dtype)

        self.update_count = 0

    def create_model(self, name: str) -> Sequential:
        model = Sequential(name=name)
        model.add(Input(shape=(self.input_shape, ),
                        batch_size=self.batch_size))
        model.add(Dense(self.input_shape))
        model.add(Activation('relu'))
        model.add(Dense(32))
        model.add(Activation('relu'))
        model.add(Dense(10))
        model.add(Dropout(0.1))
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
    trainer = Trainer(visual=True, event=True, animate=False)

    try:
        print('LOADING MODEL')
        trainer.main_nn = load_model('main.h5')
        trainer.target_nn = load_model('main.h5')
    except Exception:
        trainer.main_nn = trainer.create_model('main')
        trainer.target_nn = trainer.create_model('target')
        trainer.set_weight()

    ep_reward_hist = []
    ep_reward = 0

    while trainer.game.running:
        state = trainer.game.reset()
        ep_reward = 0
        while not trainer.game.over:
            action = trainer.get_action(state)
            over, state_, reward = trainer.step(action=action)
            buffer.insert([state, action, state_, reward, over])
            state = state_
            trainer.epsilon = max(trainer.min_epsilon,
                                  trainer.epsilon*trainer.ep_decay)
            ep_reward += reward
            if len(buffer.buffer) >= trainer.min_buffer_size:
                trainer.fit(trainer.prepare_data(buffer.sample(trainer.batch_size)))
                trainer.update_count += 1
            if over:
                trainer.set_weight()
                trainer.update_count += 1
            trainer.game.title('eps: ' + str(trainer.epsilon) + ' ep_r: ' + str(ep_reward))
        ep_reward_hist.append(ep_reward)

    plt.plot(ep_reward_hist)
    plt.ylabel('REWARD')
    plt.xlabel('EPISODE')
    plt.show()

    save_model(trainer.main_nn, 'model_' + str(max(ep_reward_hist)) + '_' + str(dt.now()).split(' ')[0] + '.h5')


if __name__ == '__main__':
    main()
