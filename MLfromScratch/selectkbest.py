import math
import sys
import numpy as np
from sklearn import svm


def getfeaturedata(featurefile, bias=0):
    x = []
    dfile = open(featurefile, 'r')
    i = 0
    for line in dfile:
        row = line.split()
        rvec = [float(item) for item in row]
        #rvec.insert(0, 1.0)
        if bias > 0:
            rvec.insert(0, bias)
        x.append(rvec)
        i += 1
    dfile.close()
    return x


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


inData = sys.argv[1]
inLabels = sys.argv[2]
data = np.array(getfeaturedata(inData, 0))
lDict = getlabeldata(inLabels, False)
labels = np.array(getfeaturedata(inLabels, 0))
labels2 = []
for i in range(len(labels)):
    if labels[i][0] == 0:
        labels2.append(-1)
    else:
        labels2.append(labels[i][0])
data2 = np.array(data)

from sklearn import feature_selection
featureselect = feature_selection.SelectKBest(feature_selection.chi2, k=400)
X_new = featureselect.fit_transform(data2, labels2)
cols = featureselect.get_support(indices=True)
featurecolumns = open('featurecolumns.txt', 'w')
print(cols, file = featurecolumns)
featurecolumns.close()

clf = svm.SVC(C = 999.0, gamma='auto')
clf.fit(data2, labels2)

mask = featureselect.get_support()
inTest = sys.argv[3]
testdata = np.array(getfeaturedata(inTest, 0))
newtestdata = testdata[:,mask]
predictions = clf.predict(newtestdata)
for i in range(len(predictions)):
    print(str(prediction[i]) + "\t" + str(i))