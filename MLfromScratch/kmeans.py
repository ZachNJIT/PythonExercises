# Zach Barnhart
# k-means clustering

# Format command line argument as kmeans.py datafile.data

import math
import sys
import random


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


def dotProduct(u, v):
    sum = 0
    for i in range(len(u)):
        sum += u[i] * v[i]
    return sum


def findmin(datapoint, testmeans):
    minarg = -1
    mindist = math.inf
    for i in range(len(testmeans)):
        diff = []
        for j in range(len(datapoint)):
            diff.append(datapoint[j] - testmeans[i][j])
        dist = dotProduct(diff, diff)
        if dist < mindist:
            mindist = dist
            minarg = i
    return minarg


def lossfunction(testdata, means, lDict):
    loss = 0
    for i in range(len(testdata)):
        diff = []
        for j in range(len(means[0])):
            diff.append(testdata[i][j] - means[lDict.get(i)][j])
        loss += dotProduct(diff, diff)
    return loss


def kmeansclustering(testdata, testk, teststop):
    means = []
    for i in range(testk):
        test = []
        for j in range(len(testdata[i])):
            test.append(0.0)
        means.append(test)
    init = random.sample(range(0, len(testdata)), testk)
    for i in range(testk):
        for j in range(len(testdata[0])):
            means[i][j] = testdata[init[i]][j]
    preverror = math.inf
    error = 9999999999999.0
    lDict = {}
    while abs(preverror - error) > teststop:
        preverror = error
        for i in range(len(testdata)):
            lDict.update({i: findmin(testdata[i], means)})
        sums = []
        count = []
        for i in range(len(means)):
            test = []
            for j in range(len(means[i])):
                test.append(0.0)
            sums.append(test)
            count.append(0.0)
        for i in range(len(testdata)):
            for j in range(len(testdata[i])):
                sums[lDict.get(i)][j] += testdata[i][j]
            count[lDict.get(i)] += 1.0
        for i in range(len(means)):
            for j in range(len(means[i])):
                means[i][j] = float(sums[i][j])/float(count[i])
        error = lossfunction(testdata, means, lDict)
    for i in range(len(testdata)):
        lDict.update({i: findmin(testdata[i], means)})
    return lDict


stop = 0.00000000000001

if len(sys.argv) > 2:
    for i in range(len(sys.argv)):
        if sys.argv[i].endswith(".data"):
            inData = sys.argv[i]
            if i == 1:
                k = int(sys.argv[2])
            elif i == 2:
                k = int(sys.argv[1])
    data = getfeaturedata(inData, 0)
    labels = kmeansclustering(data, k, stop)
    for i in labels:
        print(str(labels.get(i)) + "\t" + str(i))
elif len(sys.argv) == 2:
    inData = sys.argv[1]
    data = getfeaturedata(inData, 0)
    k = int(input("How many clusters? "))
    labels = kmeansclustering(data, k, stop)
    for i in labels:
        print(str(labels.get(i)) + "\t" + str(i))
else:
    print("Improper format. Please format your command line argument as follows:")
    print("kMeans.py datafile.data")