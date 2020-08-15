# Zach Barnhart
# Logistic Regression

# WARNING: RUNTIME MAY BE SEVERAL SECONDS
# Format command line argument as logistic.py datafile.data datalabels.trainlabels.x
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


def whichclass(datapoint, weights):
    estcl = dotProduct(datapoint, weights)
    if abs(estcl - 1) < abs(estcl):
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


def model(theta, datapoint):
    z = dotProduct(datapoint, theta)
    z = 1 + math.exp(-z)
    z = 1 / z
    return z


def modelerror(theta, tempdata, dict):
    errr = 0.0
    for i in range(len(tempdata)):
        if (dict.get(i) == 0) or (dict.get(i) == 1):
            y = dict.get(i)
            pred = model(theta, tempdata[i])
            if abs(pred - 1.0) < 0.00000001:
                pred = 0.99999999999999
            if abs(pred) < 0.00000001:
                pred = 0.0000000000001
            errr += (-1)*y*math.log(pred) - (1-y)*math.log(1 - pred)
    return errr


def gradDescent(theta, tempdata, dict, testeta):
    dtheta = [0.0] * len(theta)
    for j in range(len(theta)):
        sum = 0.0
        for i in range(len(tempdata)):
            if (dict.get(i) == 0) or (dict.get(i) == 1):
                sum += (dict.get(i)-model(theta, data[i])) * data[i][j]
        dtheta[j] = testeta * sum
    return dtheta


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
    lDict = getlabeldata(inLabels, False)

    w = [0.0] * len(data[0])
    for i in range(len(data[0])):
        w[i] = random.uniform(-0.01, 0.01)
    error = 99999.0
    prevError = 100000.0
    dw = [0.0] * len(w)
    while abs(prevError - error) > stop:
        prevError = error
        error = modelerror(w, data, lDict)
        dw = gradDescent(w, data, lDict, eta)
        for i in range(len(w)):
            w[i] += dw[i]

    dw = [0.0] * (len(w) - 1)
    for i in range(len(w) - 1):
        dw[i] = w[i + 1]

    print("Our vector w = [w₁, w₂] is given by")
    print("w = [" + str(dw[0]) + ", " + str(dw[1]) + "]")
    print("We have ||w|| = " + str(math.sqrt(dw[0]**2 + dw[1]**2)))
    print("The distance from the plane to the origin is")
    print(abs(w[0]/math.sqrt(dotProduct(dw, dw))))
    predictionlist = listprediction(data, lDict, w)
    print("We predict the following classes for these datapoints:")
    for i in predictionlist:
        print(str(predictionlist.get(i)) + "\t" + str(i))
else:
    print("Improper format. Please format your command line argument as follows:")
    print("logistic.py datafile.data labelfile.trainlabels.x")