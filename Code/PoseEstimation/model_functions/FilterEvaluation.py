import numpy as np
import matplotlib.pyplot as plt
import os
import random
def filterEvaluate(file):

    data = open(file, 'r')
    Lines = data.readlines()
    motion = False
    T_pose = False
    avg= []
    basename = os.path.basename(file)
    
    video_name = basename[:basename.rfind('.')]
    for line in Lines:

        if 'Frame Time:' in line:
            motion = True
            T_pose = True
            continue
        if T_pose:
            T_pose = False
            continue
        if motion :
            pos = line.split(" ")
            pos  = [float(i) for i in pos]
            avg.append(np.average(pos))
    # plotting the points
    print(len(avg))
    # x-axis label
    plt.xlabel('Frames')
    # frequency label
    plt.ylabel('Average joint location and orientantion')
    # plot title
    plt.title('Gaussian Filter')
    plt.plot(range(0,len(avg)),avg)
    name = video_name + '.png'
    plt.savefig(name)   
    
         
    print(np.average(avg))
def AddNoise(file):

    data = open(file, 'r')
    Lines = data.readlines()
    motion = False
    Edited = []
    basename = os.path.basename(file)
    
    video_name = basename[:basename.rfind('.')]
    for line in Lines:

        if 'Frame Time:' in line:
            motion = True
            Edited.append(line)
            continue
        if motion :
            pos = line.split(" ")
            l = ''
            pos = pos[:-1]
            pos  = [float(i) for i in pos]
            count = 0
            for i in range(0,len(pos)): 

                pos[i] = pos[i] + random.uniform(-1, 1)
                count+=1
                
            for n,i in enumerate(pos):
                if n == len(pos) -1:
                    l += str(i) + '\n'
                else:
                    l += str(i) + ' '
            Edited.append(l)
        else:
            Edited.append(line)
    try:
        save_file = open(file, 'wt')
        for line in Edited:
                save_file.write(str(line))
        save_file.close()
    except:
        pass
 
# filterEvaluate("D:\\tuc\\Github\\Thesis\\BVH\\filter_test\\1_no_filter.bvh")
# filterEvaluate("D:\\tuc\\Github\\Thesis\\BVH\\filter_test\\1_mean_7.bvh")
# filterEvaluate("D:\\tuc\\Github\\Thesis\\BVH\\filter_test\\1_butterworth.bvh")
#filterEvaluate("D:\\tuc\\Github\\Thesis\\BVH\\filter_test\\1_Gaussian_1000_3000.bvh")

AddNoise("D:\\tuc\\Github\\Thesis\\BVH\\Mixamo\\original.bvh")