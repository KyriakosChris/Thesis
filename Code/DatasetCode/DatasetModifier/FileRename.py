import os
import glob
import ast
from Read_AllFiles import ReadFiles
dirName = 'D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_FBX'

# importing the module


                
allFiles = ReadFiles.getListOfFiles(None,dirName)

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