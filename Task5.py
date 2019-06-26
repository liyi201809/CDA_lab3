import csv
import math
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFECV
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from numpy import array
import numpy
from sklearn.model_selection import train_test_split
from loaddata import load_data
df = load_data('capture20110811.pcap.netflow.labeled')

# print(dataset.head())

# dataset_botnet = dataset[dataset['Label']=='Botnet']
# dataset_legitimate = dataset[dataset['Label']=='LEGITIMATE']
# dataset_legitimate = dataset_legitimate.head(dataset_botnet.size)
print(df.head())
dataset = df[['Durat', 'Packets']]
labels = df['Label']
translation_table = {
    'LEGITIMATE': 0,
    'Botnet': 1,
    'Background': 2
}
new_labels = []
for label in labels:
    new_labels.append(translation_table[label])
labels = new_labels

traindata, testdata, trainlabels, testlabels = train_test_split(dataset, labels, test_size = 0.2)
traindata = numpy.array(traindata)
trainlabels = numpy.array(trainlabels)
# traindata = traindata.astype(np.float64)
# trainlabels = trainlabels.astype(np.float64)
sm = SMOTE()
traindata, trainlabels = sm.fit_resample(traindata, trainlabels)
print('done with smote ')

classifier = LogisticRegression()
classifier.fit(traindata, trainlabels)
predictions = classifier.predict(testdata)

print(predictions)
error_matrix = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
for i in range(len(predictions)):
    error_matrix[int(labels[i])][int(predictions[i])]+=1
print(error_matrix)
# print(dataset_legitimate.size)
# print(dataset_botnet.size)
