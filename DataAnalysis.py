import copy

import matplotlib.pyplot as plt
import numpy as np
file1 = open('AnalyseData.csv', 'r')
Lines = file1.readlines()

entryNrLines = 22
entries = []
count = -1
# Strips the newline character
obj = []

entry = []
fights = [[],[],[],[],[]]

def plotFight(entryNr,fightNr):
    fight = entries[entryNr][4][fightNr]
    frames = []
    for i in range(1, len(fight[1]) + 1):
        frames.append(i)
    plt.plot(frames, fight[1], 'b-', label='NPC')
    plt.plot(frames, fight[2], 'g-', label='Player')
    plt.plot(frames, fight[3], 'r-', label='Aps Of Player')
    plt.xlabel('Time (seconds)')
    plt.show()

def plotAnswers(entryNo,question):
    answers = entries[entryNo][1]
    for fight in answers:
        print(fight)

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
    listNew = line.split(",")

    if (count%22 == 0):
        entry = []
        fights = [[],[],[],[],[]]
        participantData = listNew[0:10]
        participantAnswers = []
        participantAnswers.append(listNew[9:21])
        participantAnswers.append(listNew[22:34])
        participantAnswers.append(listNew[35:47])
        participantAnswers.append(listNew[48:60])
        participantAnswers.append(listNew[61:73])
        npcComparison = [listNew[34],listNew[47],listNew[60],listNew[73]]
        entry.append(participantData)
        entry.append(participantAnswers)
        entry.append(npcComparison)
    elif (count % 22 == 1):
        entry.append(listNew[0:5]) # order of fighting
    else:
        del listNew[0]
        countCurr = count%22-2
        fightNr = int(countCurr/4)
        rowNr = countCurr%4
        if (rowNr == 0):
            fights[fightNr].append(listNew[0:3]) # aboutFightInfo(which NPC, whoWon, timeElapsed)
        else:
            hpList = []
            for i in range(0,len(listNew)):
                if(listNew[i]==""): break #fast solution to excel problem
                hpList.append(int(listNew[i]))
            fights[fightNr].append(hpList)

        if (count%22==21):
            entry.append(fights)
            entries.append(entry)
        # fights [ [] , ........]
        # fights[fightNo] = [ [about] [hpNPC] [hpPlayer] [apmPlayer] ]
#
plotFight(1,0)
plotFight(1,1)
plotFight(1,2)
plotFight(1,3)
plotFight(1,4)
plotAnswers(1,1)
print(getVarianceAnsers())