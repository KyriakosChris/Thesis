import os
import glob
import ast
dirName = 'D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_FBX'

# importing the module

  

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
                
allFiles = getListOfFiles(dirName)

# reading the data from the file
with open('CMUclips.txt') as f:
    data = f.read()
  
      
# reconstructing the data as a dictionary
d = ast.literal_eval(data)
  
count = 0
total = 0
for file in allFiles:
    if file.split(".")[0].split("\\")[6] in d:
        count+=1
        total+=1
    else:
        total+=1
        #os.remove(file)

print(count)
print(total)