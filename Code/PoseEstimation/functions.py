from tkinter import *

from BVHsmoother.smooth import smooth
import numpy as np
from bvh_skeleton import h36m_skeleton
from common.Bvh2Gif import *
def fastsmooth(filename):
    filter = 'butterworth'
    border = 100 
    u0 = 60
    order = 2
    median = None
    sigma = None
    smooth(filename,filename,filter,order,border,u0, median , sigma)
def PositionEdit(file,positions):

    data = open(file, 'r')
    Lines = data.readlines()
    motion = False
    Edited = []
    for line in Lines:

        if 'Frame Time:' in line:
            motion = True
            Edited.append(line)
            continue
        if motion :
            pos = line.split(" ")
            l = ''
            pos  = [float(i) for i in pos]

            for i in range(0,3): 
                pos[i] = pos[i]/positions[i]
            for n,i in enumerate(pos):
                if n == len(pos) -1:
                    l += str(i) + '\n'
                else:
                    l += str(i) + ' '
            Edited.append(l)
        else:
            Edited.append(line)
    try:
        geeky_file = open(file, 'wt')
        for line in Edited:
                geeky_file.write(str(line))
        geeky_file.close()
    except:
        print("Unable to write to file")
            

def new_animation(prediction, output):
    vis_3d_keypoints_sequence(keypoints_sequence=prediction,skeleton=h36m_skeleton.H36mSkeleton(),
    azimuth=np.array(45., dtype=np.float32),fps=60,output_file=output,b=False)


def motion(file):

    data = open(file, 'r')
    Lines = data.readlines()
    motion = False
    mocap = []
    for line in Lines:

        if 'Frame Time:' in line:
            motion = True
            continue
        if motion :
            pos = line.split(" ")
            pos  = np.array([float(i) for i in pos])
            pos = pos.reshape((17,3))
            mocap.append(pos)

    return np.array(mocap)        


#new_animation("D:\\tuc\\Github\\Thesis\\BVH\\kunkun_cut_one_second\\kunkun_cut_one_second.bvh","D:\\tuc\\Github\\Thesis\\BVH\\kunkun_cut_one_second\\3d_pose.mp4")