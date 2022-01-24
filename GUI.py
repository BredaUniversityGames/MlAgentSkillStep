
from OpenGL.GL import *
from OpenGL.GLU import *

from imgui.integrations.pygame import PygameRenderer
import imgui

def show_help_marker(desc):

    imgui.text_disabled("(?)")
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.push_text_wrap_pos(imgui.get_font_size() * 35.0)
        imgui.text_unformatted(desc)
        imgui.pop_text_wrap_pos()
        imgui.end_tooltip()
class GUI:
    # diff - a number from 0 to 4 representing the level of difficulty
    def __init__(self):
        self.ethnicity = ""
        self.nationality = ""
        self.survey = False
        self.tutorial = False
        self.anon = False
        self.GDPR = False
        self.noh = ""
        self.gender = ""

        self.username = ""
        self.age = ""
        self.widgets_basic_radio_button = 0

        self.state = 0
        self.round = 0

        self.window_flags = 0
        self.window_flags |= imgui.WINDOW_NO_MOVE
        self.window_flags |= imgui.WINDOW_NO_COLLAPSE

    def getUsername(self):
        return self.username

    def nextUI(self):
        if self.state == 1 and self.round < 4:
            self.round+=1
        else:
            self.state+=1

    def displayLogin(self):
        imgui.set_next_window_size(800, 600)
        imgui.set_next_window_position(0, 0)
        imgui.begin("User Information", closable=False, flags=self.window_flags )
        imgui.text("Name")
        clicked, self.username = imgui.input_text(
            label="Name", value=self.username, buffer_length=64
        )
        imgui.text("Age")
        clicked, self.age = imgui.input_text(
            label="Age",
            value=self.age,
            buffer_length=64,
            flags=imgui.INPUT_TEXT_CHARS_DECIMAL,
        )
        imgui.text("Gender")
        clicked, self.gender = imgui.input_text(
            label="Gender",
            value=self.gender,
            buffer_length=64,
        )
        imgui.text("Nationality")
        clicked, self.nationality = imgui.input_text(
            label="Nationality",
            value=self.nationality,
            buffer_length=64,
        )
        imgui.text("Ethnicity")
        clicked, self.ethnicity = imgui.input_text(
            label="Ethnicity",
            value=self.ethnicity,
            buffer_length=64,
        )
        imgui.text("Number of Hours playing video games per week")
        clicked, self.noh = imgui.input_text(
            label="Hours played",
            value=self.noh,
            buffer_length=64,
            flags=imgui.INPUT_TEXT_CHARS_DECIMAL,
        )
        clicked, self.GDPR = imgui.checkbox(label="Agree with the data processing mentioned at: https://bit.ly/MGTO2022", state=self.GDPR)

        clicked, self.anon = imgui.checkbox(label="Remain anonymous", state=self.anon)

        imgui.text("")
        imgui.text("")
        if imgui.button("Tutorial"):
            self.tutorial = True
        imgui.same_line(150)
        if imgui.button("Start Survey"):
            self.survey = True
        imgui.end()

    def displayQuestionary(self):
        imgui.set_next_window_size(0, 0, condition=imgui.FIRST_USE_EVER)
        imgui.begin("Questionary " + str(self.round+1) + "/5", closable=False, flags=self.window_flags )
        imgui.text("Bar")

        clicked, self.widgets_basic_radio_button = imgui.radio_button("radio a", self.widgets_basic_radio_button)
        imgui.same_line()
        clicked, self.widgets_basic_radio_button = imgui.radio_button("radio b", self.widgets_basic_radio_button)
        imgui.same_line()
        clicked, self.widgets_basic_radio_button = imgui.radio_button("radio c", self.widgets_basic_radio_button)
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





