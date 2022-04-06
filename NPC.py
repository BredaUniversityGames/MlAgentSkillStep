from FightMatch import FightMatch
from PresenceNPC import PresenceNPC
from Quiz import Quiz


class NPC:
    def __init__(self,name,participants):
        self.name = name
        self.presences = []
        self.critDictionary = {"name":self.name}
        for participant in participants:
            result = participant.getNPCDetails(name)
            if result != False:
                self.presences.append(PresenceNPC(result,participant))

    def getCriteria(self, fromCrit):
        if fromCrit in self.critDictionary.keys():
            return self.critDictionary[fromCrit]
        elif fromCrit in self.presences[0].quiz.critDictionary.keys():
            return [presence.quiz.critDictionary[fromCrit] for presence in self.presences]
        elif fromCrit in self.presences[0].fight.critDictionary.keys():
            return [presence.fight.critDictionary[fromCrit] for presence in self.presences]

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