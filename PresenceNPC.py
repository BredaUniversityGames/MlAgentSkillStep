class PresenceNPC:
    def __init__(self, dataPack, participant):
        self.matchOrderNr = dataPack[0]
        self.fightOrderNr = dataPack[1]
        self.participant = participant
        self.quiz = dataPack[2]
        self.fight = dataPack[3]