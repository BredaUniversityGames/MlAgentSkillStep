class PresenceNPC:
    def __init__(self, dataPack, participant):
        self.matchOrderNr = dataPack[0]
        self.fightOrderNr = dataPack[1]
        self.participant = participant
        self.quiz = dataPack[2]
        self.fight = dataPack[3]
        self.critDictionary = {"whoWon": self.fight.whoWon, "participant": self.participant}

    def getCriteria(self,fromCrit):
        if fromCrit == "identity":
            return self
        if fromCrit in self.critDictionary.keys():
            return self.critDictionary[fromCrit]
        elif fromCrit in self.quiz.critDictionary.keys():
            return self.quiz.critDictionary[fromCrit]
        elif fromCrit in self.fight.critDictionary.keys():
            return self.fight.critDictionary[fromCrit]