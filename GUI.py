import sys

from OpenGL.GL import *
from OpenGL.GLU import *

from imgui.integrations.pygame import PygameRenderer
import imgui
from datetime import datetime

from DataSender import sendEmail


def show_help_marker(desc):
    imgui.same_line()
    imgui.text_disabled("(?)")
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.push_text_wrap_pos(imgui.get_font_size() * 35.0)
        imgui.text_unformatted(desc)
        imgui.pop_text_wrap_pos()
        imgui.end_tooltip()


class GUI:
    # diff - a number from 0 to 4 representing the level of difficulty
    def __init__(self, callback, callbackTutorial):
        self.skipTutorial = False
        self.didTutorial = False
        self.buttonClicked = False
        maxRounds = 5
        self.nrQuestionsInRound = 14
        pointsOnScale = 7

        self.fps=0
        self.callback = callback
        self.callbackTutorial = callbackTutorial

        self.opinion = []
        self.roundResults = [[], [], [], [], []]
        self.order = []

        self.ethnicity = 0
        self.education = 0
        self.nationality = ""
        self.survey = False
        self.tutorial = False
        self.anon = False
        self.exp = False
        self.GDPR = False
        self.noh = ""
        self.gender = ""

        self.username = ""
        self.age = ""
        self.widgets_basic_radio_button = 0

        self.state = 0
        self.round = 0
        self.closed = False
        self.match = 0
        self.nextMatch = 0

        self.window_flags = 0
        self.window_flags |= imgui.WINDOW_NO_MOVE
        self.window_flags |= imgui.WINDOW_NO_COLLAPSE

        self.id = 211
        self.initAnswerMatrix(maxRounds, self.nrQuestionsInRound, pointsOnScale)

    def setMatchRoundId(self, matchRoundId):
        self.nextMatch = matchRoundId

    def initAnswerMatrix(self, rounds, nrQuestions, nrPointsOnScale):
        for i in range(rounds):
            self.opinion.append([])
            for j in range(nrQuestions):
                self.opinion[i].append([])
                for k in range(nrPointsOnScale):
                    self.opinion[i][j].append(False)

    def checkRadioButton(self, questionAnswer, questionNR, size, itemPoz):
        onlyAnswer = True
        for i in range(size):
            if questionAnswer[questionNR][i] == True and i != itemPoz:
                questionAnswer[questionNR][i] = False

    def showLikertScale(self, questionAnswer, size, questionNR, quant1="Poor", quant2="Excellent"):

        imgui.text(quant1)
        for i in range(size):
            imgui.same_line(120 + i * 25)
            # Use push id to avoid unique labels
            imgui.push_id(str(questionNR) + str(i))
            clicked, questionAnswer[questionNR][i] = imgui.checkbox("", questionAnswer[questionNR][i])
            if clicked:
                self.checkRadioButton(questionAnswer, questionNR, size, i)
            imgui.pop_id()
        imgui.same_line()
        imgui.text(quant2)

    def getUsername(self):
        return self.username

    def nextUI(self):
        self.closed = False
        if self.state == 1 and self.round < 4:
            self.round += 1
        else:
            self.state += 1
        if self.state == 2:
            try:
                self.saveDataToCSV()
            except:
                print("Can't write results on csv, please contact me at 214930@buas.nl")
            try:
                self.sendDataToEmail()
            except:
                print("Can't send results email, please contact me at 214930@buas.nl")


    def closeUI(self):
        self.match = self.nextMatch
        self.callback()
        self.closed = True
        self.buttonClicked = False
        if self.round == 4:
            self.nextUI()
            self.closed = False

    def displayTutorial(self):
        imgui.set_next_window_size(300, 300)
        imgui.set_next_window_position(0, 0)
        imgui.begin("Controls tutorial", closable=False)
        imgui.text("")
        imgui.text("Move buttons:")
        imgui.text("Arrow keys <-v^-> ")
        imgui.text("")
        imgui.text("Attack buttons:")
        imgui.text("A S D")
        imgui.text("Z X C")
        imgui.text("")
        imgui.text("Defend: Move Back")
        imgui.text("")
        imgui.text("Throw: Move into enemy NPC and press S")
        imgui.text("")
        imgui.text("")
        if imgui.button("Start Survey"):
            self.survey = True
            self.tutorial = False
            self.didTutorial = True
            self.closeUI()
            self.callbackTutorial()
        imgui.text("")
        imgui.text("")
        imgui.end()

    def displayLogin(self):

        imgui.set_next_window_size(800, 600)
        imgui.set_next_window_position(0, 0)
        imgui.begin("User Information", closable=False, flags=self.window_flags)
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
        changed, self.ethnicity = imgui.combo(
            label="Ethnicity",
            current=self.ethnicity,
            items=["Asian/Pacific Islander", "African American or Black", "Hispanic", "European American or White", "Multiracial/Multiethnic"]
        )
        imgui.text("Highest level of education completed")
        changed, self.education = imgui.combo(
            label="Highest level of education completed",
            current=self.education,
            items=["elementary","high school", "bachelor's degree","master's degree", "doctorate"]
        )
        # clicked, self.ethnicity = imgui.input_text(
        #     label="Ethnicity",
        #     value=self.ethnicity,
        #     buffer_length=64,
        # )
        imgui.text("Number of Hours playing video games per week")
        clicked, self.noh = imgui.input_text(
            label="Hours played",
            value=self.noh,
            buffer_length=64,
            flags=imgui.INPUT_TEXT_CHARS_DECIMAL,
        )
        clicked, self.GDPR = imgui.checkbox(
            label="Agree with the data processing mentioned at: https://bit.ly/MGTO2022", state=self.GDPR)

        clicked, self.anon = imgui.checkbox(label="Remain anonymous", state=self.anon)
        clicked, self.exp = imgui.checkbox(label="Do you have previous experience playing 2 player fighting games such as Street Fighter II?", state=self.exp)
        clicked, self.skipTutorial = imgui.checkbox(label="Skip Tutorial", state=self.skipTutorial)
        imgui.text("")
        imgui.text("The game Street Fighter II was released in 1992 and I have swapped the default enemy with Machine Learning NPCs")
        imgui.text("This research aims to analyse the skill of Machine Learning Artificial Intelligence.")
        imgui.text("You will fight 5 enemies (NPCs) that each learned to play for longer or shorter periods of time.")
        imgui.text("")
        imgui.text("")
        imgui.same_line(200)
        if imgui.button("Start Survey"):
            if self.GDPR and self.gender != "" and self.nationality != "" and self.ethnicity != "" and self.noh != "" and self.age != "":
                if self.skipTutorial:
                    self.survey = True
                    self.closeUI()
                else:
                    self.tutorial = True
                    self.callbackTutorial()
                    self.buttonClicked = False
            else:
                self.buttonClicked = True
        if self.buttonClicked:
            imgui.same_line()
            imgui.text_colored("Fill in everything!", 1.0, 0.0, 0.0, 1.0)
        imgui.end()

    def displayQuestionary(self):
        # Create this rounds answers dimension

        imgui.set_next_window_size(800, 600)
        imgui.set_next_window_position(0, 0)
        imgui.begin("Questionnaire " + str(self.round + 1) + "/5", closable=False, flags=self.window_flags)

        imgui.text("Did you enjoy competing against this NPC?")
        self.showLikertScale(self.opinion[self.match], 7, 0, "Didn't enjoy it", "Enjoyed it")

        imgui.text("How skilled was the NPC?")
        self.showLikertScale(self.opinion[self.match], 7, 1)

        imgui.text("How skilled were you?")
        self.showLikertScale(self.opinion[self.match], 7, 2)

        imgui.text("How skilled was the NPC compared to you?")
        self.showLikertScale(self.opinion[self.match], 3, 3, "Less Skilled", "More Skilled")

        imgui.text("How well did the NPC attack compared to you?")
        self.showLikertScale(self.opinion[self.match], 7, 4)

        imgui.text("How well did the NPC defend compared to you?")
        self.showLikertScale(self.opinion[self.match], 7, 5)

        imgui.text("How well did the NPC move compared to you?")
        self.showLikertScale(self.opinion[self.match], 7, 6)

        imgui.text("How passive or aggressive was the NPC?")
        self.showLikertScale(self.opinion[self.match], 7, 7, "Passive", "Aggressive")
        imgui.text("How well did the NPC riposte compared to you?")
        show_help_marker("A riposte is when you offer an immediate attack after a parry or block")
        self.showLikertScale(self.opinion[self.match], 7, 8)
        imgui.text("How delayed were the NPC's reactions?")
        self.showLikertScale(self.opinion[self.match], 7, 9, "Delayed", "Reactive")
        imgui.text("How human-like was the NPC?")
        self.showLikertScale(self.opinion[self.match], 7, 10, "Inhuman", "Human")
        imgui.text("How predictable was the NPC?")
        self.showLikertScale(self.opinion[self.match], 7, 11, "Unpredictable", "Predictable")
        imgui.text("Was the NPC behaviour exploitable?")
        self.showLikertScale(self.opinion[self.match], 7, 12, "Exploitable", "Adaptive")
        if self.round > 0:
            imgui.text("How skilled was this NPC compared to the previous one?")
            self.showLikertScale(self.opinion[self.match], 3, 13, "Less Skilled", "More Skilled")

        imgui.same_line(400)
        stringButtonNext = "Finish"
        if self.round < 4:
            stringButtonNext ="Next NPC " + str(self.round + 2) + "/5"
        if imgui.button(stringButtonNext):
            if self.validateAnswers(self.opinion[self.match],self.round):
                self.closeUI()
            else:
                self.buttonClicked = True
        if self.buttonClicked:
            imgui.same_line()
            imgui.text_colored("Fill in everything!",1.0,0.0,0.0,1.0)
        imgui.end()

    def displayThanks(self):
        imgui.set_next_window_size(800, 600)
        imgui.set_next_window_position(0, 0)
        imgui.begin("Thank you", closable=False, flags=self.window_flags)
        imgui.text("Thank You!")
        imgui.text("This is the end of the survey")
        imgui.text("")
        if imgui.button("Exit"):
            sys.exit()
        imgui.end()

    def addGameDetails(self, whihcMLAgent, whoWon, fpsavg, timeSpent, moments):
        self.fps += fpsavg
        self.order.append(self.match + 1)
        self.roundResults[self.match].append(whihcMLAgent)
        self.roundResults[self.match].append(whoWon)
        self.roundResults[self.match].append(timeSpent)
        self.roundResults[self.match].append(moments)

    def sendDataToEmail(self):
        if self.username == "" or self.anon:
            self.username = datetime.now()
        stringData = "\n" + str(self.username) + "," + str(self.age) + "," + str(self.gender) + "," + str(
            self.nationality) + "," + str(self.ethnicity) + "," + str(self.education) + "," + str(self.noh) + "," + str(self.exp) + "," + str(self.didTutorial) + "," + str(self.fps/5)
        for round in self.opinion:
            for question in round:
                answered = False
                for i in range(0, 7):
                    if question[i] == True:
                        stringData += "," + str(i)
                        answered = True
                if answered == False:
                    stringData += ",-1"
        stringData += "\n"
        for i in self.order:
            stringData += str(i) + ","
        for i in range(0, 5):
            stringData += "\n" + str(i + 1) + "," + str(self.roundResults[i][0]) + "," + str(
                self.roundResults[i][1]) + ","
            stringData += str(self.roundResults[i][2])
            for player in range(3):
                stringData += "\n" + str(i + 1)
                for j in self.roundResults[i][3][player]:
                    stringData += "," + str(j)

        sendEmail(stringData)

    def saveDataToCSV(self):
        f = open("MLSkillStepData.csv", "a")
        if self.username == "" or self.anon:
            self.username = datetime.now()
        stringData = "\n" + str(self.username) + "," + str(self.age) + "," + str(self.gender) + "," + str(
            self.nationality) + "," + str(self.ethnicity) + "," + str(self.education) + "," + str(self.noh) + "," + str(self.exp) + "," + str(self.didTutorial) + "," + str(self.fps/5)
        for round in self.opinion:
            for question in round:
                answered = False
                for i in range(0, 7):
                    if question[i] == True:
                        stringData += "," + str(i)
                        answered = True
                if answered == False:
                    stringData += ",-1"

        f.write(stringData)
        stringData = "\n"
        for i in self.order:
            stringData += str(i) + ","
        f.write(stringData)
        for i in range(0, 5):
            stringData = "\n" + str(i + 1) + "," + str(self.roundResults[i][0]) + "," + str(
                self.roundResults[i][1]) + ","
            stringData += str(self.roundResults[i][2])
            f.write(stringData)
            for player in range(3):
                stringData = "\n" + str(i + 1)
                for j in self.roundResults[i][3][player]:
                    stringData += "," + str(j)
                f.write(stringData)

        f.close()

    def on_frame(self):

        if self.closed: return
        if self.tutorial:
            self.displayTutorial()
            return
        if self.state == 1:
            self.displayQuestionary()
        elif self.state == 0:
            self.displayLogin()
        else:
            self.displayThanks()

    def validateAnswers(self, questions,firstRound):
        allMandatoryQuestionsAnswered = True
        nrQuestionsChecked = self.nrQuestionsInRound
        if firstRound == 0:
            nrQuestionsChecked -= 1
        for i in range(nrQuestionsChecked):
            answeredQuestion = False
            for j in range(7):
                if questions[i][j]:
                    answeredQuestion = True
                    break
            if not answeredQuestion:
                allMandatoryQuestionsAnswered = False
                return allMandatoryQuestionsAnswered
        return allMandatoryQuestionsAnswered
