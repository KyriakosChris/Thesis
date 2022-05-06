from tkinter import *
from tkinter import ttk
from BVHsmoother.smooth import smooth
import numpy as np
from tkinter import *   
from PIL import Image, ImageTk
from tkinter import messagebox

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx()
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffff", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


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

def display_video(label,video):
   # iterate through video data
   for image in video.iter_data():
      # convert array into image
      img = Image.fromarray(image)
      # Convert image to PhotoImage
      image_frame = ImageTk.PhotoImage(image = img)
      # configure video to the lable
      label.config(image=image_frame)
      label.image = image_frame

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
                pos[i] = pos[i]*positions[i]
            for n,i in enumerate(pos):
                if n == len(pos) -1:
                    l += str(i) + '\n'
                else:
                    l += str(i) + ' '
            Edited.append(l)
        else:
            Edited.append(line)
    try:
        save_file = open(file, 'wt')
        for line in Edited:
                save_file.write(str(line))
        save_file.close()
    except:
        pass
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

def CorrectionOfPositions(file,positions):

    data = open(file, 'r')
    Lines = data.readlines()
    motion = False
    Edited = []
    counter = 0
    for line in Lines :

        if 'Frame Time:' in line:
            motion = True
            Edited.append(line)
            continue
        if motion :
            pos = line.split(" ")
            l = ''
            pos  = [float(i) for i in pos]

            for i in range(0,3): 
                pos[i] = positions[counter][0][i]

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
        for line in Edited:
                geeky_file.write(str(line))
        geeky_file.close()
    except:
        print("Unable to write to file")        
def filter_display(win,file):
    def Quit():
        win.destroy()
    
    def event(event=None):
        filter = Combo.get()
        if comboframe.winfo_exists():
            for widget in comboframe.winfo_children():
                widget.destroy()
    

        if filter == 'butterworth':
            question = Label(comboframe, text = '❔', fg = "black")
            CreateToolTip(widget = question, text = "Border")
            Label(comboframe, text = "FFT Border: ", fg = "black")
            Border = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Border.set(100)
            question = Label(comboframe, text = '❔', fg = "black")
            CreateToolTip(widget = question, text = "Cutoff")
            Label(comboframe, text = "Cutoff frequency: ", fg = "black")
            Uo = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Uo.set(60)
            question = Label(comboframe, text = '❔', fg = "black")
            CreateToolTip(widget = question, text = "Order")
            Label(comboframe, text = "Order: ", fg = "black")
            Order = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Order.set(2)
            
        elif filter == 'average':
            question = Label(comboframe, text = '❔', fg = "black")
            CreateToolTip(widget = question, text = "Average")
            Label(comboframe, text = "Median: ", fg = "black")
            Median = ttk.Spinbox(comboframe, from_=2, to=10000, width=5, textvariable=IntVar())
            Median.set(35)
            
        elif filter == 'gaussian':
            question = Label(comboframe, text = '❔', fg = "black")
            CreateToolTip(widget = question, text = "Border")
            Label(comboframe, text = "FFT Border: ", fg = "black")
            Border = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Border.set(100)
            question = Label(comboframe, text = '❔', fg = "black")
            CreateToolTip(widget = question, text = "Sigma")
            Label(comboframe, text = "Sigma: ", fg = "black")
            Sigma = ttk.Spinbox(comboframe, from_=1, to=10000, width=5, textvariable=IntVar())
            Sigma.set(30)
            
        for widget in comboframe.winfo_children():
            widget.pack(side=LEFT,padx=5, pady=10)
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
    menubar = Menu(win)
    filemenu = Menu(menubar, tearoff=0)

    filemenu.add_command(label="Exit", command=Quit)
    menubar.add_cascade(label="File", menu=filemenu)
    
    win.config(menu=menubar)
    frame = Frame(win)
    frame.pack(side=TOP)
    vlist = ["butterworth", "average", "gaussian"]
    label = Label(frame, text = "Choose the filter type", fg = "black")
    label.pack(side=LEFT, padx = 20, pady = 20)
    Combo = ttk.Combobox(frame, values = vlist)
    Combo.set("Pick a Filter")
    Combo.pack(side=LEFT,padx = 20, pady = 20)
    Combo.bind("<<ComboboxSelected>>", event)
    question = Label(frame, text = '❔', fg = "black")
    question.pack(side=LEFT)
    CreateToolTip(widget = question, text = "Filter Details")
    comboframe = Frame(win)
    comboframe.pack(side=TOP)
    submit_frame = Frame(win)
    submit_frame.pack(side=TOP)
    win.mainloop()