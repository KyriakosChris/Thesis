import sys
sys.path.append('./')
import ast
import numpy as np
import utils.BVH as BVH
from numpy import average
from utils.Quaternions import Quaternions
from utils import util
from tqdm import tqdm 
from Read_AllFiles import ReadFiles
from numpy import load
def evalutation(dict,name):
    if dict[name][0]=='walk':
        return 1.0
    if 'walk' in dict[name][0].lower():
        return 1.0
    if 'run' in dict[name][0].lower():
        return 0.0
    if 'navigate' in dict[name][0].lower():
        return 0.0
    if 'jump' in dict[name][0].lower():
        return 0.0
    return 0.0


def Classification(dict,name):
    if dict[name][0]=='walk':
        return dict[name][1]
    if 'walk' in dict[name][0].lower():
        return dict[name][1]
    else :
        return 'No_Walking'
    
y_class = []
y = []
bvh = []
bvh_files = util.make_dataset(["/home/kyriakos/Desktop/Projects/Dataset/CMU_BVH"], phase='bvh', data_split=1, sort_index=0)
out = "/home/kyriakos/Desktop/Projects/Dataset/CMU_test/"
with open("/home/kyriakos/Desktop/Projects/Thesis/Code/DatasetCode/MotioNet-master/data/CMUclips.txt") as f:
    data = f.read()
cmuClips = ast.literal_eval(data)
for file in tqdm(bvh_files):
    count = count +1
    original_anim, name, frametime = BVH.load(file, rotate=True)
    sampling = 1
    #to_keep = [0, 7, 8, 2, 3, 12, 13, 15, 18, 19, 25, 26]
    #real_rotations = original_anim.rotations.qs[1:, to_keep, :]
    #print(file)
    #print(cmuClips[file.split('.bvh')[0].split("/")[7]][1])
    y_class.append(Classification(cmuClips,file.split('.bvh')[0].split("/")[7]))
    y.append(evalutation(cmuClips,file.split('.bvh')[0].split("/")[7]))
    #print(y)
    #print(y_class)
    positions = original_anim.positions.astype('float32')
    rotations = np.asarray(original_anim.rotations).astype('float32')
    concat = np.concatenate((positions,rotations),axis=2)
    #print(concat.shape)
    #concat = np.concatenate((name,concat),axis=1)
    bvh.append(concat)
    #path = out + file.split('.bvh')[0].split("/")[7]
    #np.savez_compressed(path, coordinates=concat)

shape = []
for file in (bvh):
    shape.append(file.shape[0])
m = max(shape)
print(m)

bvh_resized = []
for file in (bvh):
    bvh_resized.append(np.resize(file,(m,file.shape[1],file.shape[2])))

shape = []
for file in (bvh_resized):
    shape.append(file.shape[0])
bvh_resized = np.asarray(bvh_resized)
print(bvh_resized.shape)
y_class = np.array(y_class)
y= np.array(y)
np.save("/home/kyriakos/Desktop/Projects/Dataset/y_class", y_class)
np.save("/home/kyriakos/Desktop/Projects/Dataset/y", y)
np.save("/home/kyriakos/Desktop/Projects/Dataset/merged", bvh_resized)

 