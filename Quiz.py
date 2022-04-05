class Quiz:
    def __init__(self,dataEntry):
        self.enjoy = dataEntry[0]
        self.skillNPC = dataEntry[1]
        self.skillPlayer = dataEntry[2]
        self.skillRelative = dataEntry[3]
        self.skillAttack = dataEntry[4]
        self.skillMove = dataEntry[5]
        self.skillDefend = dataEntry[6]
        self.passiveAggressive = dataEntry[7]
        self.riposte = dataEntry[8]
        self.delayed = dataEntry[9]
        self.human = dataEntry[10]
        self.predictable = dataEntry[11]
        self.exploitable = dataEntry[12]
        self.skillNPCtoPrevNPC = dataEntry[13]
        self.critDictionary = {"enjoy": self.enjoy, "skillNPC": self.skillNPC, "skillPlayer": self.skillPlayer,
                               "skillRelative": self.skillRelative, "skillAttack": self.skillAttack, "skillMove": self.skillMove, "skillDefend": self.skillDefend,
                               "passiveAggressive": self.passiveAggressive, "self.riposte": self.riposte, "delayed":self.delayed, "human":self.human, "predictable":self.predictable, "exploitable":self.exploitable, "skillNPCtoPrevNPC":self.skillNPCtoPrevNPC}

