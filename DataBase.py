from matplotlib import pyplot as plt

from NPC import NPC


def getAvgNumber(data):
    howMany = 0
    sumAgg = 0
    for e in data:
        if isinstance(e,list):
            for ee in e:
                sumAgg += ee
                howMany += 1
        else:
            sumAgg += e
            howMany += 1
    return sumAgg/howMany

def dotPlot(dataX,dataY,xlabel,ylabel):
    plt.plot(dataX,dataY,'o')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def getCountOf(data,what):
    howMany = 0
    for e in data:
        if isinstance(e, list):
            for ee in e:
                if ee == what:
                    howMany += 1
        elif e == what:
            howMany += 1
    return howMany

class DataBase:
    def __init__(self,participants):
        self.participants = participants
        self.NPCs = []
        self.npcNamesDict = {"10":0, "100":1, "1k":2, "100k":3, "1000k":4}
        self.getNPCs()

    def getSize(self):
        return len(self.participants)

    def operatorFunction(self,param, operator, amount):
        if operator is None:
            return True
        if operator == "<":
            return param < amount
        if operator == "<=":
            if isinstance(param, list):
                for entity in param:
                    if entity <= amount:
                        return True
                return False
            return param <= amount
        if operator == "!=":
            if isinstance(param, list):
                for entity in param:
                    if entity != amount:
                        return True
                return False
            return param != amount
        if operator == ">=":
            if isinstance(param, list):
                for entity in param:
                    if entity >= amount:
                        return True
                return False
            return param >= amount
        if operator == ">":
            return param > amount
        if operator == "==":
            if isinstance(amount,list):
                for entity in amount:
                    if param == entity:
                        return True
                return False
            return param == amount
        raise "no such operator defined"

    def filterBy(self, fromCrit, operator=None, amount=None, nameNPC= None):
        newList = []
        dataPool = self.participants
        if nameNPC is not None:
            if nameNPC != True:
                for npc in self.NPCs:
                    if npc.name == nameNPC:
                        dataPool = [npc]
            else:
                dataPool = self.NPCs

        for dataEntry in dataPool:
            if self.operatorFunction(dataEntry.getCriteria(fromCrit), operator, amount):
                newList.append(dataEntry)
        return newList

    def getSubsetCritBy(self, subset, fromCrit, operator=None, amount=None, nameNPC= None):
        newList = []
        for dataEntry in subset:
            result = dataEntry.getCriteria(fromCrit)
            if self.operatorFunction(result, operator, amount):
                newList.append(result)
        return newList

    def filterSubsetBy(self,subset, fromCrit, operator=None, amount=None):
        newList = []
        for dataEntry in subset:
            if self.operatorFunction(dataEntry.getCriteria(fromCrit), operator, amount):
                newList.append(dataEntry)
        return newList

    def nohIncresesReportedSkillOfPlayer(self,noh):
        entriesWithNohlessthan = self.filterEntriesBy( "noh", "<", noh)
        entriesWithNohMoreOrEqual = self.filterEntriesBy( "noh", ">=", noh)
        skillPlayersLess = self.filterSubsetBy(entriesWithNohlessthan,"skillPlayer")
        skillPlayersMoreEq = self.filterSubsetBy(entriesWithNohMoreOrEqual, "skillPlayer")
        print("avg Skill for Noh Less to " + str(noh) + " : " + str(getAvgNumber(skillPlayersLess)))
        print("avg Skill for Noh More or Eq to " + str(noh) + " : " + str(getAvgNumber(skillPlayersMoreEq)))

    def genderIncresesReportedSkillOfPlayer(self):
        entriesM = self.filterEntriesBy( "gen", "==", "m")
        entriesF = self.filterEntriesBy( "gen", "==", "f")
        skillPlayersM = self.filterSubsetBy(entriesM,"skillPlayer")
        skillPlayersF = self.filterSubsetBy(entriesF, "skillPlayer")
        print("avg Skill for gender Male"  + " : " + str(getAvgNumber(skillPlayersM)))
        print("avg Skill for gender Female "  + " : " + str(getAvgNumber(skillPlayersF)))

    def linkOnePointWithArrayAvg(self, criteria1,criteria2, nameNPC=None, plotOpt=None, excludeMinus=False, Avg=True):
        #links a general point to an average

        criteria1Pool ,criteria2Linked = self.linkBetween(criteria1,criteria2,nameNPC)

        for criteria2Index in range(0,len(criteria2Linked)):
            if excludeMinus:
                criteria2Linked[criteria2Index] = deleteFromList(criteria2Linked[criteria2Index],-1)
            if Avg:
                criteria2Linked[criteria2Index] = getAvgNumber(criteria2Linked[criteria2Index])

        if plotOpt == "dot":
            dotPlot(criteria1Pool,criteria2Linked,criteria1,criteria2)
        return criteria1Pool,criteria2Linked

    def linkOnePointWithArrayCount(self, criteria1,criteria2, nameNPC=None, plotOpt=None, excludeMinus=False, countWhat=None):
        #links a general point to an average

        criteria1Pool ,criteria2Linked = self.linkBetween(criteria1,criteria2,nameNPC)

        for criteria2Index in range(0,len(criteria2Linked)):
            if excludeMinus:
                criteria2Linked[criteria2Index] = deleteFromList(criteria2Linked[criteria2Index],-1)
            criteria2Linked[criteria2Index] = getCountOf(criteria2Linked[criteria2Index],countWhat)

        if plotOpt == "dot":
            dotPlot(criteria1Pool,criteria2Linked,criteria1,criteria2)
        return criteria1Pool,criteria2Linked

    def linkCriteriasFromAllFights(self, criteria1,criteria2, nameNPC=None, plotOpt=None ):
        criteria1Pool, criteria2Linked = self.linkBetween(criteria1, criteria2, nameNPC, identity=False)

        new1Pool = []
        new2Link = []
        if isinstance(criteria1Pool[0], list):
            for index in range(0,len(criteria1Pool)):
                for jndex in range(0, len(criteria1Pool[0])):
                    if criteria1Pool[index][jndex] in new1Pool:
                        if isinstance(new2Link[new1Pool.index(criteria1Pool[index][jndex])],list):
                            new2Link[new1Pool.index(criteria1Pool[index][jndex])].append(criteria2Linked[index][jndex])
                        else:
                            new2Link[new1Pool.index(criteria1Pool[index][jndex])] = [new2Link[new1Pool.index(criteria1Pool[index][jndex])],criteria2Linked[index][jndex]]
                    else:
                        new1Pool.append(criteria1Pool[index][jndex])
                        new2Link.append(criteria2Linked[index][jndex])

        for new2Index in range(0,len(new2Link)):
            new2Link[new2Index] = getAvgNumber(new2Link[new2Index])

        return new1Pool,new2Link


    def getNPCs(self):
        for name in self.npcNamesDict.keys():
            self.NPCs.append(NPC(name,self.participants))

    def getNPCRemainingHP(self,nameNPC):
        return self.NPCs[self.npcNamesDict[nameNPC]].getHPatTheEndOfGameNPC()

    def getDiffHPatTheEnd(self,nameNPC):
        return self.NPCs[self.npcNamesDict[nameNPC]].getDerivHPatTheEndofTheGame()

    def linkBetween(self,criteria1,criteria2,nameNPC=None, identity=True):
        dataPool = self.participants
        if nameNPC is not None:
            if nameNPC != True:
                for npc in self.NPCs:
                    if npc.name == nameNPC:
                        dataPool = [npc]
            else:
                dataPool = self.NPCs
        criteria1Pool = []
        criteria2Linked = []
        for dataBite in dataPool:
            if dataBite.getCriteria(criteria1) not in criteria1Pool or identity is False:
                criteria1Pool.append(dataBite.getCriteria(criteria1))
                criteria2Linked.append(dataBite.getCriteria(criteria2))
            else:
                if isinstance(dataBite.getCriteria(criteria2),list):
                    criteria2Linked[criteria1Pool.index(dataBite.getCriteria(criteria1))] += dataBite.getCriteria(criteria2)
                else:
                    criteria2Linked[criteria1Pool.index(dataBite.getCriteria(criteria1))].append(dataBite.getCriteria(criteria2))
        return criteria1Pool,criteria2Linked

    def getNPCTime(self,nameNPC,filter):
        return self.NPCs[self.npcNamesDict[nameNPC]].getNPCTime(filter)

    def getRoundsInOrderOfExperiencingRounds(self,round1,round2,crit):
        round1List = []
        round2List = []
        fights = self.getSubsetCritBy(self.participants,"fightsOrdered")
        for rounds in fights:
            round1List.append(rounds[round1].getCriteria(crit))
            round2List.append(rounds[round2].getCriteria(crit))
        return round1List,round2List

    def getRounds(self,round1,round2,crit):
        round1List = []
        round2List = []
        fights = self.getSubsetCritBy(self.participants,"fightsNPC")
        for rounds in fights:
            round1List.append(rounds[round1].getCriteria(crit))
            round2List.append(rounds[round2].getCriteria(crit))
        return round1List,round2List

    def getAnswers(self,round1,round2,crit):
        quiz1List = []
        quiz2List = []
        answers = self.getSubsetCritBy(self.participants, "answersOrdered")
        for quizes in answers:
            quiz1List.append(quizes[round1].getCriteria(crit))
            quiz2List.append(quizes[round2].getCriteria(crit))
        return quiz1List, quiz2List
    def getAnswersInOrderOfNPCSs(self,round1,round2,crit):
        quiz1List = []
        quiz2List = []
        answers = self.getSubsetCritBy(self.participants, "answersNPC")
        for quizes in answers:
            quiz1List.append(quizes[round1].getCriteria(crit))
            quiz2List.append(quizes[round2].getCriteria(crit))
        return quiz1List, quiz2List
    def getHowManyGamesThePlayerWon(self,participants):
        roundsWon = []
        for participant in participants:
            roundsWon.append(participant.getGamesWonByParticipant())
        return roundsWon


def deleteFromList(listOld, item):
    newList = []
    for i in listOld:
        if i != item:
            newList.append(i)
    return newList
