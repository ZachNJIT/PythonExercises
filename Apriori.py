# Zach Barnhart

import math
import itertools
import pandas as pd

datafile = input("Please type name of datafile: ")
dataframe = pd.read_csv(datafile)
data = dataframe.values

support = float(input("What is the minimum support desired for transactions? (Decimal less than 1) "))
confidence = float(input("What is the minimum confidence desired for association rules? (Decimal less than 1) "))
print()

def checklist(testlist, testdata):
    count = 0
    setsize = len(testlist)
    for i in range(nrows):
        sum = 0
        for j in testlist:
            sum = sum + testdata[i][j]
        if sum == setsize:
            count = count + 1
    return count

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

nrows = data.shape[0]
ncols = data.shape[1]
supportthresh = math.ceil(support*nrows)

frequent = []
supportarr = []
supportconfidence = []
associationrules = []
associationrulesnames = []

print("The database contains the following transactions:")
for i in range(len(data)):
    transaction = "Trasaction "
    transaction = transaction + str(i+1) + ": \t"
    countery = 0
    colnames = ""
    for j in range(len(data[i])):
        colname = ""
        if data[i][j] == 1:
            if countery == 0:
                countery = countery + 1
                for k in range(len(dataframe.columns[j])):
                    colname = colname + dataframe.columns[j][k]
            else:
                colname = colname + ", "
                for k in range(len(dataframe.columns[j])):
                    colname = colname + dataframe.columns[j][k]
        colnames = colnames + colname
    transaction = transaction + colnames
    print(transaction)

freq1 = []
supp1 = []
for j in range(ncols):
    ccount = 0
    for i in range(nrows):
        ccount = ccount + data[i][j]
    if ccount >= supportthresh:
        adder = [j]
        freq1.append(adder)
        supp1.append(ccount)
frequent.append(freq1)
supportarr.append(supp1)

for count in range(1, ncols):
    if len(frequent[count - 1]) == 0:
        break
    freqc = []
    suppc = []
    newrow = []
    for i in frequent[count - 1]:
        for j in frequent[0]:
            if j[0] not in i:
                newrow = i + j
                tempsupp = checklist(newrow, data)
                if tempsupp >= supportthresh:
                    newrow.sort()
                    if newrow not in freqc:
                        freqc.append(newrow)
                        suppc.append(tempsupp)
    if len(freqc) == 0:
        break
    else:
        frequent.append(freqc)
        supportarr.append(suppc)
    count = count + 1

for i in range(1, len(frequent)):
    for j in frequent[i]:
        for k in range(i):
            subsets = findsubsets(j, k+1)
            for s in subsets:
                conf = supportarr[i][frequent[i].index(j)] / supportarr[k][frequent[k].index(list(s))]
                if  conf >= confidence:
                    pred = [x for x in j if x not in s]
                    rule = [list(s), pred]
                    suppconf = [supportarr[i][frequent[i].index(j)] / nrows, conf]
                    associationrules.append(rule)
                    supportconfidence.append(suppconf)

for i in associationrules:
    secondlevel = []
    for j in i:
        thirdlevel = ""
        counter = 0
        for k in j:
            if counter == 0:
                colname = ""
                for i in range(len(dataframe.columns[k])):
                    colname = colname + dataframe.columns[k][i]
                thirdlevel = thirdlevel + colname
                counter = counter + 1
            else:
                colname = ""
                for i in range(len(dataframe.columns[k])):
                    colname = colname + dataframe.columns[k][i]
                thirdlevel = thirdlevel + ", " + colname
        secondlevel.append(thirdlevel)
    associationrulesnames.append(secondlevel)

max = 0
for i in range(len(associationrulesnames)):
    test = len(associationrulesnames[i][0]) + len(associationrulesnames[i][1])
    if test > max:
        max = test
max = max + 10


print()
print("We searched for association rules with minimum support " + str(support) + " and minimum confidence " + str(confidence))
print("We found the following association rules in the dataset: ")
for i in range(len(associationrulesnames)):
    left_aligned = str(associationrulesnames[i][0]) + " --> " + str(associationrulesnames[i][1])
    right_aligned = "Support: " + str(float("{0:.2f}".format(supportconfidence[i][0]*100.0))) +  "%  Confidence: " + str(float("{0:.2f}".format(supportconfidence[i][1]*100.0))) + " %"
    if max < 40:
        print("{: <40}".format(left_aligned) + right_aligned)
    elif 50 > max >= 40:
        print("{: <50}".format(left_aligned) + right_aligned)
    elif 60 > max >= 50:
        print("{: <60}".format(left_aligned) + right_aligned)
    elif 70 > max >= 60:
        print("{: <70}".format(left_aligned) + right_aligned)
    elif 80 > max >= 70:
        print("{: <80}".format(left_aligned) + right_aligned)
    elif 90 > max >= 80:
        print("{: <90}".format(left_aligned) + right_aligned)
    elif 100 > max >= 90:
        print("{: <100}".format(left_aligned) + right_aligned)
    elif 110 > max >= 100:
        print("{: <110}".format(left_aligned) + right_aligned)
    elif 120 > max >= 110:
        print("{: <120}".format(left_aligned) + right_aligned)
    elif 130 > max >= 120:
        print("{: <130}".format(left_aligned) + right_aligned)
    elif 140 > max >= 130:
        print("{: <140}".format(left_aligned) + right_aligned)
    elif 150 > max >= 140:
        print("{: <150}".format(left_aligned) + right_aligned)
    elif 160 > max >= 150:
        print("{: <160}".format(left_aligned) + right_aligned)
    elif 170 > max >= 160:
        print("{: <170}".format(left_aligned) + right_aligned)
    elif 180 > max >= 170:
        print("{: <180}".format(left_aligned) + right_aligned)
    elif 190 > max >= 180:
        print("{: <190}".format(left_aligned) + right_aligned)
    elif 200 > max >= 190:
        print("{: <200}".format(left_aligned) + right_aligned)
    elif max >= 200:
        print(left_aligned)
        print(right_aligned)