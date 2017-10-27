from __future__ import absolute_import, division, print_function
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import os
import numpy as np
import subprocess
from dask.array.image import imread
from sklearn.model_selection import train_test_split


def read_data_from_dir(dataDir,extension):
    """ Read a stack of images located in subdirectories into a dask array
        returning X (array of data) and y (array of labels)
    """
    X = np.concatenate([imread(dataDir+subdir+'/*.'+extension).compute() for subdir in os.listdir(dataDir)]) 

    filesdict = {}

    for subdir in sorted(os.listdir(dataDir)):
        files = next(os.walk(dataDir+subdir))[2]
        files = len([fi for fi in files if fi.endswith("."+extension)])
        filesdict.update({subdir:files})

    if sum(filesdict.values()) != X.shape[0]:
        
        raise ValueError('Images and Labels does not Match')

    else:
        y = np.zeros([X.shape[0],1], dtype=np.uint8)
        i = 0
        imagelist = []
        for category in list(filesdict.keys()):
            z = filesdict[category]
            y[sum(imagelist):sum(imagelist)+z] = i
            imagelist.append(z)
            i += 1   

    return X,y
        

def replace_missingvalues_bandmean(X):
    """ Read a numpy array and check for missing values (zeros) and 
        replace zeros with band mean
    """
    zeros = np.where(X[:,:,:] == 0)
    pic, row, column, band = zeros[0],zeros[1],zeros[2],zeros[3]
    bandmean = {}
    for i in sorted(np.unique(band)):
        bandmean.update({i:np.mean(X[:,:,:,i])})
        
    for i in range(0,len(zeros[0])):
        pic, row, column, band = zeros[0][i],zeros[1][i],zeros[2][i],zeros[3][i]
        mean = bandmean.get(band)
        X[pic,row,column,band] = mean
        
    return X


dataDir = 'Sentinel2_Trainingdata/Full_Data/'

X,y = read_data_from_dir(dataDir,'tif')
num_classes = 10
X = X.astype('float32')
X = X[:,:,:,:]
 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

X = None
y = None

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)



# dimensions of images
img_width, img_height = 64, 64


nb_train_samples = len(X_train)
nb_validation_samples = len(X_test)
epochs = 50
batch_size = 8


input_shape = (img_width, img_height, X_train.shape[3])

model = Sequential()
model.add(Conv2D(8, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(8, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(16, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(32))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(10))
model.add(Activation('sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


train_datagen = ImageDataGenerator(
    rotation_range=180,
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.5,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1. / 255)


train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)

validation_generator = test_datagen.flow(X_test, y_test, batch_size=batch_size)


model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)
