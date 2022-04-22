from tkinter import *
from tkinter import ttk
from BVHsmoother.smooth import smooth
import numpy as np
from tkinter import *   
from PIL import Image, ImageTk
from tkinter import messagebox


def fastsmooth(filename):
    filter = 'butterworth'
    border = 100 
    u0 = 60
    order = 2
    median = None
    sigma = None
    smooth(filename,filename,filter,order,border,u0, median , sigma)


def filter_display(win,file):
    def Quit():
        win.destroy()
        #window.deiconify()
    def default_filter():
        fastsmooth(file)
        messagebox.showinfo(title="Filter Info", message="The butterworth filter was applied successfully")
        Quit()

    width = win.winfo_screenwidth()/3
    height = win.winfo_screenheight()/3
    win.geometry("%dx%d+%d+%d" % ( width , height , width  , height) )
    win.title("Filter Editor")
    frame = Frame(win)
    frame.pack(side=TOP)
    submit = Button(frame, text = 'Default Smoothing', width = 20 ,command=default_filter)
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