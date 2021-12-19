# reading the data from the file
import os
from tqdm import tqdm

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles
loc = 'D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_BVH'
list = getListOfFiles(loc)
for file in tqdm(list):
    data = open(file, 'r')
    Lines = data.readlines()
    Edited = []
    total = 0
    for n,line in enumerate(Lines) :
        if n == 1 or n == 2 or n == 3 or n == 4 or n == 188:
            continue
        if n== 5:
            line = "  ROOT Hips\n"
        if n<188 and n>1:
           line = line[2:]
        if n==190 :
            total = str(round(int(line[8:])/4))
            line = 'Frames: ' + total + '\n'
        if n>191 :
            line = line[13:]
            Edited.append(str(line))
        else:
        # print(line)
            Edited.append(str(line))
    try:
        out_path = "D:\\tuc\\exam10\\Thesis\\Dataset\\FIXED_CMU_BVH\\"
        bvh_path = out_path+file.split("\\")[6].split(".bvh")[0]+".bvh"
        geeky_file = open(bvh_path, 'wt')
        frame=0
        for n,line in enumerate(Edited):
            if n<187:
                geeky_file.write(str(line))
            if n>186 and round(frame/4) < int(total):
                if(frame%4==0):
                        geeky_file.write(str(line))
                frame+=1
        geeky_file.close()
    except:
        print("Unable to write to file")