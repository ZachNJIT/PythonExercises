# Zach Barnhart
# Hinge Loss

# WARNING: RUNTIME MAY BE SEVERAL SECONDS
# Format command line argument as hingeloss.py datafile.data datalabels.trainlabels.x
# If the training data has more than two classes, this program will not work

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
        rvec.insert(0, 1.0)
        if bias > 0:
            rvec.insert(0, bias)
        #print('row {} : {}'.format(i, rvec))
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
        #print('label : {}'.format(ldict))
        if hyperplaneclass and int(row[0]) <= 0:
            ldict[int(row[1])] = -1
        else:
            ldict[int(row[1])] = int(row[0])
    lfile.close()
    return ldict


def fillzeros(reference):
    matrix = [[0.01 for x in range(len(reference[0]))] for y in range(2)]
    return matrix


def whichclass(datapoint, weights):
    estcl = 0.0
    for i in range(len(datapoint)):
        estcl += datapoint[i] * weights[i]
    if abs(estcl - 1) < abs(estcl + 1):
        return 1
    else:
        return 0


def listprediction(reference, dicti, weights):
    prediction = {}
    for i in range(len(reference)):
        if i not in dicti:
            prediction[i] = whichclass(reference[i], weights)
    return prediction


def dotProduct(u, v):
    sum = 0
    for i in range(len(u)):
        sum += u[i] * v[i]
    return sum

def labelshift(dicti):
    for i in dicti:
        if dicti.get(i) == 0:
            dicti[i] = -1
    return dicti


eta = 0.001
stop = 0.001

if len(sys.argv) > 1:
    for i in range(len(sys.argv)):
        if sys.argv[i].endswith(".data"):
            inData = sys.argv[i]
            if i == 1:
                inLabels = sys.argv[2]
            elif i == 2:
                inLabels = sys.argv[1]
    data = getfeaturedata(inData, 0)
    lDict = labelshift(getlabeldata(inLabels, False))

    d = [0.0] * len(data)
    w = [0.0] * len(data[0])
    for i in range(len(data[0])):
        w[i] = random.uniform(-0.01, 0.01)
    error = 99999.0
    prevError = 100000.0
    dw = [0.0] * len(w)
    sum = 0.0
    while (abs(prevError - error) > stop):
        prevError = error
        error = 0.0
        for i in range(len(data)):
            if (lDict.get(i) == -1) or (lDict.get(i) == 1):
                d[i] = 1 - lDict.get(i)*(dotProduct(data[i], w))
                if d[i] < 0.0:
                    d[i] = 0.0
            error += d[i]
        for j in range(len(w)):
            sum = 0.0
            for i in range(len(d)):
                if lDict.get(i) is not None:
                    if lDict.get(i)*(dotProduct(data[i], w)) < 1:
                        sum += lDict.get(i)*data[i][j]
            dw[j] = eta * sum
        for i in range(len(w)):
            w[i] += dw[i]
        #print(error)

    dw = [0.0] * (len(w) - 1)
    for i in range(len(w) - 1):
        dw[i] = w[i + 1]

    print("Our vector w = [w₁, w₂] is given by")
    print("w = [" + str(dw[0]) + ", " + str(dw[1]) + "]")
    print("We have w[0] = " + str(w[0]))
    print("The distance from the plane to the origin is")
    print(abs(w[0]/math.sqrt(dotProduct(dw, dw))))
    predictionlist = listprediction(data, lDict, w)
    print("We predict the following classes for these datapoints:")
    for i in predictionlist:
        print(str(predictionlist.get(i)) + "\t" + str(i))
else:
    print("Improper format. Please format your command line argument as follows:")
    print("hingeloss.py datafile.data labelfile.traininglabels.x")