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

def string_Parse(str):
    if str == None:
        return False
    if str.isdigit():
        return False
    else:
        return True

def Try_parse(stringToInt):
    try:
        variable = int(stringToInt)
    except :
        variable = None
    return variable
def filter_display(win,file):
    def Quit():
        win.destroy()
        #window.deiconify()
    def default_filter():
        fastsmooth(file)
        messagebox.showinfo(title="Filter Info", message="The butterworth filter was applied successfully")
        Quit()
    def event(event=None):
        filter = Combo.get()
        if comboframe.winfo_exists():
            for widget in comboframe.winfo_children():
                widget.destroy()
    

        if filter == 'butterworth':
            Label(comboframe, text = "FFT Border: ", fg = "black")
            Border = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Border.set(1)
            Label(comboframe, text = "Cutoff frequency: ", fg = "black")
            Uo = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Uo.set(1)
            Label(comboframe, text = "Order: ", fg = "black")
            Order = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Order.set(1)
            
        elif filter == 'average':
            Label(comboframe, text = "Median: ", fg = "black")
            Median = ttk.Spinbox(comboframe, from_=2, to=10000, width=5, textvariable=IntVar())
            Median.set(2)
            
        elif filter == 'gaussian':
            Label(comboframe, text = "FFT Border: ", fg = "black")
            Border = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Border.set(1)
            Label(comboframe, text = "Sigma: ", fg = "black")
            Sigma = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Sigma.set(1)
            
        for widget in comboframe.winfo_children():
            widget.pack(side=LEFT,padx=15, pady=10)
        if len(comboframe.winfo_children())> 1 :    
            if submit_frame.winfo_exists():
                for widget in submit_frame.winfo_children():
                    widget.destroy()
            if filter == 'butterworth':
                submit = Button(submit_frame, text='Submit',width = 20, command=lambda: click(filter=filter,border=Border.get(),uo=Uo.get(),order=Order.get()))
            elif filter == 'average' :
                submit = Button(submit_frame, text='Submit',width = 20, command=lambda: click(filter=filter,median=Median.get()))
            elif filter == 'gaussian':
                submit = Button(submit_frame, text='Submit',width = 20, command=lambda: click(filter=filter,border=Border.get(),sigma=Sigma.get())) 
            submit.pack(side=TOP,pady=20)
    def click(filter, border=None,uo=None,order=None,median=None,sigma=None) :
        print(filter, border,uo,order,median,sigma)
        print(type(median))
        print(string_Parse(median))
        if string_Parse(border) or string_Parse(uo) or string_Parse(order) or string_Parse(median) or string_Parse(sigma):
            messagebox.showinfo(title="Input Info", message='The filter parameteres must be integers.')
            return
        
        if filter == 'average' and int(median) <2:
            messagebox.showinfo(title="Median Info", message='The median must be greater than one.')
            return
        smooth(filename=file,out=file, filter=filter,border= Try_parse(border),order=Try_parse(order),uo=Try_parse(uo),median=Try_parse(median),sigma=Try_parse(sigma))
        messagebox.showinfo(title="Filter Info", message='The ' +filter+ ' was applied successfully.')
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
    label = Label(frame, text = "Choose the filter type", fg = "black")
    label.pack(side=LEFT, padx = 20, pady = 20)
    Combo = ttk.Combobox(frame, values = vlist)
    Combo.set("Pick a Filter")
    Combo.pack(side=LEFT,padx = 20, pady = 20)
    Combo.bind("<<ComboboxSelected>>", event)
    comboframe = Frame(win)
    comboframe.pack(side=TOP)
    submit_frame = Frame(win)
    submit_frame.pack(side=TOP)



    win.mainloop()


file = "D:\\tuc\\Github\\Thesis\\BVH\\cxk\\cxk.bvh"
win = Tk()
win.grab_set()
filter_display(win,file)