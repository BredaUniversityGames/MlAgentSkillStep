import numpy as np

class FightMatch:
    def __init__(self,dataEntry):
        self.NPC = dataEntry[0][0]
        self.whoWon = dataEntry[0][1]
        self.durationFrames = dataEntry[0][2]
        self.durationSec = dataEntry[0][2]/30
        self.hpNPC = dataEntry[1]
        self.hpPlayer = dataEntry[2]
        self.apsPlayer = dataEntry[3]
        self.hpDiff = []


        if self.whoWon == 0:
            self.hpNPC.append(self.hpNPC[len(self.hpNPC)-1])
            self.hpPlayer.append(-1)
        if self.whoWon == 1:
            self.hpNPC.append(-1)
            self.hpPlayer.append(self.hpPlayer[len(self.hpPlayer)-1])

        self.getHPdiffOverTime()
        self.endHP = self.hpDiff[len(self.hpDiff)-1]
        self.endHPofNPC = self.hpNPC[len(self.hpNPC)-1]
        self.endHPofPlayer = self.hpPlayer[len(self.hpPlayer) - 1]
        self.critDictionary = {"measuredSkill": self.endHP, "attacksPlayers":self.getPlayerAttacksToNPC(),
                               "attacksNPC": self.getNPCAttacksToPlayer(),"defensePlayer": self.getPlayerDefense(),
                               "defenseNPC": self.getNPCDefense()}

    def getHPdiffOverTime(self):
        for second in range(0,len(self.hpNPC)):
            self.hpDiff.append(self.hpNPC[second] - self.hpPlayer[second])

    def getHPDeriv(self):
        return np.diff(self.hpNPC)

    def getPlayerAttacksToNPC(self):
        attacksList=[]
        for hpIndex in range(1,len(self.hpNPC)-1):
            hpJump = self.hpNPC[hpIndex - 1] - self.hpNPC[hpIndex]
            if hpJump != 0:
                if 30 > hpJump > 10:
                    attacksList.append(1)
                elif hpJump >= 30:
                    attacksList.append(2)
            else: attacksList.append(0)
        return attacksList

    def getNPCAttacksToPlayer(self):
        attacksList=[]
        for hpIndex in range(1,len(self.hpPlayer)-1):
            hpJump = self.hpPlayer[hpIndex - 1] - self.hpPlayer[hpIndex]
            if hpJump != 0:
                if 30 > hpJump > 10:
                    attacksList.append(1)
                elif hpJump >= 30: attacksList.append(2)
            else: attacksList.append(0)
        return attacksList


    def getPlayerDefense(self):
        defenseList=[]
        for hpIndex in range(1,len(self.hpPlayer)-1):
            hpJump = self.hpPlayer[hpIndex-1] - self.hpPlayer[hpIndex]
            if 2 < hpJump <= 10:
                defenseList.append(1)
            else: defenseList.append(0)
        return defenseList

    def getNPCDefense(self):
        defenseList=[]
        for hpIndex in range(1,len(self.hpNPC)-1):
            hpJump = self.hpNPC[hpIndex - 1] - self.hpNPC[hpIndex]
            if 2 < hpJump <= 10:
                defenseList.append(1)
            else: defenseList.append(0)
        return defenseList