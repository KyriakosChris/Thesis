import tensorflow as tf 
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense,MaxPooling1D,Softmax, LSTM, Dropout
from tensorflow.keras import utils
import numpy as np
import pickle
import glob
import pandas as pd
import numpy as np
from Read_AllFiles import ReadFiles
from numpy import load
from tqdm import tqdm

print('hi')

"""

path = ('D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_nmpy\\')
files=ReadFiles.getListOfFiles(None,path)
x  = []
y = []
seq = []
seq_len = 100
for file in tqdm(files):
    x.append(np.load(file))

    

###   (4320,150,13,2) ---->>>   (4320, 150, 26)

X= np.asarray(x)
X = np.reshape(X, (X.shape[0], X.shape[1],X.shape[2]*X.shape[3]))
X= X/np.max(X)
print(X.shape)

y = utils.to_categorical(y)

print(y.shape)

model = Sequential()
model.add(LSTM(256, input_shape = (X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(3, activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()
probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-biggeer.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose = 1, save_best_only=True, mode = 'min')
callbacks_list = [checkpoint]

model.fit(X, y, epochs = 30, batch_size=32, callbacks=callbacks_list)
"""