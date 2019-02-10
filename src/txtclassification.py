#encoding=utf-8
from gensim.models import word2vec
import math
import operator

def knnMuInfo(): # classify by mutual information similarity
    commodities = []
    labels = []
    dfs = {} #{'0':0}
    coTable = {} #{('0','0'):0.0}
    i = open('C:/facts/titles.txt', 'r')
    lines = i.read().split('\n')
    for line in lines:
        labels.append(line.split('\t')[1])
        commodities.append(line.split('\t')[0].split(' '))
    i.close()
        
    for c in commodities:
        for x in c:
            if x in dfs.keys():
                dfs[x] += 1
            else:
                dfs[x] = 1
            for y in c:
                if (x,y) in coTable.keys():
                    coTable[(x,y)] += 1.0
                else:
                    coTable[(x,y)] = 1.0
                
    for k,v in coTable.items():
        d = v*len(commodities)/(dfs[k[0]]*dfs[k[1]]);
        coTable[k] = math.log(d)
        
    t = 1
    for g in coTable:
        print(g,coTable[g])
        t += 1
        if t > 10:
            break
    
    newcommodities = []
    newlabels = []
    ni = open('C:/facts/title-test.txt', 'r')
    lines = ni.read().split('\n')
    for line in lines:
        newlabels.append(line.split('\t')[1])
        newcommodities.append(line.split('\t')[0].split(' '))
    ni.close()
    for nc in newcommodities:
        miAvrList = {} #{'0':0.0} average mutual information with each known commodity
        knearestlabels = []
        for x in range(len(commodities)):
            c = commodities[x]
            ncmisum = 0.0
            for ns in nc:
                nsmisum = 0.0
                for s in c:
                    if coTable.__contains__((ns,s)):
                        nsmisum += coTable[(ns,s)]
                nsmi = nsmisum/(1+len(c))
                ncmisum += nsmi
            ncmi = ncmisum/(1+len(nc))
            miAvrList[x] = ncmi
        miAvrRank = sorted(miAvrList.items(), key=operator.itemgetter(1), reverse = True)
        for n in range(3): # k of KNN
            knearestlabels.append(labels[miAvrRank[n][0]])
        print(knearestlabels)
        
knnMuInfo()


"""
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

batch_size = 128
num_classes = 10
epochs = 12

# input image dimensions
img_rows, img_cols = 28, 28

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

"""