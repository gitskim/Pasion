import utils as utils
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras.optimizers import SGD
from sklearn.utils import shuffle
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.applications.vgg16 import VGG16
from keras.layers import LSTM
import numpy as np
import glob, os
from scipy.misc import imread, imresize
import tensorflow as tf

arr_frame_flat, arr_score, arr_difficulty = utils.get_pose_labels()

# (298387, 107)
input_dim = 107
timeseries = 202

model = Sequential()
model.add(LSTM(12, dropout=0.2, input_shape=(1, input_dim)))

model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
model.summary()

model.fit(arr_frame_flat, arr_score)

model.save_weights('sun-4-21-12p.h5')
