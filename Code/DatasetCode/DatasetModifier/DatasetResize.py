import numpy as np
import pickle
import glob
from numpy.lib.function_base import average
import pandas as pd
from Read_AllFiles import ReadFiles
from numpy import load
from numpy import save
from tqdm import tqdm




path = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_nmpy"
out = "D:\\tuc\\exam10\\Thesis\\Dataset\\nmpy_Resized\\"
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
    data = load(file, allow_pickle=False)
    d = data[data.files[0]]
    f= np.resize(d,(m,d.shape[1],d.shape[2]))
    name= out +file.split("\\")[6].split(".npz")[0]
    np.savez_compressed(name, f)


path = "D:\\tuc\\exam10\\Thesis\\Dataset\\nmpy_Resized"

files=ReadFiles.getListOfFiles(None,path)
clips = []
for file in tqdm(files):
    data = load(file, allow_pickle=True)
    clips.append(data[data.files[0]])

name = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_clips"
merged = np.asarray(clips)
print(merged.shape)
np.savez_compressed(name, merged)