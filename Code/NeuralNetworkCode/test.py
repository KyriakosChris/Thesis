from Model import * 
#from keras import backend as K


gan = GAN(batch_size=128,epochs=100)
gan.load_dataset()
image = (gan.X.shape[1], gan.X.shape[2])
gan.build_generator(image,z_dim=100)
gan.build_discriminator(image)
gan.build_gan()
gan.compile()
gan.train(iterations=10,sample_interval=1)