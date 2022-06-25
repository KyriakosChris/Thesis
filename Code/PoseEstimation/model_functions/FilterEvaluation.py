import numpy as np
import matplotlib.pyplot as plt
import os
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

# filterEvaluate("D:\\tuc\\Github\\Thesis\\BVH\\filter_test\\1_no_filter.bvh")
# filterEvaluate("D:\\tuc\\Github\\Thesis\\BVH\\filter_test\\1_mean_7.bvh")
# filterEvaluate("D:\\tuc\\Github\\Thesis\\BVH\\filter_test\\1_butterworth.bvh")
filterEvaluate("D:\\tuc\\Github\\Thesis\\BVH\\filter_test\\1_Gaussian_1000_3000.bvh")