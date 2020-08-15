# Zach Barnhart
# Bagging

import math
import sys
import random

#Get feature data from file as a matrix with a row per data instance
def getfeaturedata(featurefile, bias=0):
    x = []
    dfile = open(featurefile, 'r')
    i = 0
    for line in dfile:
        row = line.split()
        rvec = [float(item) for item in row]
        if bias > 0:
            rvec.insert(0, bias)
        x.append(rvec)
        i += 1
    dfile.close()
    return x


#Get label data from file as a dictionary with key as data instance index and value as the class index
def getlabeldata(labelfile, hyperplaneclass=False):
    lfile = open(labelfile, 'r')
    ldict = {}
    for line in lfile:
        row = line.split()
        if hyperplaneclass and int(row[0]) <= 0:
            ldict[int(row[1])] = -1
        else:
            ldict[int(row[1])] = int(row[0])
    lfile.close()
    return ldict


def GINI(split, testdata, column, dict):
    rows = 0.0
    gini = 0.0
    lsize = 0.0
    rsize = 0.0
    lp = 0.0
    rp = 0.0
    for i in range(len(testdata)):
        key = dict.get(i)
        if key is not None:
            rows += 1.0
            compar = (key == 1)
            if testdata[i][column] < split:
                lsize += 1.0
                if compar:
                    lp += 1.0
            else:
                rsize += 1.0
                if compar:
                    rp += 1.0
    if abs(lsize) < 0.1:
        gini = (rsize / (rows)) * (rp / rsize) * (1.0 - rp / rsize)
    elif abs(rsize) < 0.1:
        gini = (lsize/(rows))*(lp/lsize)*(1.0 - lp/lsize)
    else:
        gini = (lsize/(rows))*(lp/lsize)*(1.0 - lp/lsize) + (rsize/(rows))*(rp/rsize)*(1.0 - rp/rsize)
    return gini


def bestsplit(testdata, column, dict):
    bestsplitgini = math.inf
    bestsplit = -1
    for i in range(len(testdata)):
        split = testdata[i][column]
        testgini = GINI(split, testdata, column, dict)
        if testgini < bestsplitgini:
            bestsplitgini = testgini
            bestsplit = testdata[i][column]
    minsplit = [bestsplitgini, bestsplit]
    return minsplit


def bestcolumn(testdata, dict):
    bestcolumngini = math.inf
    bestcolumn = -1
    optimal = [bestcolumngini, bestcolumn, bestsplit]
    for j in range(0, len(testdata[0])):
        testsplit = bestsplit(testdata, j, dict)
        if testsplit[0] < optimal[0]:
            optimal[0] = testsplit[0]
            optimal[1] = j
            optimal[2] = testsplit[1]
    return optimal


def iterlabels(data1, testdata, dict, optsplit):
    leftpred, leftzero, leftsize, rightpred, rightsize, rightzero = 0, 0, 0.00000000000001, 0, 0.0000000000001, 0
    labels = {}
    for i in range(len(testdata)):
        if testdata[i][optsplit[1]] < optsplit[2]:
            leftsize += 1.0
            if dict.get(i) == 0:
                leftzero += 1
        else:
            rightsize += 1.0
            if dict.get(i) == 0:
                rightzero += 1
    leftratio = leftzero / leftsize
    rightratio = rightzero / rightsize
    if leftratio < rightratio:
        leftpred = 1
    else:
        rightpred = 1
    for i in range(len(data1)):
        if dict.get(i) is None:
            if data1[i][optsplit[1]] < optsplit[2]:
                labels[i] = leftpred
            else:
                labels[i] = rightpred
    return labels


if len(sys.argv) > 1:
    for i in range(len(sys.argv)):
        if sys.argv[i].endswith(".data"):
            inData = sys.argv[i]
            if i == 1:
                inLabels = sys.argv[2]
            elif i == 2:
                inLabels = sys.argv[1]
    data = getfeaturedata(inData, 0)
    lDict = getlabeldata(inLabels, False)

    TRIALS = 100
    SAMPLESIZE = 100
    predlabels = {}
    for i in range(len(data)):
        if lDict.get(i) is None:
            predlabels[i] = 0
    for i in range(TRIALS):
        newdata = []
        for j in range(SAMPLESIZE):
            point = random.randint(0, len(data))
            if lDict.get(point) is not None:
                newdata.append(data[point])
        optimalsplit = bestcolumn(newdata, lDict)
        labelz = iterlabels(data, newdata, lDict, optimalsplit)
        for j in range(len(data)):
            if lDict.get(j) is None:
                if labelz.get(j) == 1:
                    predlabels[j] = predlabels.get(j) + 1
    print("Label Predictions: ")
    for i in range(len(data)):
        if lDict.get(i) is None:
            if predlabels.get(i) > TRIALS / 2:
                print("1 \t " + str(i))
            else:
                print("0 \t " + str(i))
else:
    print("Improper format. Please format your command line argument as follows:")
    print("bagging.py datafile.data labelfile.trainlabels.x")