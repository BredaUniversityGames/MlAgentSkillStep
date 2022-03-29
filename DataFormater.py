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

def plotAnswers(entryNo,numberOfEntries=1,question=None):
    answers = entries[entryNo:entryNo+numberOfEntries]
    index = entryNo
    for answer in answers:
        print("answer " + str(index * 22 +1))
        index+=1
        for fight in answer[1]:
            print(fight)
def printParticipantData():
    for entry in entries:
        print("e")
        print("e")
        for i in range(0,5):
            if(i<4):
                print(entry[i])
            else:
                for j in range(0,5):
                    print(entry[i][j])

def writeAllParticipantData():
    f = open("newFormat.csv", "a")
    stringW = ""
    for entry in entries:
        for i in range(0,5):
            if i==2: continue
            else:
                if(i!=1): stringW = ""
                if(i<4 and i!=2):

                    for j in entry[i]:
                        stringW += str(j)+","
                    if(i!=0):
                        stringW+="\n"
                        f.write(stringW)
                if i==4:
                    for j in range(0,5):
                        for k in entry[i][j]:
                            stringW = ""
                            for l in k:
                                stringW += str(l) + ","
                            stringW += "\n"
                            f.write(stringW)
    f.close()

for line in Lines:

    count += 1
    listNew = line.split(",")
    if (count%22 == 0):
        entry = []
        fights = [[],[],[],[],[]]
        participantData = listNew[0:10]
        participantAnswers = listNew[10:-1]
        # participantAnswers.append(listNew[22:34])
        # participantAnswers.append(listNew[35:47])
        # participantAnswers.append(listNew[48:60])
        # participantAnswers.append(listNew[61:73])
        # npcComparison = [listNew[34],listNew[47],listNew[60],listNew[73]]
        npcComparison = []
        entry.append(participantData)
        entry.append(participantAnswers)
        entry.append(npcComparison)
    elif (count % 22 == 1):
        entry.append(listNew[0:5])  # order of fighting
    else:
        countCurr = count % 22 - 2
        fightNr = int(countCurr / 4)
        rowNr = countCurr % 4
        if (rowNr == 0):
            fights[fightNr].append(listNew[0:3])  # aboutFightInfo(which NPC, whoWon, timeElapsed)
        else:
            hpList = []
            for i in range(0, len(listNew)):
                if (listNew[i] == "\n" or listNew[i] == ""): break  # fast solution to excel problem
                hpList.append(int(listNew[i]))
            fights[fightNr].append(hpList)

        if (count % 22 == 21):
            entry.append(fights)
            entries.append(entry)
        # fights [ [] , ........]
        # fights[fightNo] = [ [about] [hpNPC] [hpPlayer] [apmPlayer] ]
#
file1.close()
def addEmptyAPS():
    for entry in entries:
        for i in range(0, 5):
            entry[4][i].append([0 for i in range(0,len(entry[4][i][2]))])

def normalizeQuestionaryAnswers():
    for entry in entries:
        newEntryAnswers = []
        for i in range(0, len(entry[0])):
            newEntryAnswers.append(entry[0][i])
            if i==4:
                newEntryAnswers.append('3')
        entry[0] = newEntryAnswers
        # for i in range(0, 5):
        #     if(len(entry[1][i])!=12):
        #         print(entry[0][0] + " "+ str(i))
def reverseAnswersScale():
    for entry in entries:
        newEntryAnswers = []
        for i in range(0, len(entry[1])):
            if (i%14==10 or i%14==11) and entry[1][i]=='8':
                newEntryAnswers.append('-1')
            else: newEntryAnswers.append(entry[1][i])
        entry[1] = newEntryAnswers
# plotAnswers(1,1)
#addEmptyAPS()
#normalizeQuestionaryAnswers()
reverseAnswersScale()
#printParticipantData()
plotAnswers(0,28)
writeAllParticipantData()


