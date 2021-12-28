import sys
sys.path.append('./')
import ast
import numpy as np
import utils.BVH as BVH
from numpy import average
from utils.Quaternions import Quaternions
from utils import util
from tqdm import tqdm 
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
    
y = []
bvh_files = util.make_dataset(["/home/kyriakos/Desktop/Projects/Dataset/CMU_BVH"], phase='bvh', data_split=1, sort_index=0)
out = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_nmpy\\"
with open("/home/kyriakos/Desktop/Projects/Thesis/Code/DatasetCode/MotioNet-master/data/CMUclips.txt") as f:
    data = f.read()
cmuClips = ast.literal_eval(data)
for file in (bvh_files):
    #original_anim, name, frametime = BVH.load(file, rotate=True)
    #sampling = 1
    #to_keep = [0, 7, 8, 2, 3, 12, 13, 15, 18, 19, 25, 26]
    #real_rotations = original_anim.rotations.qs[1:, to_keep, :]
    #print(file)
    #print(cmuClips[file.split('.bvh')[0].split("/")[7]][1])
    y.append(Classification(cmuClips,file.split('.bvh')[0].split("/")[7]))
    #positions = original_anim.positions.astype('float32')
    #rotations = np.asarray(original_anim.rotations).astype('float32')
    #concat = np.concatenate((positions,rotations),axis=2)
    #concat = np.concatenate((name,concat),axis=1)
    #bvh.append(np.arange(0, concat.shape[0] // sampling) * sampling].astype('float32'))
    #path = out + file.split('.bvh')[0].split("\\")[6]
#res = []
#[res.append(x) for x in y if x not in res]
count = 0
for x in y:
    if(x=="No_Walking"):
        count=count+1
print(count)
    #np.savez_compressed(path, coordinates=concat)
y = np.array(y)
np.save("/home/kyriakos/Desktop/Projects/Dataset/y", y)
#print(average(y))
#print(y)
 