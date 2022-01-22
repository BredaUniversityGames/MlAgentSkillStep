import gym
import retro
import retrowrapper
import pygame

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env

from GameMatch import GameMatch

newGame = GameMatch(0)
newGame.startGame()

env_id= "StreetFighterIISpecialChampionEdition-Genesis"
env = retro.make(env_id, state='2p', players=2)
obs = env.reset()
# env = SubprocVecEnv([retro.make(env_id, state='Champion.Level1.RyuVsGuile') for i in range(n_cpus)])

# model = PPO("MlpPolicy", env, verbose=1)
# # # model = PPO.load("streetFighter-ppo-100k")
# for i in range(100):
#  model.learn(total_timesteps=500000)
#  model.save("streetFighter-ppo-500k")
model = PPO.load("streetFighter-ppo-500k")

# for i in range(100000):
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action)
#     env.render()
#     if done:
#       obs = env.reset()
#
# env.close()
