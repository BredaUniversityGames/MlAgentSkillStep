import random
import sys

from DataSender import sendEmail
from GUI import GUI
import pygame
import os

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from imgui.integrations.pygame import PygameRenderer
import imgui

from GameMatch import GameMatch
from OpenGLLoader import GL_Image

running = True
logIn = True
stage = 0
matchInProgress = False
enableUI = True
round = 0
match = None
gui = None
tutorial = False
matches = [True,False,False,False,False]
clockFps = None

def initializeDisplay(w, h):
    pygame.display.set_mode((w,h), pygame.DOUBLEBUF | pygame.OPENGL | pygame.OPENGLBLIT)
    imgui.create_context()

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity();
    # this puts us in quadrant 1, rather than quadrant 4
    gluOrtho2D(0, w, h, 0)
    glMatrixMode(GL_MODELVIEW)

    # set up texturing
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def render_init(w,h):
    """Finds the smallest available resolution that fits the desired
    viewfield."""
    pygame.init()
    modelist = pygame.display.list_modes()
    nextmode = [l for l in modelist if l[0]>=w and l[1]>=h]
    bestx, besty = -1,-1
    for l in nextmode:
        if (bestx==-1 or bestx>=l[0]) and (besty==-1 or besty>=l[1]):
            bestx, besty = l[0],l[1]

    print ("resolution: ",bestx, besty)

    initializeDisplay(bestx, besty)

def uiNextHandler():
    global matchInProgress
    if (round<5):
        matchInProgress = not matchInProgress

def tutorialHandler():
    global match
    global matchInProgress
    global tutorial
    if not tutorial:
        tutorial = True
        match.closeMatch()
        match = GameMatch(-1,matchEndedHandler)
        matchInProgress = True
    else:
        tutorial = False
        match.closeMatch()
        match = GameMatch(0, matchEndedHandler)
        matchInProgress = True

def main():
    global match
    global gui
    global clockFps

    render_init(800, 600)
    io = imgui.get_io()
    io.display_size = (800, 600)

    impl = PygameRenderer()
    count = 0
    clock = pygame.time.Clock()
    clockFps = clock
    glLoadIdentity()
    while running:
        count+=1


        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print("result: " + str(clock.get_fps()) + " FPS")
                sys.exit()
            # if you don't wait one frame until you process_event the render will crash
            if count > 1: impl.process_event(event)
        if matchInProgress:
            match.renderFrame(events)
            img = match.getObs()
            img = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")
            img = pygame.transform.scale(img, (800, 600))
            # numpy.shape(pygame.surfarray.array3d(img))
            img = pygame.surfarray.array3d(img)
            img = np.insert(img, 3, 255, axis=2)
            #img = np.flip(img,2)
            #glClearColor(1, 1, 1, 1)
            img = np.swapaxes(img, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if matchInProgress:
            fooimage = GL_Image(img, 800, 600)
            fooimage.draw((0, 0))
        imgui.new_frame()
        gui.on_frame()
        clock.tick(30)
        imgui.render()
        impl.render(imgui.get_draw_data())
        pygame.display.flip()
        pygame.event.pump()

def matchEndedHandler(whichMLAgent, whoWon, timeSpent, moments):
    global round
    global matchInProgress
    global match
    global matches
    global clockFps
    gui.addGameDetails(whichMLAgent, whoWon, clockFps.get_fps(), timeSpent,moments)
    matchInProgress = False
    round += 1
    nextRound = 0
    if (round<4):
        notFoundNext = True
        while (notFoundNext):
            nextRound = random.randint(1,3)
            if (matches[nextRound] == False):
                notFoundNext = False
                matches[nextRound] = True
        gui.setMatchRoundId(nextRound)
        match = GameMatch(nextRound, matchEndedHandler)
    elif (round<5):
        gui.setMatchRoundId(round)
        match = GameMatch(round,matchEndedHandler)
    gui.nextUI()
if __name__ == "__main__":
    match = GameMatch(0,matchEndedHandler)
    gui = GUI(uiNextHandler, tutorialHandler)
    main()



# env_id= "StreetFighterIISpecialChampionEdition-Genesis"
# env = retro.make(env_id, state='2p', players=2)
# obs = env.reset()
# # env = SubprocVecEnv([retro.make(env_id, state='Champion.Level1.RyuVsGuile') for i in range(n_cpus)])
#
# # model = PPO("MlpPolicy", env, verbose=1)
# # # # model = PPO.load("streetFighter-ppo-100k")
# # for i in range(100):
# #  model.learn(total_timesteps=500000)
# #  model.save("streetFighter-ppo-500k")
# model = PPO.load("streetFighter-ppo-500k")
#
# # for i in range(100000):
# #     action, _states = model.predict(obs, deterministic=True)
# #     obs, reward, done, info = env.step(action)
# #     env.render()
# #     if done:
# #       obs = env.reset()
# #
# # env.close()
