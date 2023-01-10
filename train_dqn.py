from deep2048 import Deep2048
from RL.dqn import DQN
from matplotlib import pyplot as plt


sim = Deep2048()
model = DQN(sim.ACTION_SPACE, 0.001, 0.99)
model.create_model([sim.STATE_SPACE.__len__(), 100, 100, sim.ACTION_SPACE.__len__()], epochs=3)
model.create_buffer(5000, model.batchs)

while sim.running:
    state = sim.reset()
    while not sim.over:
        action = model.policy(state)
        n_state, reward, over = sim.step(action)

        if n_state:
            model.learn(state, action, n_state, reward, over)
            state = n_state

    info = ' '.join([f'e: {model.e}', f'r: {model.reward_history["episode_reward"][-1]}'])
    print(info)


print()
plt.plot(model.reward_history['episode_reward'])
plt.show()
