from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import os
import numpy as np
import subprocess



def convert_2_PNG(dataDir):
    counter = 0
    files = []
    for subdir in os.listdir(dataDir):
        for file in os.listdir(dataDir+subdir):
            if file.endswith(".tif"):
                 files.append(dataDir+subdir+'/'+file)

        if not files:
            raise Exception('No Image was found')
            
    print ('Files to process: ',len(files))
    for file in files:
        counter += 1
        subprocess.call(['gdal_translate -of PNG -b 2 -b 3 -b 4 ' + file +' '+ os.path.splitext(file)[0]+'.png'], shell=True)
        if counter % 500 == 0:
            print ('Files processed: ', counter) 

            
            
def split_Train_Test(dataDir):
    path = os.path.dirname(os.path.dirname(dataDir))
    shuffleFiles = "cd "+dataDir+" && for d in ./*/; do ( mkdir -p "+path+"/Test_Data/$d && cd $d && shuf -zen"+str(num)+" *.png | xargs -0 mv -t "+path+"/Test_Data/$d/ ); done"
    subprocess.call(shuffleFiles, shell=True)
    
dataDir = '/Sentinel2_Trainingdata/Full_Data/'
convert_2_PNG(dataDir)
split_Train_Test(dataDir)


img_height, img_width, channels = 64,64,3

train_data_dir = "/Sentinel2_Trainingdata/Train_Data/"
validation_data_dir = "/Sentinel2_Trainingdata/Test_Data/"
nb_train_samples = 1875 * 10
nb_validation_samples = 625 * 10
epochs = 50
batch_size = 16


height, width, channels
if K.image_data_format() == 'channels_first':
    input_shape = (channels, img_width, img_height)
else:
    input_shape = (img_width, img_height, channels)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(10))
model.add(Activation('sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)


test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)


