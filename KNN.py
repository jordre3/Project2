import sys
import math


def makePredictions(anotherList, distMeasure):
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

    #print(finalLabelList)
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
    displayData(classLabel1, classLabel2, TrueNeg, TruePos, FalseNeg, FalsePos)


def displayData(label1, label2, trueNeg, truePos, falseNeg, falsePos):
    print("CLASS LABEL 1: " + label1)
    print("CLASS LABEL 2: " + label2)
    print("TRUE POS: " + str(truePos))
    print("TRUE NEG: " + str(trueNeg))
    print("FALSE NEG: " + str(falseNeg))
    print("FALSE POS: " + str(falsePos))


trainFile = open("ALL_AML_SigGene.train.arff", 'r')
testFile = open("ALL_AML_SigGene.test.arff", 'r')

line = trainFile.readline()
while "@data" not in line:
    line = trainFile.readline()

trainData = []
dataLine = trainFile.readline()
while dataLine is not "":
    dataLine = dataLine.split(',')
    trainData.append(dataLine)
    dataLine = trainFile.readline()

line = testFile.readline()
while "@data" not in line:
    line = testFile.readline()

testData = []
dataLine = testFile.readline()
while dataLine is not "":
    dataLine = dataLine.split(',')
    testData.append(dataLine)
    dataLine = testFile.readline()

k = 3
while k <= 11:
    manotherList = []
    canotherList = []
    eanotherList = []
    csanotherList = []
    for rowTest in testData:
        mlistDist = []
        clistDist = []
        elistDist = []
        cslist = []
        x = 0
        while x < len(trainData):
            i = 0
            mdist = 0
            cdist = 0
            edist = 0
            dotProduct = 0
            testCos = 0
            trainCos = 0
            #cs = 0
            while i < len(trainData[0]) - 1:
                mdist += abs(float(rowTest[i]) - float(trainData[x][i]))
                if abs(float(rowTest[i]) - float(trainData[x][i])) > cdist:
                    cdist = abs(float(rowTest[i]) - float(trainData[x][i]))
                edist += (float(rowTest[i]) - float(trainData[x][i]))**2
                # dot product for computing cosine similarity
                dotProduct += (float(rowTest[i]) * float(trainData[x][i]))
                # the dot product will be divided by the product of these two variables to give cos sim
                testCos += float(rowTest[i]) ** 2
                trainCos += float(trainData[x][i]) ** 2
                i += 1
            elistDist.append([math.sqrt(edist), x])
            mlistDist.append([mdist, x])
            clistDist.append([cdist, x])
            #cosine similarity list
            cosSim = dotProduct/(math.sqrt(testCos)*math.sqrt(trainCos))
            cslist.append([cosSim,x])
            x += 1
        elistDist.sort()
        mlistDist.sort()
        clistDist.sort()
        cslist.sort()
        cslist.reverse()
        manotherList.append(mlistDist)
        canotherList.append(clistDist)
        eanotherList.append(elistDist)
        csanotherList.append(cslist)

    makePredictions(eanotherList, "EUCLIDEAN")
    makePredictions(manotherList, "MANHATTAN")
    makePredictions(canotherList, "CHEBYCHEV")
    makePredictions(csanotherList, "COSINE SIMILARITY")
    k += 2