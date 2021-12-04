
import glob
import os
import pandas as pd
import xlrd

loc = ("D:\\tuc\\exam10\\Thesis\Dataset\\cmu-mocap-master\\cmu-mocap-index-spreadsheet.xls")
dict = {}
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
 
for i in range(12,sheet.nrows):
    l = []
    l.append(str(sheet.cell_value(i, 1)))
    l.append(str(sheet.cell_value(i, 2)))
    v = {sheet.cell_value(i, 0): l}
    dict.update(v)

list_search = ["walk","run","navigate", "jog", ]
count=0

for value in dict.copy().values():
    key = list(dict.keys())[list(dict.values()).index(value)]
    if any(i in value[0].lower() for i in list_search) or any(i in value[1].lower() for i in list_search) :
        count+=1
    else :
        dict.pop(key, None)

print(count)
print(len(dict))

try:
    geeky_file = open('CMUclips.txt', 'wt')
    geeky_file.write(str(dict))
    geeky_file.close()
  
except:
    print("Unable to write to file")