DataMining.py is a Python script that finds a number of classifier models (Naive Bayes, SVM, and Random Forest)
for the UCI Machine Learning Repository, available here:

http://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29

The script is executed with a single argument consisting of the dataset, as follows:

[file path to python.exe] DataMining.py wdbc.data

Where a path to DataMining.py and wdbc.data will need to be provided if not in the working directory, and
wdbc.data may be replaced with the file name of the dataset.

The data consist of 569 cases classified into 357 benign cases and 212 malignant cases, with 30 real-valued
input features. The features were computed from a digitized image of a fine needle aspirate (FNA) of a
breast mass, and they describe characteristics of the cell nuclei present in the image. Ten real-valued
features are computed for each cell nucleus: a) radius (mean of distances from center to points on the
perimeter), b) texture (standard deviation of gray-scale values), c) perimeter, d) area, e) smoothness
(local variation in radius lengths), f) compactness (perimeter2 / area - 1.0), g) concavity (severity of
concave portions of the contour), h) concave points (number of concave portions of the contour), i) symmetry,
and j) fractal dimension ("coastline approximation" - 1). The mean, standard error, and "worst" or largest
(mean of the three largest values) of these features were computed for each image, resulting in 30 features.
For instance, field 3 is Mean Radius, field 13 is Radius SE, field 23 is Worst Radius.

The script preprocesses the raw data file as downloaded from the source, so it cannot be used on other
datasets (as it eliminates features and encodes labels in a manner specific to the WDBC data set).