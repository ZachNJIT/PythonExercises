# Zach Barnhart
# Naive Bayes Classifier

# Format command line argument as naivebayes.py datafile.data datalabels.trainlabels.x
# If the training data has more than two classes, this program will not work

import math
import sys

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


def findsums(reference, dicti):
    tempsums = fillzeros(reference)
    for i in range(len(reference)):
        if dicti.get(i) == 0:
            for y in range(len(tempsums[0])):
                tempsums[0][y] += reference[i][y]
        if dicti.get(i) == 1:
            for z in range(len(tempsums[1])):
                tempsums[1][z] += reference[i][z]
    return tempsums


def findcounts(reference, dicti):
    counters = [0 for x in range(len(reference[0]))]
    for i in range(len(reference)):
            if dicti.get(i) == 0:
                counters[0] += 1
            if dicti.get(i) == 1:
                counters[1] += 1
    return counters


def findmeans(reference, dicti):
    tempmeans = fillzeros(reference)
    tempcounts = findcounts(reference, dicti)
    tempsums = findsums(reference, dicti)
    for i in range(len(tempsums)):
        for j in range(len(tempsums[i])):
            if tempcounts[i] != 0:
                tempmeans[i][j] = tempsums[i][j] / float(tempcounts[i])
    return tempmeans


def finderr(reference, dicti):
    tempsums = fillzeros(reference)
    tempmeans = findmeans(reference, dicti)
    for i in range(len(reference)):
        if dicti.get(i) == 0:
            for y in range(len(tempsums[0])):
                tempsums[0][y] += (reference[i][y] - tempmeans[0][y])**2
        if dicti.get(i) == 1:
            for z in range(len(tempsums[1])):
                tempsums[1][z] += (reference[i][z] - tempmeans[1][z])**2
    return tempsums


def findsd(reference, dicti):
    temperr = finderr(reference, dicti)
    tempcounts = findcounts(reference, dicti)
    tempsd = fillzeros(reference)
    for i in range(len(temperr)):
        for j in range(len(temperr[i])):
            if tempcounts[i] != 0:
                tempsd[i][j] = math.sqrt(temperr[i][j] / float(tempcounts[i]))
    return tempsd


def whichclass(datapoint, means1, sd1):
    classtot = [0, 0]
    for i in range(len(datapoint)):
        if (sd1[0][i] != 0) and (sd[1][i] != 0):
            classtot[0] += ((datapoint[i] - means1[0][i]) / sd1[0][i])**2
            classtot[1] += ((datapoint[i] - means1[1][i]) / sd1[1][i])**2
    if classtot[0] < classtot[1]:
        return 0
    else:
        return 1

def listprediction(reference, dicti):
    prediction = {}
    means1 = findmeans(reference, dicti)
    sd1 = findsd(reference, dicti)
    for i in range(len(reference)):
        if i not in dicti:
            prediction[i] = whichclass(reference[i], means1, sd1)
    return prediction

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
    means = findmeans(data, lDict)
    sd = findsd(data, lDict)
    predictionlist = listprediction(data, lDict)
    for i in predictionlist:
        print(str(predictionlist.get(i)) + "\t" + str(i))
else:
    print("Improper format. Please format your command line argument as follows:")
    print("naivebayes.py datafile.data labelfile.traininglabels.x")


