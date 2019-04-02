import matplotlib.pyplot as plt
import numpy as np
import os

# The code in this notebook should work identically between TF v1 and v2
import tensorflow as tf
import zipfile

from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16, MobileNet, MobileNetV2

from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras import regularizers, optimizers
import pandas as pd
import numpy as np

# TODO: fill the train dir
TRAIN_DIR = "/home/ek2993/train"

# TODO: fill the test dir
TEST_DIR = "/home/ek2993/michael"

traindf = pd.read_csv('./train.csv', header=0, encoding='unicode_escape')
testdf = pd.read_csv("./test.csv", header=0, encoding='unicode_escape')

print(traindf.head(3))
print(testdf.head(3))

traindf.columns = ['frame', 'score', 'difficulty']
testdf.columns = ['frame', 'score', 'difficulty']

print(traindf.head(3))
print(testdf.head(3))

print(traindf.tail(3))
print(testdf.tail(3))

traindf = traindf[:-1]
testdf = testdf[:-1]

print(traindf.tail(3))
print(testdf.tail(3))

# Images will be resized to(TARGET_SHAPE, TARGET_SHAPE) as they're read off disk.
TARGET_SHAPE = 224
BATCH_SIZE = 100
EPOCHS = 5

train_image_generator = ImageDataGenerator(rescale=1. / 255)
val_image_generator = ImageDataGenerator(rescale=1. / 255)

train_data_gen = train_image_generator.flow_from_directory(directory=TRAIN_DIR,
                                                           dataframe=traindf,
                                                           x_col="frame",
                                                           y_col="score",
                                                           shuffle=True,  # Best practice: shuffle the training data
                                                           target_size=(TARGET_SHAPE, TARGET_SHAPE),
                                                           class_mode='other')

val_data_gen = val_image_generator.flow_from_directory(directory=TEST_DIR,
                                                       dataframe=testdf,
                                                       x_col="frame",
                                                       y_col="score",
                                                       shuffle=True,  # Best practice: shuffle the training data
                                                       target_size=(TARGET_SHAPE, TARGET_SHAPE),
                                                       class_mode='other')

conv_base = MobileNet(weights=None, include_top=False, input_shape=(TARGET_SHAPE, TARGET_SHAPE, 3))

model = Sequential()
model.add(conv_base)
model.add(Flatten())
model.add(Dense(1, activation='linear'))

model.compile(
    optimizer=tf.train.AdamOptimizer(),
    loss='mse',
    metrics=['accuracy'])

history = model.fit_generator(
    train_data_gen,
    # steps_per_epoch=int(np.ceil(233 / float(BATCH_SIZE))),
    epochs=EPOCHS,
    validation_data=val_data_gen,
    # validation_steps=int(np.ceil(60 / float(BATCH_SIZE)))
)
