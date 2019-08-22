import pose_utils as utils
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras.optimizers import SGD
from sklearn.utils import shuffle
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.applications.vgg16 import VGG16
from keras.layers import LSTM, Bidirectional
import numpy as np
import glob, os
from scipy.misc import imread, imresize
import tensorflow as tf
import keras.backend as K
arr_frames, arr_score, arr_difficulty = utils.get_pose_labels2()
print(arr_frames.shape)

# (298387, 104)
timeseries = 202
input_dim = 104

def correlation_coefficient_loss(y_true, y_pred):
    print('----------suhyun cc loss --------')
    print(y_true[1], y_pred[1])
    x = y_true
    y = y_pred
    mx = K.mean(x)
    my = K.mean(y)
    xm, ym = x-mx, y-my
    r_num = K.sum(tf.multiply(xm,ym))
    r_den = K.sqrt(tf.multiply(K.sum(K.square(xm)), K.sum(K.square(ym))))
    r = r_num / r_den

    r = K.maximum(K.minimum(r, 1.0), -1.0)
    return 1 - K.square(r)


model = Sequential()
model.add(LSTM(512, dropout=0.2, input_shape=(timeseries, input_dim), return_sequences=True))
model.add(LSTM(128, dropout=0.2))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss='mse', metrics=['mse'])
model.summary()

history = model.fit(arr_frames, np.array(arr_score), epochs=300, validation_split=0.2, shuffle=True)
hist_df = pd.DataFrame(history.history)

with open('model2-mse.json', 'w') as f:
        hist_df.to_json(f)



model = Sequential()
model.add(LSTM(512, dropout=0.2, input_shape=(timeseries, input_dim), return_sequences=True))
model.add(LSTM(128, dropout=0.2))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss='mae', metrics=['mae'])
model.summary()

history = model.fit(arr_frames, np.array(arr_score), epochs=300, validation_split=0.2, shuffle=True)
hist_df = pd.DataFrame(history.history)

with open('model2-5-14-mae.json', 'w') as f:
        hist_df.to_json(f)


