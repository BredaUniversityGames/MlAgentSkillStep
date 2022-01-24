
from OpenGL.GL import *
from OpenGL.GLU import *

from imgui.integrations.pygame import PygameRenderer
import imgui

username = ""
age = ""
widgets_basic_radio_button = 0

class GUI:
    # diff - a number from 0 to 4 representing the level of difficulty
    def __init__(self):
        self.state = 0
        self.round = 0
        self.window_flags = 0
        self.window_flags |= imgui.WINDOW_NO_MOVE
        self.window_flags |= imgui.WINDOW_NO_COLLAPSE



    def nextUI(self):
        if self.state == 1 and self.round < 4:
            self.round+=1
        else:
            self.state+=1

    def displayLogin(self):
        global username
        global age
        imgui.set_next_window_size(0, 0, condition=imgui.FIRST_USE_EVER)
        imgui.begin("User Information", closable=False, flags=self.window_flags )
        imgui.text("Bar")
        clicked, username = imgui.input_text(
            label="Name", value=username, buffer_length=64
        )
        imgui.text("Bar")
        clicked, age = imgui.input_text(
            label="Age",
            value=age,
            buffer_length=64,
            flags=imgui.INPUT_TEXT_CHARS_DECIMAL,
        )
        imgui.text_colored("Eggs", 0.2, 1., 0.)
        imgui.end()

    def displayQuestionary(self):

        global widgets_basic_radio_button
        imgui.set_next_window_size(0, 0, condition=imgui.FIRST_USE_EVER)
        imgui.begin("Questionary " + str(self.round+1) + "/5", closable=False, flags=self.window_flags )
        imgui.text("Bar")

        clicked, widgets_basic_radio_button = imgui.radio_button("radio a", widgets_basic_radio_button)
        imgui.same_line()
        clicked, widgets_basic_radio_button = imgui.radio_button("radio b", widgets_basic_radio_button)
        imgui.same_line()
        clicked, widgets_basic_radio_button = imgui.radio_button("radio c", widgets_basic_radio_button)
        imgui.text_colored("Eggs", 0.2, 1., 0.)
        imgui.end()

    def displayThanks(self):
        imgui.begin("Thank you", closable=False, flags=self.window_flags )
        imgui.text("Bar")
        imgui.text_colored("Eggs", 0.2, 1., 0.)
        imgui.end()

    def on_frame(self):
        if self.state == 1:
            self.displayQuestionary()
        if self.state == 0:
            self.displayLogin()
        else:
            self.displayThanks()





