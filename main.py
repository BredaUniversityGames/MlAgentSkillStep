import gym
import retro
import retrowrapper
import pygame

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env




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

pygame.init()
win = pygame.display.set_mode((800, 600))

# j = pygame.joystick.Joystick(1)
# j.init()

clock = pygame.time.Clock()

butts = ['B', 'A', 'MODE', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'C', 'Y', 'X', 'Z']

action_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
a2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
actionFrame = 0
while True:

    actions = set()

    # Display
    img = pygame.image.frombuffer(obs.tostring(), obs.shape[1::-1], "RGB")
    img = pygame.transform.scale(img, (800, 600))
    win.blit(img, (0, 0))
    pygame.display.flip()

    # Control Events

    pygame.event.pump()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        if keys[pygame.K_RIGHT] :
            actions.add('RIGHT')
        if keys[pygame.K_LEFT] :
            actions.add('LEFT')
        if keys[pygame.K_DOWN] :
            actions.add('DOWN')
        if keys[pygame.K_UP]:
            actions.add('UP')

        if keys[pygame.K_z]:
            actions.add('A')
        if keys[pygame.K_x]:
            actions.add('B')
        if keys[pygame.K_c]:
            actions.add('C')
        if keys[pygame.K_a]:
            actions.add('X')
        if keys[pygame.K_s]:
            actions.add('Y')
        if keys[pygame.K_d]:
            actions.add('Z')

        for i, a in enumerate(butts):
            if a in actions:
                action_array[i] = 1
            else:
                action_array[i] = 0

    # if actionFrame == 4:
    #     actionFrame = 0
    a2, _ = model.predict(obs)
    a2 = a2.tolist()

    act =  a2 + action_array

    #for 2 Models
    # a3, _ = model2.predict(obs)
    #act = a2.tolist() + a3.tolist()

    # Progress Environemt forward
    obs, rew, done, info = env.step(act)
    clock.tick(60)
    actionFrame += 1
