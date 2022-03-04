import matplotlib.pyplot as plt

file1 = open('AnalyseData.csv', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character
obj = []
frames=[]
for line in Lines:
    count += 1
    listNew = line.split(",")
    del listNew[0]
    for i in range(0,len(listNew)):
        listNew[i] = int(listNew[i])
    obj.append(listNew)

# obj[0].reverse()
# obj[1].reverse()
for i in range(1,len(obj[0])+1):
    frames.append(i)
plt.plot(frames, obj[0], 'b-', label='Australia')
plt.plot(frames, obj[1], 'g-', label='New Zealand')
plt.xlabel('Time (frames)')
plt.show()