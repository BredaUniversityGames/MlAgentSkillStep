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
        self.critDictionary = {"age": self.age, "gen": self.gender, "nat": self.nation,
                               "etn": self.ethnic, "edu": self.education, "noh": self.noh, "exp": self.experience, "tut": self.tutorial, "fps":self.fps}
        for i in range(0,5):
            self.answers.append(Quiz(entry[1][i]))
            self.fights.append(FightMatch(entry[4][i]))
        self.matchOrder = entry[3]
        self.comparisonNPC = entry[2]

    def getCriteria(self,fromCrit):
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

