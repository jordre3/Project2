import math
from prettytable import PrettyTable


def makePredictions(anotherList, distMeasure, l1, l2):
    finalLabelList = []
    print("FOR " + distMeasure + " AND K = " + str(k) + ":")
    for row in anotherList:
        i = 0
        nearestLabels = []
        while i < k:
            label = trainData[row[i][1]][len(trainData[0]) - 1].strip('\n')
            nearestLabels.append([label, row[i][0]])
            i += 1
        finalLabelList.append(nearestLabels)

    Classifications = []
    classLabel1 = l1
    classLabel2 = l2
    for sample in finalLabelList:
        class1 = 0
        class2 = 0
        for label in sample:
            if label[0] != classLabel1:
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
    displayConfusionMatrix(classLabel1, classLabel2, TrueNeg, TruePos, FalseNeg, FalsePos)
    precision = TruePos / (TruePos + FalsePos)
    recall = TruePos / (TruePos + FalseNeg)
    f1 = (2 * TruePos) / ((2 * TruePos) + FalsePos + FalseNeg)
    precision2 = TrueNeg / (TrueNeg + FalseNeg)
    recall2 = TrueNeg / (TrueNeg + FalsePos)
    f12 = (2 * TrueNeg) / ((2 * TrueNeg) + FalseNeg + FalsePos)
    return precision, recall, f1, precision2, recall2, f12


def displayConfusionMatrix(label1, label2, trueNeg, truePos, falseNeg, falsePos):
    print("FOR LABEL: " + label1)
    table = PrettyTable()
    table.field_names = ["", "predicted", "yes", "no"]
    table.add_row(["actual", "yes", truePos, falseNeg])
    table.add_row(["", "no", falsePos, trueNeg])
    print(table)
    print("FOR LABEL: " + label2)
    table = PrettyTable()
    table.field_names = ["", "predicted", "yes", "no"]
    table.add_row(["actual", "yes", trueNeg, falsePos])
    table.add_row(["", "no", falseNeg, truePos])
    print(table)


def displayAccuracyMeasures(measure, list, label):
    print(measure + " for class " + label)
    table = PrettyTable()
    table.field_names = ["", "EUCLIDEAN", "CHEBYCHEB", "MANHATTAN", "COSINE SIMILARITY"]
    table.add_row(["k = 3", list[0][0], list[2][0], list[1][0], list[3][0]])
    table.add_row(["k = 5", list[0][1], list[2][1], list[1][1], list[3][1]])
    table.add_row(["k = 7", list[0][2], list[2][2], list[1][2], list[3][2]])
    table.add_row(["k = 9", list[0][3], list[2][3], list[1][3], list[3][3]])
    table.add_row(["k = 11", list[0][4], list[2][4], list[1][4], list[3][4]])
    print(table)


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

label1 = trainData[0][len(trainData[0]) - 1].strip('\n')
label2 = ''
i = 0
while label2 == '':
    if trainData[i][len(trainData[i]) - 1].strip('\n') != label1:
        label2 = trainData[i][len(trainData[i]) - 1].strip('\n')
    i += 1

k = 3
precisionList = [[], [], [], [], []]
recallList = [[], [], [], [], []]
f1List = [[], [], [], [], []]
precisionList2 = [[], [], [], [], []]
recallList2 = [[], [], [], [], []]
f1List2 = [[], [], [], [], []]
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

    precision, recall, f1, precision2, recall2, f12 = makePredictions(eanotherList, "EUCLIDEAN", label1, label2)
    precisionList[0].append(precision)
    recallList[0].append(recall)
    f1List[0].append(f1)
    precisionList2[0].append(precision2)
    recallList2[0].append(recall2)
    f1List2[0].append(f12)
    precision, recall, f1, precision2, recall2, f12 = makePredictions(manotherList, "MANHATTAN", label1, label2)
    precisionList[1].append(precision)
    recallList[1].append(recall)
    f1List[1].append(f1)
    precisionList2[1].append(precision2)
    recallList2[1].append(recall2)
    f1List2[1].append(f12)
    precision, recall, f1, precision2, recall2, f12 = makePredictions(canotherList, "CHEBYCHEV", label1, label2)
    precisionList[2].append(precision)
    recallList[2].append(recall)
    f1List[2].append(f1)
    precisionList2[2].append(precision2)
    recallList2[2].append(recall2)
    f1List2[2].append(f12)
    precision, recall, f1, precision2, recall2, f12 = makePredictions(csanotherList, "COSINE SIMILARITY", label1, label2)
    precisionList[3].append(precision)
    recallList[3].append(recall)
    f1List[3].append(f1)
    precisionList2[3].append(precision2)
    recallList2[3].append(recall2)
    f1List2[3].append(f12)
    k += 2

displayAccuracyMeasures("PRECISION", precisionList, label1)
displayAccuracyMeasures("RECALL", recallList, label1)
displayAccuracyMeasures("F1-MEASURE", f1List, label1)
displayAccuracyMeasures("PRECISION", precisionList2, label2)
displayAccuracyMeasures("RECALL", recallList2, label2)
displayAccuracyMeasures("F1-MEASURE", f1List2, label2)