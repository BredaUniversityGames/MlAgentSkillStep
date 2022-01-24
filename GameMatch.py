import sys

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
        self.matchNr = 0
        self.actionFrame = 0
        self.butts = ['B', 'A', 'MODE', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'C', 'Y', 'X', 'Z']
        self.action_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.a2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def getPlaying(self):
        return self.matchNr == 2 and self.actionFrame >= 500

    def getMatchNumber(self):
        return self.matchNr

    def getObs(self):
        return self.obs

    def closeMatch(self):
        self.env.close()

    def renderFrame(self, events):

        # j = pygame.joystick.Joystick(1)
        # j.init()

        clock = pygame.time.Clock()

        self.actions = set()

        # Display

        # img = pygame.image.frombuffer(self.obs.tostring(), self.obs.shape[1::-1], "RGB")
        # img = pygame.transform.scale(img, (800, 600))
        # win.blit(img, (0, 0))
        # pygame.display.flip()

        # Control Events

        pygame.event.pump()
        keys = pygame.key.get_pressed()

        for event in events:
            if keys[pygame.K_RIGHT]:
                self.actions.add('RIGHT')
            if keys[pygame.K_LEFT]:
                self.actions.add('LEFT')
            if keys[pygame.K_DOWN]:
                self.actions.add('DOWN')
            if keys[pygame.K_UP]:
                self.actions.add('UP')

            if keys[pygame.K_z]:
                self.actions.add('A')
            if keys[pygame.K_x]:
                self.actions.add('B')
            if keys[pygame.K_c]:
                self.actions.add('C')
            if keys[pygame.K_a]:
                self.actions.add('X')
            if keys[pygame.K_s]:
                self.actions.add('Y')
            if keys[pygame.K_d]:
                self.actions.add('Z')

            for i, a in enumerate(self.butts):
                if a in self.actions:
                    self.action_array[i] = 1
                else:
                    self.action_array[i] = 0

        # if actionFrame == 4:
        #     actionFrame = 0

        a2, _ = self.model.predict(self.obs)
        a2 = a2.tolist()

        act = a2 + self.action_array

        # for 2 Models
        # a3, _ = model2.predict(obs)
        # act = a2.tolist() + a3.tolist()

        # Progress Environemt forward
        self.obs, rew, done, info = self.env.step(act)
        # if info['matches_won'] == 1 and self.actionFrame == 500:
        #     displaying = True
        # if info['matches_won'] == 2:
        #     print(info['matches_won'])
        #     playing = False
        clock.tick(60)
        self.actionFrame += 1

