from PresenceNPC import PresenceNPC


class NPC:
    def __init__(self,name,participants):
        self.name = name
        self.presences = []

        for participant in participants:
            result = participant.getNPCDetails(name)
            if result != False:
                self.presences.append(PresenceNPC(result,participant))



    def getWins(self):
        totalWins = 0
        for presence in self.presences:
            totalWins += 1 if presence.fight.whoWon == 0 else 0
        return totalWins

    def getLoses(self):
        totalLoses = 0
        for presence in self.presences:
            totalLoses += 1 if presence.fight.whoWon == 1 else 0
        return totalLoses

    def getHPatTheEndOfGameNPC(self):
        aggregHPs = []
        for presence in self.presences:
            aggregHPs.append(presence.fight.endHPofNPC)
        return aggregHPs

    def getHPatTheEndOfGamePlayer(self):
        aggregHPs = []
        for presence in self.presences:
            aggregHPs.append(presence.fight.endHPofPlayer)
        return aggregHPs

    def getDerivHPatTheEndofTheGame(self):
        aggregHPs = []
        for presence in self.presences:
            aggregHPs.append(presence.fight.endHP)
        return aggregHPs

    def getNPCTime(self,filter):
        aggregTime = []
        for presence in self.presences:
            if filter(None,presence):
                aggregTime.append(presence.fight.durationFrames)
        return aggregTime

class filterNPC:
    def filterMatchesWonByNPC(self,presence):
        return presence.fight.whoWon == 0
    def filterMatchesLostByNPC(self,presence):
        return presence.fight.whoWon == 1