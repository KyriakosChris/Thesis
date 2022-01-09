#pyPi libraries
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from keras.layers import CuDNNLSTM
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from tqdm import tqdm
from tensorflow.keras.optimizers import Adam
#This configures GPUs so that memory issues don't occur

class GAN:
  def __init__(self, batch_size, epochs):
    self.batch_size = batch_size
    self.epochs = epochs
    self.losses = []
    self.accuracies = []
    self.iteration_checkpoints = []

  def load_dataset(self):
    file = '/home/kyriakos/Desktop/Projects/Dataset/merged.npy'
    X = np.load(file, allow_pickle=True)
    X = np.reshape(X, (X.shape[0], X.shape[1],X.shape[2]*X.shape[3]))
    X = X/np.max(X)
    self.X = X
    file = '/home/kyriakos/Desktop/Projects/Dataset/y.npy'
    Y = np.load(file, allow_pickle=True)
    self.Y = Y

  def build_discriminator(self,img_shape):

    model = Sequential()

    # Flatten the input image
    model.add(Flatten(input_shape=img_shape))

    # Fully connected layer
    model.add(Dense(128))

    # Leaky ReLU activation
    model.add(LeakyReLU(alpha=0.01))

    # Output layer with sigmoid activation
    model.add(Dense(1, activation='sigmoid'))

    self.discriminator = model

  def build_generator(self,img_shape, z_dim):

    model = Sequential()

    # Fully connected layer
    model.add(Dense(128, input_dim=z_dim))

    # Leaky ReLU activation
    model.add(LeakyReLU(alpha=0.01))

    # Output layer with tanh activation
    model.add(Dense(3198 * 186 * 1, activation='tanh'))

    # Reshape the Generator output to image dimensions
    model.add(Reshape(img_shape))
    self.gen_size = z_dim
    self.generator = model

  def build_gan(self):

    model = Sequential()

    # Combined Generator -> Discriminator model
    model.add(self.generator)
    model.add(self.discriminator)

    self.gan = model
  
  def compile(self):
      # Build and compile the Discriminator
    self.discriminator.compile(loss='binary_crossentropy',
                          optimizer=Adam(),
                          metrics=['accuracy'])


    # Keep Discriminator’s parameters constant for Generator training
    self.discriminator.trainable = False

    self.gan.compile(loss='binary_crossentropy', optimizer=Adam())

  def train(self,iterations, sample_interval):

    # Load the MNIST dataset
    x_train,x_test,y_train,y_test = train_test_split(self.X,self.Y,test_size = 0.2)
    self.X= x_train
    self.X = np.expand_dims(self.X, axis=3)


    # Labels for real images: all ones
    real = np.ones((self.batch_size, 1))

    # Labels for fake images: all zeros
    fake = np.zeros((self.batch_size, 1))

    for iteration in tqdm(range(iterations)):

        # -------------------------
        #  Train the Discriminator
        # -------------------------

        # Get a random batch of real images

        idx = np.random.randint(0, self.X.shape[0], self.batch_size)
        imgs = self.X[idx]
        # Generate a batch of fake images
        z = np.random.normal(0, 1, (self.batch_size, self.gen_size))
        gen_imgs = self.generator.predict(z)

        # Train Discriminator
        d_loss_real = self.discriminator.train_on_batch(imgs, real)
        d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)
        d_loss, accuracy = 0.5 * np.add(d_loss_real, d_loss_fake)

        # ---------------------
        #  Train the Generator
        # ---------------------

        # Generate a batch of fake images
        z = np.random.normal(0, 1, (self.batch_size, self.gen_size))
        gen_imgs = self.generator.predict(z)

        # Train Generator
        g_loss = self.gan.train_on_batch(z, real)

        if (iteration + 1) % sample_interval == 0:

            # Save losses and accuracies so they can be plotted after training
            self.losses.append((d_loss, g_loss))
            self.accuracies.append(100.0 * accuracy)
            self.iteration_checkpoints.append(iteration + 1)

            # Output training progress
            print("%d [D loss: %f, acc.: %.2f%%] [G loss: %f]" %
                  (iteration + 1, d_loss, 100.0 * accuracy, g_loss))

    # Output a sample of generated image
  def sample_images(self,generator, image_grid_rows=4, image_grid_columns=4):

      # Sample random noise
      z = np.random.normal(0, 1, (image_grid_rows * image_grid_columns, self.gen_size))

      # Generate images from random noise
      gen_imgs = generator.predict(z)

      # Rescale image pixel values to [0, 1]
      gen_imgs = 0.5 * gen_imgs + 0.5
      self.gen = gen_imgs