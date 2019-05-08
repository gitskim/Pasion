import pose_utils as utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Flatten, Dense
from tensorflow.keras import applications
from tensorflow.keras.optimizers import SGD
from sklearn.utils import shuffle
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import LSTM
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

model.fit(arr_frames, np.array(arr_score), epochs=50, validation_split=0.15)

model.save_weights('wed-5-8-3p.h5')

