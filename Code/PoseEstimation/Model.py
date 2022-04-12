from tqdm import tqdm
import cv2
import numpy as np
import glob
import os


def Calculate_Height(file):
    data = open(file, 'r')
    Lines = data.readlines()
    height = 0
    found = False
    for n,line in enumerate(Lines) :

        if "RightKnee" in line or "RightAnkle" in line:
            found = True
        if found and "OFFSET" in line:
            found = False
            base = line.split(' ')

            base = float(base[-1])

            height+=abs(base)

        if "Motion" in line :
            break
    return height

def PositionsEdit(file,positions, scale):

    if scale:
        positions = positions / 20
    data = open(file, 'r')
    Lines = data.readlines()
    motion = False
    Edited = []
    counter = 0
    firstline = True
    for n,line in enumerate(Lines) :

        if ( line.__contains__('Frame Time:')):
            motion = True
            Edited.append(line)
            continue
        if motion :
            pos = line.split(" ")
            l = ''
            pos  = [float(i) for i in pos]
            # if firstline:
            #     firstline = False
            #     xyz = pos[0:3] + positions[0]
            #     y = pos[1]

            for i in range(0,3): 
                pos[i] = positions[counter][0][i]
                # if i ==1:
                #     pos[i] = y -pos[i]
                #     pos[i] *=2000
                #     pos[i] += y 
                # else :
                #     pos[i] *=2000

            counter +=1
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
        frame=0
        for line in Edited:
                geeky_file.write(str(line))
        geeky_file.close()
    except:
        print("Unable to write to file")

def videoPath(videopath,extension):
    basename = os.path.basename(videopath)
    video_name = basename[:basename.rfind('.')]
    new_dir_name = "D:\\tuc\\Github\\Thesis\\Code\\Output\\Videos"
    path = f'{new_dir_name}/{video_name}{extension}'
    return path


def printVideo(out,path,name):
    basename = os.path.basename(name)
    video_name = basename[:basename.rfind('.')]
    new_dir_name = "D:\\tuc\\Github\\Thesis\\Code\\Output\\Videos"
    out_path = f'{new_dir_name}/{video_name}.mp4'
    img_array = []
    files = []
    #path = "C:\\Users\\msi\\Desktop\\VideoTo3dPoseAndBvh\\outputs\\outputvideo\\alpha_pose_desert\\vis\\*.jpg"
    folder = path.split('*')[0]
    counter = 0
    for filename in tqdm(glob.glob(path)):
        name= str(folder + str(counter) + '.jpg')
        files.append(name)
        counter+=1
    for filename in tqdm(files):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    
    
    out = cv2.VideoWriter(out_path,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


#Calculate_Height("D:\\tuc\\Github\\Thesis\\BVH\\alpha_pose_kunkun_cut_one_second\\alpha_pose_kunkun_cut_one_second.bvh")