# -*- coding: utf-8 -*-
"""stockmarketprediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1A_MxEhdN4NhLq8ecfTesmumMtc8dT5yo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data

import yfinance as yf
start = "2010-01-01"
end = "2023-01-01"
# Fetch AAPL stock data
krt = yf.Ticker("KRETTOSYS.BO")
df = krt.history(start=start, end=end)
# Display the first 20 rows
df.head(20)
df=df.reset_index()

df.head()

df.columns

df = df.drop(['Dividends','Stock Splits'],axis=1)
df.head()

df.head()

plt.plot(df['Date'],df['Close'])

ma100 = df.Close.rolling(100).mean()
print(ma100)

plt.figure(figsize=(12,6))
plt.plot(df['Date'],df['Close'])
plt.plot(df['Date'],ma100,'r')

ma200 = df.Close.rolling(200).mean()
print(ma200)

plt.figure(figsize=(12,6))
plt.plot(df['Date'],df['Close'])
plt.plot(df['Date'],ma100,'r')
plt.plot(df['Date'],ma200,'g')

df.shape

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])
print(data_training.shape)
print(data_testing.shape)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0,1))
data_training_array = scaler.fit_transform(data_training)

data_training_array.shape

x_train = []
y_train = []
for i in range(100,data_training_array.shape[0]):
  x_train.append(data_training_array[i-100:i])
  y_train.append(data_training_array[i,0])

x_train,y_train = np.array(x_train),np.array(y_train)

print(x_train)
print(y_train)

!pip install keras tensorflow

import keras
from keras.layers import Dense,Dropout,LSTM

from keras.models import Sequential

model = Sequential()

model.add(LSTM(units=50,activation='relu',return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(Dropout(0.2))
model.add(LSTM(units=60,activation='relu',return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(units=80,activation='relu',return_sequences=True))
model.add(Dropout(0.4))
model.add(LSTM(units=120,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units = 1))

model.summary()

model.compile(optimizer='adam',loss='mean_squared_error')
model.fit(x_train,y_train,epochs=50)

model.save('keras_models1.h5')

data_testing.head()

data_training.tail()

past_100_data = data_training.tail()
final_df = pd.concat([past_100_data, data_testing], ignore_index=True)

final_df.head

input_data = scaler.fit_transform(final_df)
input_data.shape

x_test = []
y_test = []
for i in range(100,input_data.shape[0]):
  x_test.append(input_data[i-100:i])
  y_test.append(input_data[i,0])

x_test,y_test =np.array(x_test),np.array(y_test)

print(x_test.shape)
print(y_test.shape)

y_predicted = model.predict(x_test)

y_predicted.shape

y_test

y_predicted

scaler.scale_

scale_factor= 1/scaler.scale_

y_predicted = y_predicted*scale_factor
y_test = y_test*scale_factor

plt.figure(figsize = (12,6))
plt.plot(y_test,'b',label='Original Price')
plt.plot(y_predicted,'r',label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()

