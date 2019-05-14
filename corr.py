import pose_utils as utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Flatten, Dense
from tensorflow.keras import applications
from tensorflow.keras.optimizers import SGD
from sklearn.utils import shuffle
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import LSTM, Bidirectional
import numpy as np
import glob, os
from scipy.misc import imread, imresize
import tensorflow as tf
import pickle
import pandas as pd
import tensorflow.keras.backend as K

arr_frames, arr_score, arr_difficulty = utils.get_pose_labels2()
print(arr_frames.shape)
arr_frames = arr_frames.astype('float32')

# (298387, 104)
timeseries = 202
input_dim = 104

optimizer = tf.keras.optimizers.Adam()
loss_metric = tf.keras.metrics.Mean()

def correlation_coefficient_loss(y_true, y_pred):
    #print(f'suhyun true: {y_true.type}, pred: {y_pred.type}')
    x = tf.convert_to_tensor(y_true, dtype=tf.float32)
    y = y_pred

    mx = K.mean(x)
    my = K.mean(y)
    xm, ym = x-mx, y-my
    r_num = K.sum(tf.multiply(xm,ym))
    r_den = K.sqrt(tf.multiply(K.sum(K.square(xm)), K.sum(K.square(ym))))
    r = r_num / r_den

    r = K.maximum(K.minimum(r, 1.0), -1.0)
    r = K.print_tensor(r, message='suhyun --- corr rank r = ')
    return 1 - K.square(r)


model = Sequential()
model.add(LSTM(512, dropout=0.2, input_shape=(timeseries, input_dim)))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss=correlation_coefficient_loss, metrics=[correlation_coefficient_loss])
model.summary()
history = model.fit(arr_frames, np.array(arr_score), epochs=300, validation_split=0.2, shuffle=True)


model = Sequential()
model.add(Bidirectional(LSTM(512, dropout=0.2, return_sequences=True), input_shape=(timeseries, input_dim)))
model.add(Bidirectional(LSTM(128, dropout=0.2)))
model.add(Dense(1))
model.compile(optimizer='adam', loss=correlation_coefficient_loss, metrics=[correlation_coefficient_loss])
model.summary()

for epoch in range(300):
    print('Start of epoch %d' % (epoch,))

    # Iterate over the batches of the dataset.
    # for step, x_batch_train in enumerate(train_dataset):
    with tf.GradientTape() as tape:
        print('inside gradient tape')
        print('arr_frames shape:')
        np.random.shuffle(arr_frames)
        print(arr_frames.shape)
        reconstructed = model(arr_frames)

        #print(f'reconstruct: {reconstructed}')
        # Compute reconstruction loss
        loss = correlation_coefficient_loss(np.array(arr_score, dtype=np.float32), reconstructed)
        # print(f'y: {y.type}, reconstructed: {reconstructed.type}')
        loss += sum(model.losses)  # Add KLD regularization loss

    grads = tape.gradient(loss, model.trainable_weights)
    optimizer.apply_gradients(zip(grads, model.trainable_weights))

    result = loss_metric(loss)

    # if step % 100 == 0:
    # print('step %s: mean loss = %s' % (step, loss_metric.result()))
    # run the graph

    print('mean loss = %s' % (loss_metric.result()))
