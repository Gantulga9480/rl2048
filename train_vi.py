# TODO Value Iteration
from vigame import ViGame
from matplotlib import pyplot as plt

game = ViGame(animate=False)

try:
    game.load_table('table.json')
except Exception:
    game.q_table = dict()


def main():
    ep_rew = []
    while game.running:
        r = 0
        state = game.reset()
        while not game.over:
            action = game.get_action(state)
            over, state_, reward = game.step(action)
            game.update(over, state, action, reward, state_)
            state = state_
            r += reward
            game.set_caption(f'{game.epsilon}, {game.episode}')
        ep_rew.append(r)
    game.save_table('table')
    plt.plot(ep_rew)
    plt.ylabel('REWARD')
    plt.xlabel('EPISODE')
    plt.show()


def play():
    while game.running:
        state = game.reset()
        while not game.over:
            action = game.get_action(state)
            _, state_, _ = game.step(action)
            state = state_


if __name__ == '__main__':
    main()
else:
    pass
