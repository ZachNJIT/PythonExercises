# Zach Barnhart
# Least Squares Loss with Adaptive Step Size

# WARNING: RUNTIME MAY BE SEVERAL SECONDS
# Format command line argument as least_squares_adaptive_eta.py datafile.data datalabels.trainlabels.x
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


#def pointerror(theta, datapoint, label):
#    return label - model(theta, datapoint)


#def model(theta, datapoint):
#    return dotProduct(datapoint, theta)


def modelerror(theta, tempdata, dict):
    errr = 0.0
    for i in range(len(tempdata)):
        if dict.get(i) is not None:
            errr += 0.5 * (dict.get(i) - dotProduct(theta, tempdata[i]))**2
    #print(errr)
    return errr


def gradDescent(theta, tempdata, dict, testeta):
    dtheta = [0.0] * len(theta)
    for j in range(len(theta)):
        sum = 0.0
        for i in range(len(tempdata)):
            if dict.get(i) is not None:
                sum += (dict.get(i) - dotProduct(theta, tempdata[i]))*tempdata[i][j]
        dtheta[j] = testeta * sum
    return dtheta


def labelshift(dicti):
    for i in dicti:
        if dicti.get(i) == 0:
            dicti[i] = -1
    return dicti


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

    w = [0.0] * len(data[0])
    for i in range(len(data[0])):
        w[i] = random.uniform(-0.01, 0.01)
    error = 99999.0
    prevError = 100000.0
    dw = [0.0] * len(w)
    while (prevError - error) > stop:
        prevError = error
        eta_list = [1, .1, .01, .001, .0001, .00001, .000001, .0000001, .00000001, .000000001, .0000000001,
                    .00000000001]
        bestobj = 1000000000000
        for k in range(0, len(eta_list), 1):
            eta = eta_list[k]
            dw = gradDescent(w, data, lDict, eta)
            for i in range(len(w)):
                w[i] += dw[i]
            obj = modelerror(w, data, lDict)
            if obj < bestobj:
                bestobj = obj
                best_eta = eta
            for i in range(len(w)):
                w[i] -= dw[i]

        #print(bestobj)
        #print(best_eta)
        error = bestobj
        eta = best_eta
        dw = gradDescent(w, data, lDict, eta)
        for i in range(len(w)):
            w[i] += dw[i]

    dw = [0.0] * (len(w) - 1)
    for i in range(len(w) - 1):
        dw[i] = w[i + 1]

    #print("Our vector w = [w₁, w₂] is given by")
    #print("w = [" + str(dw[0]) + ", " + str(dw[1]) + "]")
    #print("We have ||w|| = " + str(math.sqrt(dw[0]**2 + dw[1]**2)))
    #print("The distance from the plane to the origin is")
    #print(abs(w[0]/math.sqrt(dotProduct(dw, dw))))
    predictionlist = listprediction(data, lDict, w)
    #print("We predict the following classes for these datapoints:")
    for i in predictionlist:
        print(str(predictionlist.get(i)) + "\t" + str(i))
else:
    print("Improper format. Please format your command line argument as follows:")
    print("least_squares_adaptive_eta.py datafile.data labelfile.trainlabels.x")