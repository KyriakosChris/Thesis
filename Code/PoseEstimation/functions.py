from tkinter import *
from tkinter import ttk
from BVHsmoother.smooth import smooth
import numpy as np
from tkinter import *   

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
            
def filter_display(win,file):
    def Quit():
        win.destroy()
        #window.deiconify()
    
    width = win.winfo_screenwidth()/3
    height = win.winfo_screenheight()/3
    win.geometry("%dx%d+%d+%d" % ( width , height , width  , height) )
    win.title("Filter Editor")
    frame = Frame(win)
    frame.pack(side=TOP)
    submit = Button(frame, text = 'Default Smoothing', width = 20 ,command=fastsmooth(file))
    submit.pack(side=LEFT,padx = 10, pady = 0)
    quit = Button(frame, text = 'Quit', width = 20 ,command=Quit)
    quit.pack(side=LEFT, padx = 10, pady = 0)
    frame = Frame(win)
    frame.pack(side=TOP)
    vlist = ["butterworth", "average", "gaussian"]
    
    Combo = ttk.Combobox(frame, values = vlist)
    Combo.set("Pick a Filter")
    Combo.pack(side=LEFT,padx = 0, pady = 20)
    win.mainloop()

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
