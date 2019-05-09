* mae-wed-5-8-9p.h5
127/127 [==============================] - 0s 1ms/sample - loss: 36.7620 - mse: 1588.8616 - mae: 36.7620 - val_loss: 39.8813 - val_mse: 1748.8850 - val_mae: 39.8813

* mae-wed-5-8-9-16p.h5

127/127 [==============================] - 0s 1ms/sample - loss: 18.5622 - mse: 435.4550 - mae: 18.5622 - val_loss: 17.3463 - val_mse: 413.0093 - val_mae: 17.3463

* mae-wed-5-9-12p-mse.h5
```c
model = Sequential()
model.add(LSTM(512, input_shape=(timeseries, input_dim)))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='adam', loss='mse', metrics=['mse','mae'])
model.summary()
```
Epoch 200/200
127/127 [==============================] - 0s 3ms/sample - loss: 285.6193 - mse: 285.6193 - mae: 12.9231 - val_loss: 173.7013 - val_mse: 173.7013 - val_mae: 10.7447
