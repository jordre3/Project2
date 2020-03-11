import sys
import pandas as pd
from scipy.io import arff

trainFile = open("ALL_AML_SigGene.train.arff", 'r')
testFile = open("ALL_AML_SigGene.test.arff", 'r')

k = 3

line = trainFile.readline()
while "@data" not in line:
    line = trainFile.readline()

trainData = []
dataLine = trainFile.readline()
while dataLine is not "":
    dataLine = dataLine.split(',')
    trainData.append(dataLine)
    dataLine = trainFile.readline()
print(trainData)

line = testFile.readline()
while "@data" not in line:
    line = testFile.readline()

testData = []
dataLine = testFile.readline()
while dataLine is not "":
    dataLine = dataLine.split(',')
    testData.append(dataLine)
    dataLine = testFile.readline()
print(testData)

anotherList = []
for rowTest in testData:
    listDist = []
    x = 0
    while x < len(trainData):
        i = 0
        dist = 0
        while i < len(trainData[0]) - 1:
            dist += abs(float(rowTest[i]) - float(trainData[x][i]))
            i += 1
        listDist.append([dist, x])
        x += 1
    listDist.sort()
    anotherList.append(listDist)

print(anotherList)
finalLabelList = []
for row in anotherList:
    i = 0
    nearestLabels = []
    while i < k:
        label = trainData[row[i][1]][len(trainData[0]) - 1].strip('\n')
        nearestLabels.append(label)
        i += 1
    finalLabelList.append(nearestLabels)

print(finalLabelList)
classifications = []
for sample in finalLabelList:
    classLabel1 = sample[0]
    classLabel2 = ''
    class1 = 0
    class2 = 0
    for label in sample:
        if label != classLabel1:
            classLabel2 = label
            class2 += 1
        else:
            class1 += 1
    if(class2 > class1):
        classifications.append(classLabel2)
    else:
        classifications.append(classLabel1)
print(classifications)
i = 0
wrongCount = 0
for row in testData:
    if row[len(testData[0]) - 1].strip('\n') != classifications[i]:
        wrongCount += 1
        print(i)
    i += 1

print(wrongCount)
#trainingData = arff.loadarff("ALL_AML_SigGene.train.arff")
#testData = arff.loadarff("ALL_AML_SigGene.test.arff")

#df = pd.DataFrame(trainingData)
#print(df[0].size)
#print(df[1][0][0])
