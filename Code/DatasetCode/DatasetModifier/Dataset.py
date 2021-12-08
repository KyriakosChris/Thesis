# reading the data from the file
import os

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
data = open('D:\\tuc\\exam10\\Thesis\\Dataset\\07_06.bvh', 'r')
Lines = data.readlines()
Edited = []
for n,line in enumerate(Lines) :
    if n == 1 or n == 2 or n == 3 or n == 4 or n == 188:
        continue
    if n<188 and n>1:
        line = line[2:]
    if n==190 :
        line = 'Frames: ' + str(round(int(line[8:])/4)) + '\n'
    if n>191 :
      line = line[13:]
      Edited.append(str(line))
    else:
       # print(line)
        Edited.append(str(line))
try:
    geeky_file = open('CMUclips.bvh', 'wt')
    for n,line in enumerate(Edited):
        if n<192:
            geeky_file.write(str(line))
        elif(n%4==0):
            geeky_file.write(str(line))
    geeky_file.close()

except:
    print("Unable to write to file")