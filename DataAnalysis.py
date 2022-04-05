import copy

import matplotlib.pyplot as plt
import numpy as np

from DataBase import DataBase
from NPC import filterNPC
from Participant import Participant

file1 = open('AnalyseData.csv', 'r')
Lines = file1.readlines()
NPCDataExplained = ["Matches won/lost","All times per match","Avg time per match",
                    "All health remaining per matches","Avg health remaining per match", "All health from all of NPC and Player as well as aps of player"]
roundsAnchorman = ["-1st Round", "-2nd Round","-3rd Round","-4th Round","-5th Round"]
wonLossAnchorman = ["won","lost"]
entryNrLines = 22
entries = []
objectEntries = []
count = -1
# Strips the newline character
obj = []

entry = []
fights = [[],[],[],[],[]]


populationGenderProc = 0
populationAgeAvg = 0
populationNationProc = 0
populationEducProc = {}
populationExp = 0





def nohFilter(entry):
    return entry<15

def dotPlot(dataX,dataY,xlabel,ylabel):
    plt.plot(dataX,dataY,'o')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def populationDemographics(dataSet):
    global populationGenderProc
    global populationAgeAvg
    global populationNationProc
    global populationEducProc
    global populationExp
    aggregGender = []
    aggregAge = []
    aggregNation = []
    aggregEduc = []
    aggregNoh = []
    aggregExp = []
    for entry in dataSet:
        aggregGender.append(entry[0][2][0].lower())
        aggregAge.append(int(entry[0][1]))
        aggregNation.append(entry[0][3][0].lower())
        aggregEduc.append(int(entry[0][5]))
        aggregNoh.append(int(entry[0][6]))
        aggregExp.append(entry[0][7][0])
    populationAgeAvg = getAvgNumber(aggregAge)
    populationGenderProc = getPercentageForCriteria(aggregGender,"m")
    populationNationProc = getPercentageForCriteria(aggregNation,"r")
    populationEducProc["school"] = getPercentageForCriteria(aggregEduc, 0)
    populationEducProc["highschool"] = getPercentageForCriteria(aggregEduc,1)
    populationEducProc["bachelor"] = getPercentageForCriteria(aggregEduc, 2)
    populationEducProc["master"] = getPercentageForCriteria(aggregEduc, 3)
    populationExp = getPercentageForCriteria(aggregExp,"T")
    print(getPercentageForFilter(aggregNoh,nohFilter))
    print(populationAgeAvg)
    print(populationGenderProc)
    print(populationNationProc)
    print(populationEducProc)
    print(populationExp)









def NPCDataAnalyser(dataSet):
    NPCList = {}
    for entry in dataSet:
        for fights in entry[4]:
            NPCList[fights[0][0]] = []
    for npc in NPCList:
        NPCList[npc].append([[0,0],[0,0],[0,0],[0,0],[0,0]]) #first one is for who won in what round
        NPCList[npc].append([[[], []], [[], []], [[], []], [[], []], [[], []]])  # 2nd one is for time in what round
        NPCList[npc].append([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
        NPCList[npc].append([[[], []], [[], []], [[], []], [[], []], [[], []]])   # 3th one is for left hp after each round
        NPCList[npc].append([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
        NPCList[npc].append([[[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []]]) # Hp of NPC, Hp of player and aps over time
    for entry in dataSet:
        for roundFight in range(0,5):
            npc = entry[3][roundFight]-1
            fightDetails = entry[4][npc]
            npcName = fightDetails[0][0]
            NPCList[npcName][5][roundFight][0].append(fightDetails[1])
            NPCList[npcName][5][roundFight][1].append(fightDetails[2])
            NPCList[npcName][5][roundFight][2].append(fightDetails[3])
            #print(fightDetails[0])
            if (fightDetails[0][1]==0): #if human lost
                NPCList[npcName][0][roundFight][0] += 1 #first position is for npc
                NPCList[npcName][1][roundFight][0].append(fightDetails[0][2])
                NPCList[npcName][2][roundFight][0] += fightDetails[0][2]
                NPCList[npcName][3][roundFight][0].append(fightDetails[1][len(fightDetails[1])-1])
                NPCList[npcName][4][roundFight][0] += fightDetails[1][len(fightDetails[1]) - 1]

            else:
                NPCList[npcName][0][roundFight][1] += 1
                NPCList[npcName][1][roundFight][1].append(fightDetails[0][2])
                NPCList[npcName][2][roundFight][1] += fightDetails[0][2]
                NPCList[npcName][3][roundFight][1].append(fightDetails[2][len(fightDetails[2]) - 1])
                NPCList[npcName][4][roundFight][1] += fightDetails[2][len(fightDetails[2]) - 1]
    for npc in NPCList:#compute Avgs
        for roundFight in range(0,5):
            for outcome in range(0,2):
                if NPCList[npc][0][roundFight][outcome]!=0: #avoid division by 0
                    NPCList[npc][2][roundFight][outcome]/=NPCList[npc][0][roundFight][outcome]
                    NPCList[npc][4][roundFight][outcome] /= NPCList[npc][0][roundFight][outcome]
    printNPCList(NPCList)


def plotBoxAvg(data, nameOfData):

    fig1, ax1 = plt.subplots()
    ax1.set_title(nameOfData)
    ax1.boxplot(data)
    plt.show()

def getAvgNumber(data):
    howMany = len(data)
    sumAgg = 0
    for e in data:
        sumAgg += e
    return sumAgg/howMany

def getPercentageForCriteria(data, criteria):
    howManyTotal = len(data)
    howManyCrit = 0
    for e in data:
        if e == criteria:
            howManyCrit+=1
    return howManyCrit * 100 / howManyTotal

def getPercentageForFilter(data, criteria):
    howManyTotal = len(data)
    howManyCrit = 0
    for e in data:
        if criteria(e):
            howManyCrit+=1
    return howManyCrit * 100 / howManyTotal

def plotAvgTimeOfAllNPCs(NPCList):
    aggregTime= []
    for npc in NPCList:
        concatAllTimesNPC = []
        for roundFight in range(0, 5):
            for outcome in range(0, 2):
                concatAllTimesNPC = concatAllTimesNPC + NPCList[npc][1][roundFight][outcome]
        aggregTime.append(concatAllTimesNPC)
    plotBoxAvg(aggregTime, "Average time of each NPC")


def plotHPofNPCOverTime(NPCList, npc):
    for roundFight in range(0,5):
        for fight in NPCList[npc][5][roundFight][1]:
            plt.plot(range(0,len(fight)),fight)
        plt.title("HP of " + npc + " in round " + str(roundFight))
        plt.show()

def plotHPofPlayerOverTime(NPCList, npc):
    for roundFight in range(0,5):
        for fight in NPCList[npc][5][roundFight][2]:
            plt.plot(range(0,len(fight)),fight)
        plt.title("HP of " + npc + " in round " + str(roundFight))
        plt.show()

def printNPCList(NPCList):
    plotAvgTimeOfAllNPCs(NPCList)
    for npc in NPCList:
        plotWonLostOverRounds(NPCList,npc)
        plotHPofNPCOverTime(NPCList,npc)
        plotHPofPlayerOverTime(NPCList,npc)
        #plotResponsesOfNPC()

def plotWonLostOverRounds(NPCList, npc):
    aggregWon = []
    aggregLost = []
    for roundFight in range(0, 5):
        for outcome in range(0, 2):
            if outcome == 0:
                aggregWon.append(NPCList[npc][1][roundFight][outcome])
            else:
                aggregLost.append(NPCList[npc][1][roundFight][outcome])
    plotBoxAvg(aggregWon, npc + " " + NPCDataExplained[1] + " " + wonLossAnchorman[0])
    plotBoxAvg(aggregLost, npc + " " + NPCDataExplained[1] + " " + wonLossAnchorman[1])

    concatWon = []
    concatLost = []
    for round in aggregLost:
        concatLost = concatLost + round
    for round in aggregWon:
        concatWon = concatWon + round
    plotBoxAvg([concatWon,concatLost], npc + " Average time per all matches won/lost")

def plotGraphAnswersFight(answers, npc):
    # fig, ax = plt.subplots()
    #
    # ax.hist(answers, bins=14, linewidth=1, edgecolor="white")
    # # ax.set(xlim=(0, 14), xticks=np.arange(1, 14),
    # #        ylim=(0, 7), yticks=np.linspace(0, 7, 14))
    # plt.title(str(npc) + "responses")
    # plt.show()
    values = copy.deepcopy(answers)
    del values[13]
    del values[3]
    labels = ["Enjoyment","NPC skill","Player Skill","attack","defend","move","aggresive","riposte","reactive","human","predictable","adaptive"]
    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width, align='center',edgecolor = "black")

    plt.xticks(indexes, labels)  # Replace default x-ticks with xs, then replace xs with labels
    plt.yticks(values)
    plt.show()

def masterDataAnalyserEntry(entryNo):
    plotAnswers(entryNo)
    for roundFight in range(0,5):
        plotGraphAnswersFight(entries[entryNo][1][roundFight],entries[entryNo][4][entries[entryNo][3][roundFight]-1][0][0])
    plotFights(entryNo)

def plotFight(entryNr,fightNr):

    fight = entries[entryNr][4][fightNr]
    frames = []
    for i in range(1, len(fight[1]) + 1):
        frames.append(i)
    plt.plot(frames, fight[1], 'b-', label='NPC')
    plt.plot(frames, fight[2], 'g-', label='Player')
    plt.plot(frames, fight[3], 'r-', label='Aps Of Player')

    z1 = np.array(fight[1])
    z2 = np.array(fight[2])
    plt.fill_between(frames,fight[1], fight[2],
                     where=(z1 >= z2),
                     color='b',alpha=0.5, interpolate=True)
    plt.fill_between(frames, fight[1], fight[2],
                     where=(z1 <= z2),
                     color='g', alpha=0.5, interpolate=True)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Health')
    plt.title('Round against ' + entries[entryNr][4][fightNr][0][0])
    plt.legend()
    plt.show()

def plotFights(entryNr):
    for i in range(0,5):
        plotFight(entryNr,i)

def plotAnswers(entryNo,numberOfEntries=1,question=None):
    answers = entries[entryNo:entryNo+numberOfEntries]
    index = entryNo
    for answer in answers:
        print("answer " + str(index * 22 +1))
        index+=1
        for fight in answer[1]:
            print(fight)

def printParticipantsData(entryNo,numberOfEntries=1):
    answers = entries[entryNo:entryNo+numberOfEntries]
    index = entryNo
    for answer in answers:
        print("answer " + str(index * 22 +1))
        index+=1
        for dataRow in range(0,5):
            if dataRow==1:
                for fight in answer[dataRow]:
                    print(fight)
            elif dataRow==4:
                for fight in answer[dataRow]:
                    for detail in fight:
                        print(detail)
            else:
                print(answer[dataRow])
    #plotFights(entryNo)
def getAvgAnswers():
    answers = copy.deepcopy(entries[0][1])
    for i in range(0, 5):
        for j in range(0, 12):
            answers[i][j] = 0
    for entry in entries:
        for i in range(0,5):
            for j in range(0,12):
                answers[i][j] += int(entry[1][i][j])
    for i in range(0, 5):
        for j in range(0, 12):
            answers[i][j] /= len(entries)
    return answers

def getVarianceAnsers():
    answers = copy.deepcopy(entries[0][1])
    mean = getAvgAnswers()
    for i in range(0, 5):
        for j in range(0, 12):
            answers[i][j] = 0
    for entry in entries:
        for i in range(0, 5):
            for j in range(0, 12):
                deviation = int(entry[1][i][j])-mean[i][j]
                answers[i][j] += deviation*deviation
    for i in range(0, 5):
        for j in range(0, 12):
            answers[i][j] /= len(entries)
    return answers

for line in Lines:

    count += 1
    listNew = line.replace('\n','').split(",")

    if (count%22 == 0):
        entry = []
        fights = [[],[],[],[],[]]
        participantData = listNew[0:10]
        participantData[1] = int(participantData[1])
        participantData[4] = int(participantData[4])
        participantData[5] = int(participantData[5])
        participantData[6] = int(participantData[6])
        for i in range(10, len(listNew)):
            if (listNew[i] == "\n" or listNew[i] == ""): break  # fast solution to excel problem
            listNew[i]=int(listNew[i])
        participantAnswers = [listNew[10:10+14], listNew[10+14:10+14*2], listNew[10+14*2:10+14*3], listNew[10+14*3:10+14*4], listNew[10+14*4:10+14*5]]
        npcComparison = [participantAnswers[0][13],participantAnswers[1][13],participantAnswers[2][13],participantAnswers[3][13],participantAnswers[4][13]]
        entry.append(participantData)
        entry.append(participantAnswers)
        entry.append(npcComparison)
    elif (count % 22 == 1):
        for i in range(0, len(listNew)):
            if (listNew[i] == "\n" or listNew[i] == ""): break  # fast solution to excel problem
            listNew[i] = int(listNew[i])
        entry.append(listNew[0:5]) # order of fighting
    else:
        if listNew[0] == "1" or listNew[0] == "2" or listNew[0] == "3" or listNew[0] == "4" or listNew[0] == "5":
            del listNew[0]
        countCurr = count%22-2
        fightNr = int(countCurr/4)
        rowNr = countCurr%4
        if (rowNr == 0):
            fights[fightNr].append([listNew[0],int(listNew[1]),int(listNew[2])]) # aboutFightInfo(which NPC, whoWon, timeElapsed)
        else:
            hpList = []
            for i in range(0,len(listNew)):
                if (listNew[i] == "\n" or listNew[i] == ""): break #fast solution to excel problem
                hpList.append(int(listNew[i]))
            fights[fightNr].append(hpList)

        if (count%22==21):
            entry.append(fights)
            objectEntries.append(Participant(entry))
            entries.append(entry)
        # fights [ [] , ........]
        # fights[fightNo] = [ [about] [hpNPC] [hpPlayer] [apmPlayer] ]

dataBase = DataBase(objectEntries)

printParticipantsData(43,1)
#print(getVarianceAnsers())
# populationDemographics(entries)
# dataBase.nohIncresesReportedSkillOfPlayer(15)
# dataBase.genderIncresesReportedSkillOfPlayer()
#dataBase.ageIncresesReportedSkillOfPlayer()
#dataBase.linkTwoDataPoints("age","skillPlayer",plotOpt="dot")
#dataBase.linkOnePointWithArrayAvg("noh","skillPlayer",plotOpt="dot")
# print(getAvgNumber(dataBase.getNPCRemainingHP("10")))
# print(getAvgNumber(dataBase.getNPCRemainingHP("100")))
# print(getAvgNumber(dataBase.getNPCRemainingHP("1k")))
# print(getAvgNumber(dataBase.getNPCRemainingHP("100K")))
# print(getAvgNumber(dataBase.getNPCRemainingHP("1000K")))
#
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("10")))
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("100")))
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("1k")))
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("100K")))
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("1000K")))

#print(dataBase.linkCriteriasFromAllFights("skillPlayer","measuredSkill"))
print(len(dataBase.getNPCTime("10",filterNPC.filterMatchesWonByNPC)))
print(len(dataBase.getNPCTime("10",filterNPC.filterMatchesLostByNPC)))
print(dataBase.linkCriteriasFromAllFights("enjoy","measuredSkill"))
print(dataBase.linkCriteriasFromAllFights("enjoy","skillPlayer"))

# print(dataBase.linkTwoDataPoints("gen","skillPlayer"))
# masterDataAnalyserEntry(43)
# NPCDataAnalyser(entries)