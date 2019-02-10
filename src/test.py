#encoding=utf-8
from gensim.models import word2vec
import numpy as np
import math
import operator
#from keras.datasets import imdb
import numpy
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

batch_size = 4
num_classes = 4
epochs = 10

# input image dimensions
img_rows, img_cols = 16, 20
"""
# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print((x_train, y_train))
print((x_test, y_test))
"""
sentences=word2vec.Text8Corpus('C:/facts/titles-utf.txt')
model=word2vec.Word2Vec(sentences,min_count=1,size=20)
#print('Laneige',model['Laneige'])
commodities = []
labels = []
maxlen = 0 # =16
i = open('C:/facts/titles.txt', 'r')
lines = i.read().split('\n')
for line in lines:
    labels.append(line.split('\t')[1])
    comd = line.split('\t')[0].split(' ')
    commodities.append(comd)
    if len(comd) > maxlen:
        maxlen = len(comd)
        
matrixx = []
for cd in commodities:
    for j in range(maxlen):
        if j < len(cd):
            try:
                matrixx.append(model[cd[j]])
                #print(cd[j],model[cd[j]])
            except KeyError:
                matrixx.append([0.0 for t in range(20)])
                #print('padding',[0.0 for t in range(20)])
        else:
            matrixx.append([0.0 for t in range(20)])
            #print('padding',[0.0 for t in range(20)])

x_train = np.array(matrixx)
names = []
for q in range(len(labels)):
    if labels[q] not in names:
        names.append(labels[q])
        labels[q] = names.index(labels[q])
    else:
        labels[q] = names.index(labels[q])

y_train = np.array(labels)

print(x_train, y_train)
