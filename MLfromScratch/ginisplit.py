# Zach Barnhart
# GINI split

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
        if dict.get(i) is not None:
            rows += 1.0
            if testdata[i][column] < split:
                lsize += 1.0
                if dict.get(i) == 1:
                    lp += 1.0
            else:
                rsize += 1.0
                if dict.get(i) == 1:
                    rp += 1.0
    if abs(lsize) < 0.1:
        gini = (rsize / (rows)) * (rp / rsize) * (1.0 - rp / rsize)
    elif abs(rsize) < 0.1:
        gini = (lsize/(rows))*(lp/lsize)*(1.0 - lp/lsize)
    else:
        gini = (lsize/(rows))*(lp/lsize)*(1.0 - lp/lsize) + (rsize/(rows))*(rp/rsize)*(1.0 - rp/rsize)
    #print(gini)
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
    #print("minsplit: " + str(minsplit[0]))
    return minsplit


def bestcolumn(testdata, dict):
    bestcolumngini = math.inf
    bestcolumn = -1
    optimal = [bestcolumngini, bestcolumn, bestsplit]
    for j in range(0, len(testdata[0])):
        testsplit = bestsplit(testdata, j, dict)
        #print("testsplit: " + str(testsplit[0]))
        if testsplit[0] < optimal[0]:
            optimal[0] = testsplit[0]
            optimal[1] = j
            optimal[2] = testsplit[1]
    return optimal


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

    optimalsplit = bestcolumn(data, lDict)

    print("PRELIMINARY EXPLANATION")
    print("We define a split as a value s of a certain feature that partitions data points with the rules:")
    print("xᵢ < s implies xᵢ --> left partition")
    print("xᵢ ≥ s implies xᵢ --> right partition")
    print("")
    print("In the data set contained in the file " + str(inData) + " with labels " + str(inLabels))
    print("The best gini split is in column " + str(optimalsplit[1]) + ", s = " + str(optimalsplit[2]))
    print("The gini value for this split is " + str(optimalsplit[0]))
else:
    print("Improper format. Please format your command line argument as follows:")
    print("ginisplit.py datafile.data labelfile.trainlabels.x")