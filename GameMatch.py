

import gym
import retro
import retrowrapper
import pygame

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env


class GameMatch:
    # diff - a number from 0 to 4 representing the level of difficulty
    def __init__(self,diff):
        self.difficulties = ["streetFighter-ppo-500k"]
        self.env_id = "StreetFighterIISpecialChampionEdition-Genesis"
        self.env = retro.make(self.env_id, state='2p', players=2)
        self.obs = self.env.reset()
        self.model = PPO.load(self.difficulties[diff])

    def startGame(self):
        playing= True
        displaying = False

        pygame.init()
        win = pygame.display.set_mode((800, 600))

        # j = pygame.joystick.Joystick(1)
        # j.init()

        clock = pygame.time.Clock()

        butts = ['B', 'A', 'MODE', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'C', 'Y', 'X', 'Z']

        action_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        a2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        actionFrame = 0
        while playing:

            actions = set()

            # Display
            if displaying :
                img = pygame.image.frombuffer(self.obs.tostring(), self.obs.shape[1::-1], "RGB")
                img = pygame.transform.scale(img, (800, 600))
                win.blit(img, (0, 0))
                pygame.display.flip()

            # Control Events

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():

                if keys[pygame.K_RIGHT]:
                    actions.add('RIGHT')
                if keys[pygame.K_LEFT]:
                    actions.add('LEFT')
                if keys[pygame.K_DOWN]:
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
            a2, _ = self.model.predict(self.obs)
            a2 = a2.tolist()

            act = a2 + action_array

            # for 2 Models
            # a3, _ = model2.predict(obs)
            # act = a2.tolist() + a3.tolist()

            # Progress Environemt forward
            self.obs, rew, done, info = self.env.step(act)
            if info['matches_won'] == 1 and actionFrame == 500:
                displaying = True
            if info['matches_won'] == 2:
                print(info['matches_won'])
                playing = False
            clock.tick(60)
            actionFrame += 1
        self.env.close()
