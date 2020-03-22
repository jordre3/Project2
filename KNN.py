import sys
import math


def doStuff(anotherList, distMeasure):
    finalLabelList = []
    print("FOR " + distMeasure + " DISTANCE AND K = " + str(k) + ":")
    for row in anotherList:
        i = 0
        nearestLabels = []
        while i < k:
            label = trainData[row[i][1]][len(trainData[0]) - 1].strip('\n')
            nearestLabels.append([label, row[i][0]])
            i += 1
        finalLabelList.append(nearestLabels)

    print(finalLabelList)
    Classifications = []
    classLabel1 = finalLabelList[0][0][0]
    classLabel2 = ''
    for sample in finalLabelList:
        class1 = 0
        class2 = 0
        for label in sample:
            if label[0] != classLabel1:
                classLabel2 = label[0]
                class2 += (1 / (label[1] ** 2 + 1))
            else:
                class1 += (1 / (label[1] ** 2 + 1))
        if (class2 > class1):
            Classifications.append(classLabel2)
        else:
            Classifications.append(classLabel1)
    i = 0
    TruePos = 0
    TrueNeg = 0
    FalsePos = 0
    FalseNeg = 0
    for row in testData:
        if row[len(testData[0]) - 1].strip('\n') == classLabel1:
            if Classifications[i] == classLabel1:
                TruePos += 1
            else:
                FalseNeg += 1
        else:
            if Classifications[i] == classLabel2:
                TrueNeg += 1
            else:
                FalsePos += 1
        i += 1
    print("CLASS LABEL 1: " + classLabel1)
    print("CLASS LABEL 2: " + classLabel2)
    print("TRUE POS: " + str(TruePos))
    print("TRUE NEG: " + str(TrueNeg))
    print("FALSE NEG: " + str(FalseNeg))
    print("FALSE POS: " + str(FalsePos))


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

manotherList = []
canotherList = []
eanotherList = []
for rowTest in testData:
    mlistDist = []
    clistDist = []
    elistDist = []
    x = 0
    while x < len(trainData):
        i = 0
        mdist = 0
        cdist = 0
        edist = 0
        while i < len(trainData[0]) - 1:
            mdist += abs(float(rowTest[i]) - float(trainData[x][i]))
            if abs(float(rowTest[i]) - float(trainData[x][i])) > cdist:
                cdist = abs(float(rowTest[i]) - float(trainData[x][i]))
            edist += (float(rowTest[i]) - float(trainData[x][i]))**2
            i += 1
        elistDist.append([math.sqrt(edist), x])
        mlistDist.append([mdist, x])
        clistDist.append([cdist, x])
        x += 1
    elistDist.sort()
    mlistDist.sort()
    clistDist.sort()
    manotherList.append(mlistDist)
    canotherList.append(clistDist)
    eanotherList.append(elistDist)

doStuff(eanotherList, "EUCLIDEAN")
doStuff(manotherList, "MANHATTAN")
doStuff(canotherList, "CHEBYCHEV")


