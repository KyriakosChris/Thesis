import numpy as np
import matplotlib.pyplot as plt
file = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_clips_no_zip.npy"
X = np.load(file, allow_pickle=True)
X = np.reshape(X, (X.shape[0], X.shape[1],X.shape[2]*X.shape[3]))
X = X/np.max(X)
X=np.abs(X)

from sklearn.model_selection import train_test_split
import numpy as np
file = "D:\\tuc\\exam10\\Thesis\\Dataset\\y.npy"
Y = np.load(file, allow_pickle=True)
X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size = 0.2, random_state = 42)

from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.layers import *
model = keras.Sequential() # fill the model
# Conv 1
model.add(Conv2D(32, kernel_size=(3, 3), strides =1, padding='same', activation=None, input_shape=(3198, 186, 1)))
# BatchNormalization 1
model.add(BatchNormalization())
model.add(keras.layers.Activation('relu'))

# Conv 2
model.add(Conv2D(32, kernel_size=(3, 3), strides =1, padding='same', activation=None, input_shape=(3198, 186, 1)))
# BatchNormalization 2
model.add(BatchNormalization())
model.add(keras.layers.Activation('relu'))

# Max Pool 2
model.add(MaxPooling2D((2, 2),padding='valid'))
# Dropout 1
model.add(Dropout(0.2))

# Conv 3
model.add(Conv2D(64, (3, 3), padding='same', activation=None, input_shape=(1599, 93, 32)))
# BatchNormalization 3
model.add(BatchNormalization())
model.add(keras.layers.Activation('relu'))

# Conv4
model.add(Conv2D(64, (3, 3), padding='same', activation=None, input_shape=(1599, 93, 64)))
# BatchNormalization 4
model.add(BatchNormalization())
model.add(keras.layers.Activation('relu'))

# Max Pool 2
model.add(MaxPooling2D((2, 2),padding='valid'))
# Dropout 2
model.add(Dropout(0.3))

# Flatten Layer
model.add(keras.layers.Flatten())
# BatchNormalization 6
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Activation('softmax'))
# Dropout 4
model.add(keras.layers.Dropout(0.5))
# Dense 2
model.add(keras.layers.Dense(1))

model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


h = model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test))


plt.plot(h.history['accuracy'], label='accuracy')
plt.plot(h.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')
plt.show()