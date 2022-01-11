from Model import * 
#from keras import backend as K


gan = GAN(batch_size=128,epochs=100)
gan.load_dataset()
print(gan.X.shape)
#image = (gan.X.shape[1], gan.X.shape[2])
gan.build_generator(z_dim=100)
gan.build_discriminator()
gan.build_gan()
gan.compile()
gan.train(iterations=10,sample_interval=1)