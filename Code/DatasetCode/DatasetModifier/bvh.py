import numpy as np
import xlrd
from Read_AllFiles import ReadFiles
from numpy import load
from numpy import save
from numpy.lib.function_base import average
from tqdm import tqdm

class BvhNode:

    def __init__(self, value=[], parent=None):
        self.value = value
        self.children = []
        self.parent = parent
        if self.parent:
            self.parent.add_child(self)

    def select_from_excel():
       
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

        list_search = ["walk","run","navigate", "jog" ]
        count=0
        """
        for value in dict.copy().values():
            key = list(dict.keys())[list(dict.values()).index(value)]
            if any(i in value[0].lower() for i in list_search) or any(i in value[1].lower() for i in list_search) :
                count+=1
            else :
                dict.pop(key, None)
        """
        print(count)
        print(len(dict))
        loc = ("D:\\tuc\\exam10\\Thesis\Dataset\\cmu-mocap-master\\data")
        try:
            geeky_file = open('CMUclips.txt', 'wt')
            geeky_file.write(str(dict))
            geeky_file.close()
        
        except:
            print("Unable to write to file")

    def fix_root():
        loc = 'D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_BVH'
        list = ReadFiles.getListOfFiles(loc)
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

    def merge_npy_files():
        path = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_nmpy"
        out = "D:\\tuc\\exam10\\Thesis\\Dataset\\nmpy_Resized\\"
        files=ReadFiles.getListOfFiles(None,path)
        shape = []
        for file in tqdm(files):
            data = load(file, allow_pickle=True)
            shape.append(data[data.files[0]].shape[0])
        print(max(shape))
        print(min(shape))
        print(average(shape))
        m = max(shape)

        for file in tqdm(files):
            data = load(file, allow_pickle=False)
            d = data[data.files[0]]
            f= np.resize(d,(m,d.shape[1],d.shape[2]))
            name= out +file.split("\\")[6].split(".npz")[0]
            np.savez_compressed(name, f)


        path = "D:\\tuc\\exam10\\Thesis\\Dataset\\nmpy_Resized"

        files=ReadFiles.getListOfFiles(None,path)
        clips = []
        for file in tqdm(files):
            data = load(file, allow_pickle=True)
            clips.append(data[data.files[0]])

        name = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_clips"
        merged = np.asarray(clips)
        print(merged.shape)
        np.savez_compressed(name, merged)

    