import sys

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


def initializeDisplay(w, h):
    pygame.display.set_mode((w,h), pygame.DOUBLEBUF | pygame.OPENGL | pygame.OPENGLBLIT | pygame.RESIZABLE)
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



def main():
    running = True
    logIn = True
    stage = 0
    matchInProgress = False

    render_init(800, 600)
    io = imgui.get_io()
    io.display_size = (800, 600)

    impl = PygameRenderer()
    image = np.array([[[255, 0, 0, 255], [255, 0, 0, 255],[255, 0, 0, 255], [255, 0, 0, 255]], [[255, 0, 0, 255], [255, 0, 0, 255],[255, 0, 0, 255], [255, 0, 0, 255]], [[255, 0, 0, 255], [255, 0, 0, 255],[255, 0, 0, 255], [255, 0, 0, 255]], [[255, 0, 0, 255], [255, 0, 0, 255],[255, 0, 0, 255], [255, 0, 0, 255]]])


    clock = pygame.time.Clock()
    glLoadIdentity()
    while running:
        events = pygame.event.get()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if not matchInProgress:
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                impl.process_event(event)
            imgui.new_frame()
            gui.on_frame()
            imgui.show_test_window()
            imgui.render()
            impl.render(imgui.get_draw_data())
        if matchInProgress:
            match.renderFrame(events)
            img = match.getObs()
            #print(np.shape(img))

            img = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")
            img = pygame.transform.scale(img, (800, 600))
            # numpy.shape(pygame.surfarray.array3d(img))
            img = pygame.surfarray.array3d(img)
            img = np.insert(img, 3, 255, axis=2)
            #img = np.flip(img,2)
            img = np.swapaxes(img,0,1)

            fooimage = GL_Image(img, 800, 600)
            fooimage.draw((0, 0))
        clock.tick(30)
        pygame.display.flip()
        pygame.event.pump()
    print("result: " + str(clock.get_fps()) + " FPS")

if __name__ == "__main__":
    match = GameMatch(0)
    gui = GUI()
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
