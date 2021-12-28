#pyPi libraries
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import *
from keras.layers import CuDNNLSTM
import random
import numpy as np
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


file = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_clips_no_zip.npy"
X = np.load(file, allow_pickle=True)
X = np.reshape(X, (X.shape[0], X.shape[1],X.shape[2]*X.shape[3]))
X = X/np.max(X)

#"""
randomlist = []
for i in range(0,1073):
    n = float(random.randint(0,1))
    randomlist.append(n)
list = np.array(randomlist)
del randomlist
X_train,X_test,y_train,y_test = train_test_split(X,list,test_size = 0.2, random_state = 42)
del X
nNeurons = 186
output_layers = 1
# creating the NN model
model = Sequential()
model.add( CuDNNLSTM( nNeurons, return_sequences = True, input_shape = (3198, 186) ) )
model.add( Dropout(0.2))
model.add( CuDNNLSTM(3198 ,nNeurons ) )
model.add( Dropout(0.2))
model.add(Flatten())
model.add( Dense( output_layers, activation = 'softmax' ) )

opt = tf.keras.optimizers.Adam(learning_rate =1e-3, decay=1e-5)
model.compile( loss = 'sparse_categorical_crossentropy',  optimizer = opt, metrics = ['accuracy'] )
model.summary()

probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-biggeer.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose = 1, save_best_only=True, mode = 'min')
callbacks_list = [checkpoint]
probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-biggeer.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose = 1, save_best_only=True, mode = 'min')
callbacks_list = [checkpoint]

history = model.fit(X_train, y_train,validation_data = (X_test,y_test), epochs=100, batch_size=64)
#model.save('cmuclassifier.model')

y_pred = model.predict(X_test)

#Converting predictions to label





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