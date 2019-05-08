import pose_utils as utils
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

arr_frames, arr_score, arr_difficulty = utils.get_pose_labels2()
print(arr_frames.shape)

# (298387, 104)
timeseries = 202
input_dim = 104

model = Sequential()
model.add(LSTM(12, dropout=0.2, input_shape=(timeseries, input_dim)))

model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss='mse', metrics=['mse','mae'])
model.summary()

model.fit(np.array(arr_frame_flat), np.array(arr_score), epochs=50)

model.save_weights('sun-4-21-12p.h5')

