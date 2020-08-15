# Zach Barnhart
# Random Projections

import math
import sys
import random
from sklearn import svm
from sklearn import model_selection
import numpy as np

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

def getbestC(train, labels):

    random.seed()
    allCs = [.001, .01, .1, 1, 10, 100]
    error = {}
    for j in range(0, len(allCs), 1):
        error[allCs[j]] = 0
    rowIDs = []
    for i in range(0, len(train), 1):
        rowIDs.append(i)
    nsplits = 10
    for x in range(0, nsplits, 1):
        #### Making a random train/validation split of ratio 90:10
        newtrain = []
        newlabels = []
        validation = []
        validationlabels = []

        random.shuffle(rowIDs)  # randomly reorder the row numbers
        # print(rowIDs)

        for i in range(0, int(.9 * len(rowIDs)), 1):
            newtrain.append(train[i])
            newlabels.append(labels[i])
        for i in range(int(.9 * len(rowIDs)), len(rowIDs), 1):
            validation.append(train[i])
            validationlabels.append(labels[i])

        #### Predict with SVM linear kernel for values of C={.001, .01, .1, 1, 10, 100} ###
        for j in range(0, len(allCs), 1):
            C = allCs[j]
            clf = svm.LinearSVC(C=C)
            clf.fit(newtrain, newlabels)
            prediction = clf.predict(validation)

            err = 0
            for i in range(0, len(prediction), 1):
                if (prediction[i] != validationlabels[i]):
                    err = err + 1

            err = err / len(validationlabels)
            error[C] += err
            # print("err=",err,"C=",C,"split=",x)

    bestC = 0
    minerror = 100
    keys = list(error.keys())
    for i in range(0, len(keys), 1):
        key = keys[i]
        error[key] = error[key] / nsplits
        if (error[key] < minerror):
            minerror = error[key]
            bestC = key

    # print(bestC,minerror)
    return [bestC, minerror]


def dotProduct(u, v):
    sum = 0
    for i in range(len(u)):
        sum += u[i] * v[i]
    return sum


def getrandomw(datafile):
    testw = []
    for j in range(len(datafile[0])):
        testw.append(random.uniform(-1, 1))
    return testw


def getw0(datafile, testw):
    minxw = dotProduct(datafile[0], testw)
    maxxw = dotProduct(datafile[0], testw)
    for i in range(len(datafile)):
        comp = dotProduct(datafile[i], testw)
        if comp < minxw:
            minxw = comp
        elif comp > maxxw:
            maxxw = comp
    w0test = random.uniform(minxw, maxxw)
    return w0test


def testerror(testdata, testpredict, testlabels, testall):
    count = 0
    missedpredict = 0
    for i in range(len(testdata)):
        if testlabels.get(i) is None:
            if testpredict[count] != testall.get(i):
                missedpredict += 1
            count += 1
    errortest = float(missedpredict) / float(len(testpredict))
    return errortest


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


if len(sys.argv) > 3:
    data = getfeaturedata(sys.argv[1], 0)
    lDict = getlabeldata(sys.argv[2], False)
    datatest = getfeaturedata(sys.argv[3], False)
    X = data
    X1 = datatest
    clabels = []
    for i in range(len(data)):
        if lDict.get(i) is not None:
            clabels.append(lDict.get(i))
    fixlabels = np.array(clabels).ravel()
    C = 10
    LEVEL = 10000
    Z = []
    Z1 = []
    for i in range(LEVEL):
        w = getrandomw(X)
        w0 = getw0(X, w)
        z = []
        for j in range(len(X)):
            sum = 0
            for k in range(len(X[j])):
                sum += X[j][k] * w[k]
            z.append(sum + w0)
        zappend = []
        for j in range(len(z)):
            zappend.append(int((1 + int(math.copysign(1, z[j]))) / 2))
        Z.append(zappend)
        z1 = []
        for j in range(len(X1)):
            sum = 0
            for k in range(len(X1[j])):
                sum += X1[j][k] * w[k]
            z1.append(sum + w0)
        z1append = []
        for j in range(len(z1)):
            z1append.append(int((1 + int(math.copysign(1, z1[j]))) / 2))
        Z1.append(z1append)

    Zt = list(zip(*Z))
    Z1t = list(zip(*Z1))
    bestCz = getbestC(Zt, fixlabels)
    model2 = svm.LinearSVC(max_iter=10000, C=bestCz[0])
    scoreNew = model_selection.cross_val_score(model2, Zt, fixlabels, cv=C)
    zpredictions = model2.fit(Zt, fixlabels).predict(Z1t)
    print("For k = " + str(LEVEL))
    print("We get the following predictions:")
    for i in range(len(zpredictions)):
        print(str(zpredictions[i]) + "\t" + str(i))
else:
    print("Improper format. Please format your command line argument as follows:")
    print("rnadomprojections.py datafile.data labelfile.trainlabels.0 testdata")