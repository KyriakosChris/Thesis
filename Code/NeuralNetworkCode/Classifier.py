#pyPi libraries
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import *
from tensorflow.keras import utils
from keras.optimizers import Adam
from numpy import load
import numpy as np
from numpy import argmax
from pandas import read_csv
from keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
#This configures GPUs so that memory issues don't occur

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
# Restrict TensorFlow to only allocate 1GB of memory on the first GPU
    try:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Virtual devices must be set before GPUs have been initialized
        raise e


path = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_clips_no_zip.npy"

X = load(path, allow_pickle=True)
print(X.shape)

#"""
y = []
nNeurons = 186
output_layers = 1
X_train,X_test,y_train,y_test = train_test_split(X,X,test_size = 0.2, random_state = 42)
# creating the NN model
model = Sequential()
model.add( LSTM( nNeurons, return_sequences = True, input_shape = (3198, 186) ) )
model.add( LSTM( nNeurons ) )
model.add( Dense( output_layers, activation = 'softmax' ) )
model.compile( loss = 'mse',  optimizer = 'adam', metrics = ['accuracy'] )
model.summary()

probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-biggeer.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose = 1, save_best_only=True, mode = 'min')
callbacks_list = [checkpoint]
model.save('cmuclassifier.model')

y_pred = model.predict(X_test)
#Converting predictions to label
pred = list()
for i in range(len(y_pred)):
    pred.append(np.argmax(y_pred[i]))
#Converting one hot encoded test label to label
test = list()
for i in range(len(y_test)):
    test.append(np.argmax(y_test[i]))


a = accuracy_score(pred,test)
print('Accuracy is:', a*100)

history = model.fit(X_train, y_train,validation_data = (X_test,y_test), epochs=100, batch_size=64)


plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(history.history['loss']) 
plt.plot(history.history['val_loss']) 
plt.title('Model loss') 
plt.ylabel('Loss') 
plt.xlabel('Epoch') 
plt.legend(['Train', 'Test'], loc='upper left') 
plt.show()

#"""