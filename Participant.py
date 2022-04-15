import copy

from FightMatch import FightMatch
from Quiz import Quiz


class Participant:
    def __init__(self,entry):
        self.name = entry[0][0]
        self.age = entry[0][1]
        self.gender = entry[0][2][0].lower()
        self.nation = entry[0][3][0:1].lower()
        self.ethnic = entry[0][4]
        self.education = entry[0][5]
        self.noh = entry[0][6]
        self.experience = entry[0][7].lower()
        self.tutorial = entry[0][8].lower()
        self.fps = float(entry[0][9])
        self.answers = []
        self.fights = []
        for i in range(0,5):
            self.answers.append(Quiz(entry[1][i]))
            self.fights.append(FightMatch(entry[4][i]))
        self.matchOrder = entry[3]
        self.comparisonNPC = entry[2]
        self.critDictionary = {"age": self.age, "gen": self.gender, "nat": self.nation,
                               "etn": self.ethnic, "edu": self.education, "noh": self.noh, "exp": self.experience, "tut": self.tutorial,
                               "fps":self.fps, "fightsOrdered":self.getFightsInOrder(),"fightsNPC":self.fights,
                               "answersOrdered": self.answers, "answersNPC":self.getAnswersInTrainingOrder(),
                               "gamePerformance":self.getGamesPerformance(), "getTime":self.getGamesDuration(),
                               "getGamesWonByParticipant": self.getGamesWonByParticipant(), "getAPS":self.getAPS()}


    def getCriteria(self,fromCrit):
        if fromCrit == "identity":
            return self
        if fromCrit in self.critDictionary.keys():
            return self.critDictionary[fromCrit]
        elif fromCrit in self.answers[0].critDictionary.keys():
            return [quiz.critDictionary[fromCrit] for quiz in self.answers]
        elif fromCrit in self.fights[0].critDictionary.keys():
            return [fight.critDictionary[fromCrit] for fight in self.fights]


    def toString(self):
        print("name " + str(self.name))
        print("age " + str(self.age))
        print("gender " + str(self.gender))
        print("nation " + str(self.nation))
        print("ethnic " + str(self.ethnic))
        print("education " + str(self.education))
        print("noh " + str(self.noh))
        print("experience " + str(self.experience))
        print("tutorial " + str(self.tutorial))
        print(self.matchOrder)
        print(self.comparisonNPC)
        print(self.answers)
        print(self.fights)

    def locateNPC(self,nameNPC):
        fightOrderNr = -1
        matchOrderNr = -1
        for fight in range(0, 5):
            if self.fights[fight].NPC == nameNPC:
                fightOrderNr = fight
                break
        for match in range(0, 5):
            if self.matchOrder[match]-1 == fightOrderNr:
                matchOrderNr = match
                break

        return matchOrderNr, fightOrderNr

    def getNPCDetails(self,nameNPC):
        dataPackNPC = []
        matchOrderNr, fightOrderNr = self.locateNPC(nameNPC)
        if matchOrderNr == -1: return False

        dataPackNPC.append(matchOrderNr)
        dataPackNPC.append(fightOrderNr)

        dataPackNPC.append(self.answers[matchOrderNr])
        dataPackNPC.append(self.fights[fightOrderNr])

        return dataPackNPC

    def getComparisonNPCAnalysis(self):
        gradeComparison = []
        print(self.comparisonNPC)
        for i in range(1,len(self.matchOrder)):
            if self.matchOrder[i-1] > self.matchOrder[i]: #if the last NPC was trained more than current NPC
                if self.comparisonNPC[i] == 0:
                    gradeComparison.append(1)
                if self.comparisonNPC[i] == 1:
                    gradeComparison.append(0)
                if self.comparisonNPC[i] == 2:
                    gradeComparison.append(-1)
            else:#if the last NPC was trained less than current NPC
                gradeComparison.append(self.comparisonNPC[i]-1)
        return copy.deepcopy(self.matchOrder), gradeComparison

    def getFightsInOrder(self):
        orderedFights = []
        for i in self.matchOrder:
            orderedFights.append(self.fights[i-1])
        return orderedFights

    def getAnswersInTrainingOrder(self): # 1 3 4 5 2
        orderedAnswers = [0,0,0,0,0]
        for i in range(0,len(self.matchOrder)):
            orderedAnswers[self.matchOrder[i]-1] = self.answers[i]
        return orderedAnswers

    def getGamesPerformance(self):
        orderedAnswers = [0, 0, 0, 0, 0]
        orderedFights = self.getFightsInOrder()
        for i in range(0, 5):
            orderedAnswers[i] = orderedFights[i].endHP
        return orderedAnswers

    def getGamesWonByParticipant(self):
        orderedAnswers = 0
        for fight in self.fights:
            if fight.whoWon == 1:
                orderedAnswers+=1
        return orderedAnswers

    def getAPS(self):
        orderedAnswers = []
        for fight in self.fights:
            orderedAnswers.append(fight.apsPlayer)
        return orderedAnswers

    def getGamesDuration(self):
        durations = []
        for fight in self.fights:
            durations.append(fight.durationSec)
        return durations