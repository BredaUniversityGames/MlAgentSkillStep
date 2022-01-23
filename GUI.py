import sys
import gym
import numpy
import retro
import retrowrapper
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

from imgui.integrations.pygame import PygameRenderer
import imgui
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env

from GameMatch import GameMatch


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

def loadImage(image,w,h):
    # textureSurface = pygame.image.load(image)
    #
    # textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    textureData = image
    width = w
    height = h

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
                 GL_UNSIGNED_BYTE, textureData)

    return texture, width, height


def delTexture(texture):
    glDeleteTextures(texture)


def createTexDL(texture, width, height):
    newList = glGenLists(1)
    glNewList(newList, GL_COMPILE);
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)

    # Bottom Left Of The Texture and Quad
    glTexCoord2f(0, 0);
    glVertex2f(0, 0)

    # Top Left Of The Texture and Quad
    glTexCoord2f(0, 1);
    glVertex2f(0, height)

    # Top Right Of The Texture and Quad
    glTexCoord2f(1, 1);
    glVertex2f(width, height)

    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1, 0);
    glVertex2f(width, 0)
    glEnd()
    glEndList()

    return newList


def delDL(list):
    glDeleteLists(list, 1)


def render(layers):
    for l in layers:
        l.render()


class GL_Texture:
    def __init__(s, image,w,h):
        s.texture, s.width, s.height = loadImage(image,w,h)
        s.displaylist = createTexDL(s.texture, s.width, s.height)

    def __del__(self):
        if self.texture != None:
            # delTexture(self.texture)
            self.texture = None
        if self.displaylist != None:
            delDL(self.displaylist)
            self.displaylist = None

    def __repr__(s):
        return s.texture.__repr__()


class Textureset:
    """Texturesets contain and name textures."""

    def __init__(s):
        s.textures = {}

    def load(s, texname=None, texappend=".png"):
        s.textures[texname] = GL_Texture(texname, texappend)

    def set(s, texname, data):
        s.textures[texname] = data

    def delete(s, texname):
        del s.textures[texname]

    def __del__(s):
        s.textures.clear()
        del s.textures

    def get(s, name):
        return s.textures[name]


class GL_Image:
    def __init__(self, image,w,h):
        self.texture = GL_Texture(image,w,h)
        self.width = self.texture.width
        self.height = self.texture.height
        self.abspos = None
        self.relpos = None
        self.color = (1, 1, 1, 1)
        self.rotation = 0
        self.rotationCenter = None

    def draw(self, abspos=None, relpos=None, width=None, height=None,
             color=None, rotation=None, rotationCenter=None):
        if color == None:
            color = self.color

        glColor4fv(color)

        if abspos:
            glLoadIdentity()
            glTranslate(abspos[0], abspos[1], 0)
        elif relpos:
            glTranslate(relpos[0], relpos[1], 0)

        if rotation == None:
            rotation = self.rotation

        if rotation != 0:
            if rotationCenter == None:
                rotationCenter = (self.width / 2, self.height / 2)
            # (w,h) = rotationCenter
            glTranslate(rotationCenter[0], rotationCenter[1], 0)
            glRotate(rotation, 0, 0, -1)
            glTranslate(-rotationCenter[0], -rotationCenter[1], 0)

        if width or height:
            if not width:
                width = self.width
            elif not height:
                height = self.height

            glScalef(width / (self.width * 1.0), height / (self.height * 1.0), 1.0)

        glCallList(self.texture.displaylist)

        if rotation != 0:  # reverse
            glTranslate(rotationCenter[0], rotationCenter[1], 0)
            glRotate(-rotation, 0, 0, -1)
            glTranslate(-rotationCenter[0], -rotationCenter[1], 0)


class GUI:
    # diff - a number from 0 to 4 representing the level of difficulty
    def __init__(self):
        # self.difficulties = ["streetFighter-ppo-500k"]
        # self.env_id = "StreetFighterIISpecialChampionEdition-Genesis"
        # self.env = retro.make(self.env_id, state='2p', players=2)
        # self.obs = self.env.reset()
        # self.model = PPO.load(self.difficulties[0])
        self.match = None
        pygame.init()
        size = 800, 600

        render_init(800, 600)
        self.io = imgui.get_io()
        self.io.display_size = size

        self.impl = PygameRenderer()

    def startMatch(self,diff):
        self.match = GameMatch(diff)


    def startRender(self):
        rendering = True
        glLoadIdentity()
        while rendering:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                self.impl.process_event(event)

            self.match.renderFrame(events)
            imgui.new_frame()
            self.on_frame()

            # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
            #       does not support fill() on OpenGL sufraces

            img = pygame.image.frombuffer(self.match.getObs().tostring(), self.match.getObs().shape[1::-1], "RGB")
            img = pygame.transform.scale(img, (800, 600))
            #numpy.shape(pygame.surfarray.array3d(img))
            img = pygame.surfarray.array3d(img)
            img = numpy.insert(img,3 , 255, axis=2)
            print(img)
            # self.win.blit(img, (0, 0))
            fooimage = GL_Image(img, 800, 600)
            image = numpy.array([[[255, 0, 0, 255], [255, 0, 0, 255], [255, 0, 0, 255], [255, 0, 0, 255]],
                              [[255, 0, 0, 255], [255, 0, 0, 255], [255, 0, 0, 255], [255, 0, 0, 255]],
                              [[255, 0, 0, 255], [255, 0, 0, 255], [255, 0, 0, 255], [255, 0, 0, 255]],
                              [[255, 0, 0, 255], [255, 0, 0, 255], [255, 0, 0, 255], [255, 0, 0, 255]]])
            fooimage = GL_Image(image, 4, 4)


            # glClearColor(1, 1, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            fooimage.draw((0, 0))

            imgui.render()
            self.impl.render(imgui.get_draw_data())

            pygame.display.flip()

    def on_frame(self):
        # if imgui.begin_main_menu_bar():
        #     if imgui.begin_menu("File", True):
        #         clicked_quit, selected_quit = imgui.menu_item(
        #             "Quit", 'Cmd+Q', False, True
        #         )
        #         if clicked_quit:
        #             exit(1)
        #         imgui.end_menu()
        #     imgui.end_main_menu_bar()
        #imgui.show_test_window()

        imgui.begin("Custom window", True)
        imgui.text("Bar")
        imgui.text_colored("Eggs", 0.2, 1., 0.)
        imgui.end()

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
