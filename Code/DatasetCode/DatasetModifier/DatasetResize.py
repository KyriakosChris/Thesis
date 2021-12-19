import numpy as np
import pickle
import glob
from numpy.lib.function_base import average
import pandas as pd
from Read_AllFiles import ReadFiles
from numpy import load
from tqdm import tqdm




path = "D:\\tuc\\exam10\\Thesis\\Dataset\\nmpy_Resized\\Sample"
files=ReadFiles.getListOfFiles(None,path)
shape = []
for file in tqdm(files):
    data = load(file, allow_pickle=True)
    shape.append(data[data.files[0]].shape[0])
print(max(shape))
print(min(shape))
print(average(shape))
m = max(shape)
for file in tqdm(files):
    data = load(file, allow_pickle=True)
    d = data[data.files[0]]
    data = data.reshape((data.shape[0], data.shape[1], 1))
    
    break