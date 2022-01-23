from GUI import GUI
import pygame
import os

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from imgui.integrations.pygame import PygameRenderer
import imgui

from GameMatch import GameMatch


def mainApp():
    gui = GUI()
    gui.startMatch(0)
    gui.startRender()

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
    glDeleteTextures(1,[texture])


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
            delTexture(self.texture)
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



def main():
    render_init(800, 600)
    io = imgui.get_io()
    io.display_size = (800, 600)

    impl = PygameRenderer()
    image = np.array([[[255, 0, 0, 255], [255, 0, 0, 255],[255, 0, 0, 255], [255, 0, 0, 255]], [[255, 0, 0, 255], [255, 0, 0, 255],[255, 0, 0, 255], [255, 0, 0, 255]], [[255, 0, 0, 255], [255, 0, 0, 255],[255, 0, 0, 255], [255, 0, 0, 255]], [[255, 0, 0, 255], [255, 0, 0, 255],[255, 0, 0, 255], [255, 0, 0, 255]]])


    clock = pygame.time.Clock()
    glLoadIdentity()
    for count in range(100000):
        events = pygame.event.get()
        match.renderFrame(events)
        img = match.getObs()
        print(np.shape(img))
        img = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")
        img = pygame.transform.scale(img, (800, 600))
        # numpy.shape(pygame.surfarray.array3d(img))
        img = pygame.surfarray.array3d(img)
        img = np.insert(img, 3, 255, axis=2)
        #img = np.flip(img,2)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        fooimage = GL_Image(img, 600, 800)
        fooimage.draw((0, 0))
        imgui.new_frame()
        on_frame()
        clock.tick()
        imgui.render()
        impl.render(imgui.get_draw_data())
        pygame.display.flip()
        pygame.event.pump()
    print("result: " + str(clock.get_fps()) + " FPS")
def on_frame():
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

if __name__ == "__main__":
    match = GameMatch(0)
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
