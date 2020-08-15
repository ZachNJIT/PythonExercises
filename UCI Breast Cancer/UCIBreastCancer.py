# Zach Barnhart
# UCI Breast Cancer Data
# How to clean data and train classifiers

import sys
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# This method takes the raw data file, separates at commas,
# changes malignant and benign classifications into 0 and 1
# respectively, and outputs an array of floats
def getfeaturedata(featurefile, bias=0):
    x = []
    dfile = open(featurefile, 'r')
    i = 0
    for line in dfile:
        row = line.split(",")
        row1 = []
        for item in row:
            if item == "M":
                row1.append(0)
            elif item == "B":
                row1.append(1)
            else:
                row1.append(item)
        rvec = [float(item) for item in row1]
        if bias > 0:
            rvec.insert(0, bias)
        x.append(rvec)
        i += 1
    dfile.close()
    return x

inData = sys.argv[1]
data = np.array(getfeaturedata(inData, 0))

# Must delete first row, because the ID numbers won't help classify
data1 = np.delete(data,0,1)

# New first row is labels, so get us make this our target vector
y = data1[:,0]

# This last array, after removing the column of labels, will be our main data array
X = np.delete(data1,0,1)

# After some exploratory analysis, it appears that there are not
# too many outliers in the data set, but to be safe we will scale
# data using Robust scaler to avoid oversensitivity to outliers
# and speed up model convergence. Also, we plan on using PCA to
# see if it improves Naive Bayes, so this will help that PCA
scaler = RobustScaler()
X_trans = scaler.fit_transform(X)

# First we will try Naive Bayes on the raw data
# Since the data is continuous and consists of physical
# measures of cell nuclei, it is reasonable to assume they
# are normally distributed, whence the Gaussian model
model = GaussianNB()
scoreNB = cross_val_score(model, X, y, cv=10, scoring='accuracy').mean()
print("The average accuracy in the cross-validation splits with Naive Bayes is " + str(scoreNB))

# Perhaps it is better to perform Naive Bayes with independant
# features (in fact, that is one of the assumptions of Naive Bayes)
# We can use PCA to get a set of independent features we can work with
# while reducing dimension of data. After some exploratory analysis,
# we found 5 components sufficient to account for almost all variance
# and produces slightly better results
pca = PCA(n_components=5)
pca.fit(X_trans)
X_PCA = pca.transform(X_trans)
scorePCA = cross_val_score(model, X_PCA, y, cv=10, scoring='accuracy').mean()
print("The average accuracy in the cross-validation splits with Naive Bayes, data scaling, and PCA is " + str(scorePCA))

# Now we make a SVM classifier. We will use the scaled
# data set to improve convergence rate of the model
classifier = SVC(kernel = 'linear')
scoreSVM = cross_val_score(classifier, X_trans, y, cv=10, scoring='accuracy').mean()
print("The average accuracy in the cross-validation splits with SVM classifier (with data scaling) is " + str(scoreSVM))

# Lastle a random forest classifier. We will not need
# data scaling with this classifier, since the splits
# in decision trees are unaffected by scaling
# We use entropy criterion for deciding on splits, but
# there would be little difference with gini criterion
RFclassifier = RandomForestClassifier(criterion = 'entropy')
scoreRF = cross_val_score(classifier, X, y, cv=10, scoring='accuracy').mean()
print("The average accuracy in the cross-validation splits with Random Forest classifier (with data scaling) is " + str(scoreRF))