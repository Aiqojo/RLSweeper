import gym
from stable_baselines3 import PPO
import os
import time
from RLSweeperEnv import RLSweeperEnv

load = False

models_dir = f"models/PPO1"
logdir = f"logs/PPO1"

models_path = f"{models_dir}/8400000.zip"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = RLSweeperEnv()
env.reset()

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 5000
for i in range(1, 100000):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/{TIMESTEPS*i}")

    if load:
        env_load = RLSweeperEnv()
        env_load.reset()

        load_path = f"{models_dir}/{TIMESTEPS*i}.zip"

        model = PPO.load(load_path, env = env_load)

        reward_array = []

        episodes = 4
        for ep in range(episodes):
            obs = env_load.reset()
            done = False
            while not done:
                time.sleep(.02)
                env_load.render()
                action, _ = model.predict(obs)
                obs, reward, done, info = env_load.step(action)
                #print(np.fliplr(np.rot90(m=obs, k=3)))
                print(reward)
            reward_array += [reward]

        env_load.close()

env.close()