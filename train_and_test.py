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

# TODO: fill the train dir
TRAIN_DIR = "/home/ek2993/train"

# TODO: fill the test dir
TEST_DIR = "/home/ek2993/michael"

# Images will be resized to(TARGET_SHAPE, TARGET_SHAPE) as they're read off disk.
TARGET_SHAPE = 224
BATCH_SIZE = 5

train_image_generator = ImageDataGenerator(rescale=1. / 255)
val_image_generator = ImageDataGenerator(rescale=1. / 255)

train_data_gen = train_image_generator.flow_from_directory(directory=TRAIN_DIR,
                                                           dataframe=train_label_df,
                                                           shuffle=True,  # Best practice: shuffle the training data
                                                           target_size=(TARGET_SHAPE, TARGET_SHAPE),
                                                           class_mode='other')

val_data_gen = val_image_generator.flow_from_directory(directory=TEST_DIR,
                                                       dataframe=test_label_df,
                                                       shuffle=True,  # Best practice: shuffle the training data
                                                       target_size=(TARGET_SHAPE, TARGET_SHAPE),
                                                       class_mode='other')

conv_base = MobileNet(weights=None, include_top=False, input_shape=(224, 224, 3))

model = Sequential()
model.add(conv_base)
model.add(Flatten())
model.add(Dense(1, activation='linear'))

conv_base.trainable = False

model.compile(
    optimizer=tf.train.AdamOptimizer(),
    loss='mse',
    metrics=['accuracy'])

history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=int(np.ceil(233 / float(BATCH_SIZE))),
    epochs=EPOCHS,
    validation_data=val_data_gen,
    validation_steps=int(np.ceil(60 / float(BATCH_SIZE)))
)
