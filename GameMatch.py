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
    def __init__(self,diff,callback):
        self.callback = callback
        self.tutorial = False
        #Tutorial Mode is set as diff -1
        if diff == -1:
            diff = 2
            self.tutorial = True
        self.difficulties = ["streetFighter-ppo-1k","streetFighter-ppo-10k","streetFighter-ppo-400k","streetFighter-ppo-600k","streetFighter-ppo-700k"]
        self.moments = [[],[]]
        self.env_id = "StreetFighterIISpecialChampionEdition-Genesis"
        self.env = retro.make(self.env_id, state='2p', players=2)
        self.obs = self.env.reset()
        self.model = PPO.load(self.difficulties[diff])
        self.matchNr = 0
        self.actionFrame = 0
        self.butts = ['B', 'A', 'MODE', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'C', 'Y', 'X', 'Z']
        self.action_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.a2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.enemyWon = 0
        self.matchesWon = 0
        self.ended = False
        skipFirst = True
        while skipFirst:
            a2, _ = self.model.predict(self.obs)
            a2 = a2.tolist()

            act = a2 + self.action_array
            self.obs, rew, done, info = self.env.step(act)
            self.enemyWon = info['enemy_matches_won']
            if info['matches_won'] == 1:
                skipToNext = True
                while skipToNext:
                    self.obs, rew, done, info = self.env.step(act)
                    if info['health'] == 176:
                        skipToNext = False
                skipFirst = False
                self.matchesWon = 1

    def getPlaying(self):
        return self.matchNr == 2 and self.actionFrame >= 500

    def getMatchNumber(self):
        return self.matchNr

    def getObs(self):
        return self.obs

    def closeMatch(self):
        self.env.close()

    def renderFrame(self, events):
        if self.ended:
            return
        # j = pygame.joystick.Joystick(1)
        # j.init()


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
        if not self.tutorial:
            a2, _ = self.model.predict(self.obs)
            a2 = a2.tolist()
        else:
            a2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        act = a2 + self.action_array

        # for 2 Models
        # a3, _ = model2.predict(obs)
        # act = a2.tolist() + a3.tolist()

        # Progress Environemt forward
        self.obs, rew, done, info = self.env.step(act)

        # if info['matches_won'] == 1 and self.actionFrame == 500:
        #     displaying = True

        #['health'] / ['enemy_health']
        #collect data from the moments of the game
        if not self.tutorial:
            if self.actionFrame % 30 == 0:
                self.moments[0].append(info['health'])
                self.moments[1].append(info['enemy_health'])
            if info['matches_won'] == 2:
                self.ended = True
                self.env.close()
                self.callback(0, self.actionFrame, self.moments)
            elif info['enemy_matches_won'] == self.enemyWon+1:
                self.ended = True
                self.env.close()
                self.callback(1,self.actionFrame, self.moments)
        else:
            if info['matches_won'] == 2 or info['enemy_matches_won'] == self.enemyWon + 1:
                self.reset()
        self.actionFrame += 1

    def reset(self):
        self.obs = self.env.reset()
        self.enemyWon = 0
        self.matchesWon = 0
        self.ended = False
        self.action_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.a2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.actionFrame = 0
        skipFirst = True
        while skipFirst:
            a2, _ = self.model.predict(self.obs)
            a2 = a2.tolist()

            act = a2 + self.action_array
            self.obs, rew, done, info = self.env.step(act)
            self.enemyWon = info['enemy_matches_won']
            if info['matches_won'] == 1:
                skipToNext = True
                while skipToNext:
                    self.obs, rew, done, info = self.env.step(act)
                    if info['health'] == 176:
                        skipToNext = False
                skipFirst = False
                self.matchesWon = 1