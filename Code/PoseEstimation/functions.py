from tkinter import *

from BVHsmoother.smooth import smooth
import numpy as np

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
