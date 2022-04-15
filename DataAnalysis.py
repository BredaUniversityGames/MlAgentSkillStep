import copy

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from DataBase import DataBase
from NPC import filterNPC
from Participant import Participant
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

savePlots = True

file1 = open('AnalyseData.csv', 'r')
Lines = file1.readlines()
NPCDataExplained = ["Matches won/lost","All times per match","Avg time per match",
                    "All health remaining per matches","Avg health remaining per match", "All health from all of NPC and Player as well as aps of player"]
roundsAnchorman = ["-1st Round", "-2nd Round","-3rd Round","-4th Round","-5th Round"]
wonLossAnchorman = ["won","lost"]
entryNrLines = 22
alpha = 0.05
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
    return entry>2

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

def plotBar():
    N = 5
    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(ind, menMeans, width, color='r')
    ax.bar(ind, womenMeans, width, bottom=menMeans, color='b')
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    ax.set_yticks(np.arange(0, 8, 10))
    ax.legend(labels=['Men', 'Women'])
    plt.xticks()
    plt.yticks()
    plt.show()

def plotBarMultipleColors(data, nameOfData, labels, yTicks=None, xTicksLabels=None, error=None):
    mpl.style.use('default')
    X = np.arange(len(data[0]))
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    ax.bar(X - 0.25, data[0], yerr=error[0], color='m', width=0.25, error_kw=dict(lw=1, capsize=5, capthick=1))
    ax.bar(X + 0.00, data[1], yerr=error[1], color='c', width=0.25, error_kw=dict(lw=1, capsize=5, capthick=1))
    if (len(data)>2):
        ax.bar(X + 0.25, data[2], yerr=error[2],color='y', width=0.25, error_kw=dict(lw=1, capsize=5, capthick=1))
    if (len(data) > 3): raise Exception("data size too big")
    ax.set_title(nameOfData)
    ax.set_xticks(X,xTicksLabels)
    ax.set_yticks(np.arange(0, 6.5, 0.5))
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    plt.xlabel('NPCs')
    plt.ylabel('Rating')
    ax.legend(labels=labels)
    # fig.suptitle("hello")
    showOrSavePlot(nameOfData)

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
        for fight in NPCList[npc][5][roundFight][0]:
            plt.plot(range(0,len(fight)),fight)
        plt.title("HP of " + npc + " in round " + str(roundFight))
        plt.show()

def plotHPofPlayerOverTime(NPCList, npc):
    for roundFight in range(0,5):
        for fight in NPCList[npc][5][roundFight][1]:
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

def showOrSavePlot(namePlt=None):
    global savePlots
    if savePlots:
        # namePlt = namePlt.split(":")
        # nameNPC = namePlt[1]
        # namePlt = namePlt[0]
        plt.savefig("Plots/"+namePlt+".png")
        plt.close()
    else:
        plt.show()

def plotFight(entryNr,fightNr):

    fight = entries[entryNr][4][fightNr]
    frames = []
    for i in range(1, len(fight[1]) + 1):
        frames.append(i)
    if len(fight[3]) < len(frames):
        fight[3].append(0)
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
    showOrSavePlot("Participant " + str(entryNr) + ' Round against :' + entries[entryNr][4][fightNr][0][0])

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

def plotHistogram(data, xlabel, ylabel, title, binsDensity = 3):
    plt.hist(data, color='blue', edgecolor='black',
             bins=int(len(data) / binsDensity))

    # Add labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    showOrSavePlot(title)

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

def sort2Arrays(arr1,arr2):
    for i in range(1,len(arr1)):
        if arr1[i] < arr1[i-1]:
            aux = arr1[i]
            arr1[i] = arr1[i-1]
            arr1[i-1] = aux
            aux = arr2[i]
            arr2[i] = arr2[i - 1]
            arr2[i - 1] = aux
    return arr1,arr2

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

# printParticipantsData(43,1)
#print(getVarianceAnsers())
#populationDemographics(entries)
# dataBase.nohIncresesReportedSkillOfPlayer(15)
# dataBase.genderIncresesReportedSkillOfPlayer()
#dataBase.ageIncresesReportedSkillOfPlayer()
# dataBase.linkOnePointWithArrayAvg("age","skillPlayer",plotOpt="dot")
# dataBase.linkOnePointWithArrayAvg("noh","skillPlayer",plotOpt="dot")
# print(getAvgNumber(dataBase.getNPCRemainingHP("10")))
# print(getAvgNumber(dataBase.getNPCRemainingHP("100")))
# print(getAvgNumber(dataBase.getNPCRemainingHP("1k")))
# print(getAvgNumber(dataBase.getNPCRemainingHP("100k")))
# print(getAvgNumber(dataBase.getNPCRemainingHP("1000k")))
#
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("10")))
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("100")))
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("1k")))
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("100k")))
# print(getAvgNumber(dataBase.getDiffHPatTheEnd("1000k")))
#
# print(dataBase.linkCriteriasFromAllFights("skillPlayer","measuredSkill"))
# print(dataBase.getNPCTime("10",filterNPC.filterMatchesWonByNPC))
# print(dataBase.getNPCTime("10",filterNPC.filterMatchesLostByNPC))
#
# print(dataBase.linkCriteriasFromAllFights("enjoy","measuredSkill"))
# print(dataBase.linkCriteriasFromAllFights("enjoy","skillPlayer"))
# print(dataBase.linkOnePointWithArrayAvg("name","human",nameNPC=True,excludeMinus=True))
# print(dataBase.linkOnePointWithArrayAvg("name","predictable",nameNPC=True,excludeMinus=True))
# print(dataBase.linkOnePointWithArrayAvg("name","delayed",nameNPC=True,excludeMinus=True))
# print(dataBase.linkOnePointWithArrayAvg("name","exploitable",nameNPC=True,excludeMinus=True))
# print(dataBase.linkOnePointWithArrayAvg("name","exploitable",nameNPC=True,excludeMinus=True))
# print(dataBase.linkOnePointWithArrayCount("name","defenseNPC",nameNPC=True,countWhat=1))
# print(dataBase.linkOnePointWithArrayCount("name","defensePlayer",nameNPC=True,countWhat=1))
# print(dataBase.linkOnePointWithArrayCount("name","attacksNPC",nameNPC=True,countWhat=1))
# print(dataBase.linkOnePointWithArrayCount("name","attacksPlayers",nameNPC=True,countWhat=1))
# print(dataBase.linkOnePointWithArrayAvg("name","skillNPC",nameNPC=True,excludeMinus=True))
# print(dataBase.linkOnePointWithArrayAvg("name","skillPlayer",nameNPC=True,excludeMinus=True))
# print(dataBase.linkOnePointWithArrayAvg("name","skillRelative",nameNPC=True,excludeMinus=True))
#
# npcNames, attkData = dataBase.linkOnePointWithArrayAvg("name","skillAttack",nameNPC=True,excludeMinus=True,Avg=False)
# npcNames, moveData = dataBase.linkOnePointWithArrayAvg("name","skillMove",nameNPC=True,excludeMinus=True,Avg=False)
# npcNames, defendData = dataBase.linkOnePointWithArrayAvg("name","skillDefend",nameNPC=True,excludeMinus=True,Avg=False)
# #
#
# attkDataErr = []
# moveDataErr = []
# defendDataErr = []
# for i in attkData:
#     attkDataErr.append(np.std(i))
# for i in moveData:
#     moveDataErr.append(np.std(i))
# for i in attkData:
#     defendDataErr.append(np.std(i))
# print(attkDataErr,moveDataErr,defendDataErr)
# for i in range(0,5):
#     attkData[i] = np.mean(attkData[i])
#     moveData[i] = np.mean(moveData[i])
#     defendData[i] = np.mean(defendData[i])
#
#
# plotBarMultipleColors([attkData,moveData,defendData],"Reported Skill", ["attack","move","defend"], xTicksLabels=npcNames, error=[attkDataErr,moveDataErr,defendDataErr])
#plotBar()
# npcNames, skillNPC = dataBase.linkOnePointWithArrayAvg("name","skillNPC",nameNPC=True,excludeMinus=True,Avg=False)
# npcNames, skillPlayer = dataBase.linkOnePointWithArrayAvg("name","skillPlayer",nameNPC=True,excludeMinus=True,Avg=False)
#
#
# skillNPCErr = []
# skillPlayerErr = []
# for i in skillNPC:
#     skillNPCErr.append(np.std(i))
# for i in skillPlayer:
#     skillPlayerErr.append(np.std(i))
# print(skillNPCErr)
# for i in range(0,5):
#     skillNPC[i] = np.mean(skillNPC[i])
#     skillPlayer[i] = np.mean(skillPlayer[i])
#
# plotBarMultipleColors([skillNPC,skillPlayer],"Competitor Skill", ["skill NPC","skill Player"], xTicksLabels=npcNames, error=[skillNPCErr,skillPlayerErr] )

# # playersPlayingALot = dataBase.filterBy("noh",">=",15)
#
# # for npc in dataBase.NPCs:
# #     presenceNPCs = dataBase.getSubsetCritBy([npc],"participant")
# #
# #     NPCFightPlayerNoh = dataBase.filterSubsetBy(presenceNPCs[0],"identity", "==", playersPlayingALot)
# #
# matchOrd,grade = dataBase.participants[36].getComparisonNPCAnalysis()
# print(matchOrd,grade)
# # print(dataBase.linkOnePointWithArrayAvg("gen","skillPlayer"))
# # masterDataAnalyserEntry(43)
# NPCDataAnalyser(entries)
# allNPCs = dataBase.getSubsetCritBy(dataBase.participants,"fights")
#
# baseline, round1 = dataBase.getRounds(0,1,"measuredSkill")
# # plotHistogram(baseline,"Measured Skill","Fights", "Distribution of Measured skill for NPC 10")
# # plotHistogram(round1,"Measured Skill","Fights", "Distribution of Measured skill for NPC 100")
# round2, round3 = dataBase.getRounds(2,3,"measuredSkill")
# round3, round5 = dataBase.getRounds(3,4,"measuredSkill")

# npcNames, timeNPC = dataBase.linkOnePointWithArrayAvg("name","whoWon",nameNPC=True,excludeMinus=True,Avg=False)
#
# npcWinPerc = []
# for i in timeNPC:
#     npcWin = 0
#     for j in i:
#         if j==0:
#             npcWin+=1
#     npcWin = npcWin * 100/len(i)
#     npcWinPerc.append(npcWin)
#     print(npcWin)
# npcNames, skillNPC = dataBase.linkOnePointWithArrayAvg("name","skillNPC",nameNPC=True,excludeMinus=True,Avg=False)
# npcNames, skillMeasuredNPC = dataBase.linkOnePointWithArrayAvg("name","measuredSkill",nameNPC=True,excludeMinus=True,Avg=False)
#
#
# skillNPCErr = []
# skillMeasuredNPCErr = []
# for i in skillNPC:
#     skillNPCErr.append(np.std(i))
# for i in skillMeasuredNPC:
#     skillMeasuredNPCErr.append(np.std(i))
# print(skillNPCErr)
# for i in range(0,5):
#     skillNPC[i] = np.mean(skillNPC[i])
#     skillMeasuredNPC[i] = np.mean(skillMeasuredNPC[i])
#     skillMeasuredNPC[i] = skillMeasuredNPC[i] / (352/7) + 3 #get it at the level of the rating (total HP deviation devided by the scale)
#     skillMeasuredNPCErr[i] = skillMeasuredNPCErr[i] / (352/7)
#
# print()
# plotBarMultipleColors([skillMeasuredNPC, skillNPC],"Measured vs Reported Skill Of NPCs", ["Measured Skill", "Reported Skill"], xTicksLabels= npcNames, error=[skillMeasuredNPCErr, skillNPCErr])

# plotBarMultipleColors([skillMeasuredNPC, skillNPC],"Measured vs Reported Skill Of NPCs", ["Measured Skill", "Reported Skill"], xTicksLabels= npcNames)

# plotHistogram(round2,"Measured Skill","Fights", "Distribution of Measured skill for NPC 1k")
# plotHistogram(round3,"Measured Skill","Fights", "Distribution of Measured skill for NPC 100k")
# plotHistogram(round5,"Measured Skill","Fights", "Distribution of Measured skill for NPC 1000k")
# baseline, round1 = dataBase.getAnswersInOrderOfNPCSs(0,1,"skillNPC")
#
# # plotHistogram(baseline,"Reported Skill","Fights", "Distribution of Reported skill for NPC 10",4)
# # plotHistogram(round1,"Reported Skill","Fights", "Distribution of Reported skill for NPC 100",4)
# round2, round3 = dataBase.getAnswersInOrderOfNPCSs(2,3,"skillNPC")
# round3, round4 = dataBase.getAnswersInOrderOfNPCSs(3,4,"skillNPC")
#
# plotHistogram(round2,"Reported Skill","Fights", "Distribution of Reported skill for NPC 1k",4)
# plotHistogram(round3,"Reported Skill","Fights", "Distribution of Reported skill for NPC 100k",4)
# plotHistogram(round4,"Reported Skill","Fights", "Distribution of Reported skill for NPC 1000k",4)
# baseline, round1 = dataBase.getRounds(0,1,"measuredSkill")
# t_value,p_value=stats.ttest_ind(baseline,round1,equal_var=False)
# print(t_value)
# print(p_value)
# baseline, round1 = dataBase.getRounds(0,2,"measuredSkill")
# t_value,p_value=stats.ttest_ind(baseline,round1,equal_var=False)
# print(t_value)
# print(p_value)
# baseline, round1 = dataBase.getRounds(0,3,"measuredSkill")
# t_value,p_value=stats.ttest_ind(baseline,round1,equal_var=False)
# print(t_value)
# print(p_value)
# baseline, round1 = dataBase.getRounds(0,4,"measuredSkill")
# t_value,p_value=stats.ttest_ind(baseline,round1,equal_var=False)
# print(t_value)
# print(p_value)
# baseline, round1 = dataBase.getRoundsInOrderOfExperiencingRounds(2,4,"measuredSkill")
# t_value,p_value=stats.ttest_ind(baseline,round1,equal_var=False)
# print(t_value)
# print(p_value)
# baseline, round1 = dataBase.getRoundsInOrderOfExperiencingRounds(0,4,"totalDmgDoneToPlayer")
# t_value,p_value=stats.ttest_ind(baseline,round1,equal_var=False)
# print(t_value)
# print(p_value)
# baseline, round1 = dataBase.getAnswersInOrderOfExperiencingRounds(0,1,"skillNPC")
# t_value,p_value=stats.ttest_ind(baseline,round1)
# print(t_value)
# print(p_value)
# baseline, round1 = dataBase.getAnswersInOrderOfNPCSs(0,4,"skillNPC")
# t_value,p_value=stats.ttest_ind(baseline,round1)
# print(t_value)
# print(p_value)



#ANOVA TEST skill for all
# fvalue, pvalue = stats.f_oneway(baseline, round1, round2, round3,round4)
# print(fvalue, pvalue)
# fvalue, pvalue = stats.f_oneway(attkData[0],attkData[1],attkData[2],attkData[3],attkData[4])
# print(fvalue, pvalue)
# fvalue, pvalue = stats.f_oneway(moveData[0],moveData[1],moveData[2],moveData[3],moveData[4])
# print(fvalue, pvalue)
# fvalue, pvalue = stats.f_oneway(defendData[0],defendData[1],defendData[2],defendData[3],defendData[4])
# print(fvalue, pvalue)

# experiencedParticipants = dataBase.filterBy("exp","==","true")
#
# wonOneFightPlus = dataBase.filterSubsetBy(experiencedParticipants,"gamePerformance","<=",0)
#
# gamesWon = dataBase.getHowManyGamesThePlayerWon(wonOneFightPlus)
# print(np.mean(gamesWon))
#
# inexperiencedParticipants = dataBase.filterBy("exp","!=","true")
#
# print(len(inexperiencedParticipants))
# inExpWonOneFightPlus = dataBase.filterSubsetBy(inexperiencedParticipants,"gamePerformance","<=",0)
#
# inExpGamesWon = dataBase.getHowManyGamesThePlayerWon(inExpWonOneFightPlus)
# print(inExpGamesWon)
# print(np.mean(inExpGamesWon))
# #
# won3Plus = dataBase.filterSubsetBy(dataBase.participants,"getGamesWonByParticipant",">=",3)
# print(len(won3Plus))
# aps = dataBase.getSubsetCritBy(won3Plus,"getAPS")
# del aps[0:2]
# time = dataBase.getSubsetCritBy(won3Plus,"hpDiff")
# apsMean = []
# for i in aps:
#     playerMean = []
#     for j in i:
#         playerMean.append(np.mean(j))
#     apsMean.append(np.mean(playerMean))
#
# print(np.mean(apsMean))
# timeMean = []
# for i in time:
#     playerMean = []
#     for j in i:
#         playerMean.append(np.mean(j))
#     timeMean.append(np.mean(playerMean))
#
# print(np.mean(timeMean))
#
#
# won2Less = dataBase.filterSubsetBy(dataBase.participants,"getGamesWonByParticipant","<=",2)
# print(len(won2Less))
# aps = dataBase.getSubsetCritBy(won2Less,"getAPS")
# del aps[0:3]
# time = dataBase.getSubsetCritBy(won2Less,"time")
# apsMean = []
# for i in aps:
#     playerMean = []
#     for j in i:
#         playerMean.append(np.mean(j))
#     apsMean.append(np.mean(playerMean))
# print(np.mean(apsMean))
# timeMean = []
# print(time)
# for i in time:
#     playerMean = []
#     for j in i:
#         playerMean.append(np.mean(j))
#     timeMean.append(np.mean(playerMean))
#
# print(np.mean(timeMean))

# enjoyment = dataBase.getSubsetCritBy(dataBase.participants,"enjoy",">=",4)
# print(len(enjoyment))
# print(np.mean(enjoyment))
npcNames, skillNPC = dataBase.linkOnePointWithArrayAvg("name","predictable",nameNPC=True,excludeMinus=True,Avg=False)
npcNames, skillMeasuredNPC = dataBase.linkOnePointWithArrayAvg("name","riposte",nameNPC=True,excludeMinus=True,Avg=False)
npcNames, delayed = dataBase.linkOnePointWithArrayAvg("name","exploitable",nameNPC=True,excludeMinus=True,Avg=False)

skillNPCErr = []
skillMeasuredNPCErr = []
skillDelayErr = []
for i in skillNPC:
    skillNPCErr.append(np.std(i))
for i in skillMeasuredNPC:
    skillMeasuredNPCErr.append(np.std(i))
for i in delayed:
    skillDelayErr.append(np.std(i))
print(skillNPCErr)
for i in range(0,5):
    skillNPC[i] = np.mean(skillNPC[i])
    skillMeasuredNPC[i] = np.mean(skillMeasuredNPC[i])
    delayed[i] = np.mean(delayed[i])
plotBarMultipleColors([skillMeasuredNPC, skillNPC , delayed],"Other attributes Of NPCs", ["Predictable", "Riposte", "Exploitable"], xTicksLabels= npcNames, error=[skillMeasuredNPCErr, skillNPCErr, skillDelayErr])

