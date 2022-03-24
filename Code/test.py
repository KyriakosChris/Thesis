import os
if not os.getcwd().__contains__('PersonDetection'):
    os.chdir("PersonDetection")
os.getcwd()
from Model import *

videopath = 'demo/kunkun_cut_one_second.mp4'
model = Cocomodel()
#filename = None
results = compute(model,videopath)
#BVHedit(filename,results)