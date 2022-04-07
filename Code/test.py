from ast import And
import os
import subprocess
import sys
from tkinter import *   
from tkinter import filedialog as fd
from terminal import Redirect

global file_name
global folder_name
def BVHedit(file,outfolder,positions):
    basename = os.path.basename(file)
    video_name = basename[:basename.rfind('.')]
    path = f'{outfolder}/{video_name}.bvh'

    
    data = open(file, 'r')
    Lines = data.readlines()
    motion = False
    Edited = []
    for n,line in enumerate(Lines) :

        if ( line.__contains__('Frame Time:')):
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
        geeky_file = open(path, 'wt')
        for line in Edited:
                geeky_file.write(str(line))
        geeky_file.close()
    except:
        print("Unable to write to file")
        
def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

def Tkinder():
    file_name = ''
    folder_name = ''
    def click():
        global file_name
        global folder_name
        if is_float(Xinput.get()) and is_float(Yinput.get()) and is_float(Zinput.get()) and file_name != '' and folder_name != '':
            X = float(Xinput.get())
            Y = float(Yinput.get())
            Z = float(Zinput.get())
            input = file_name
            output = folder_name
            print(Xinput.get(),Yinput.get(),Zinput.get())
            print(file_name)
            print(folder_name)
            BVHedit(file_name,folder_name,(X,Y,Z))

    def select_file():
        global file_name
        filetypes = (
            ('bvh files', '*.bvh'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        file_name = filename
    def select_folder():
        global folder_name
        foldername = fd.askdirectory(
            title='Open a folder',
            initialdir='/')
        folder_name = foldername
    # create a tkinter window
    window = Tk()       
    window.configure(background="white")
    # Open window having dimension 100x100
    window.geometry('900x900')
    window.title("BVH Position Editor")
    photo = PhotoImage(file = "TUC.gif")
    tuc = Label(window, image = photo, bg = "white")
    tuc.place(x=-2, y=-2)
    
    label0 = Label(window, text = "Give the XYZ thresholds (3 float numbers): ", bg = "white", fg = "black", font= "none 12 bold")
    label0.place(x=0, y=290)

    label1 = Label(window, text = "Give X threshold: ", bg = "white", fg = "black", font= "none 12 bold")
    label1.place(x=0, y=310)
    Xinput = Entry(window,width=5, bg = "white")
    Xinput.place(x=150, y=312.5)
    
    label2 = Label(window, text = "Give Y threshold: ", bg = "white", fg = "black", font= "none 12 bold")
    label2.place(x=200, y=310)
    Yinput = Entry(window,width=5, bg = "white")
    Yinput.place(x=350, y=312.5)

    label3 = Label(window, text = "Give Z threshold: ", bg = "white", fg = "black", font= "none 12 bold")
    label3.place(x=400, y=310)
    Zinput = Entry(window,width=5, bg = "white")
    Zinput.place(x=550, y=312.5)
    # Create a Button
            # open button
    button1 = Label(window, text = "Give BVH file: ", bg = "white", fg = "black", font= "none 12 bold")
    button1.place(x=0, y=350)
    open_button = Button(
        window,
        text='Browse a File',
        command=select_file
    )
    open_button.place(x=150, y=350)
    button2 = Label(window, text = "Output folder: ", bg = "white", fg = "black", font= "none 12 bold")
    button2.place(x=250, y=350)
    open_button = Button(
        window,
        text='Browse a Folder',
        command=select_folder
    )
    open_button.place(x=400, y=350)
    
    # #open_button.pack(expand=True)
    submit = Button(window, text = 'Submit', width = 30,command=click)
    submit.place(x=0, y=390)

    label = Label(window, text = "Console Redirected: ", bg = "white", fg = "black", font= "none 12 bold")
    label.place(x=0, y=420)
    frame = Frame(window)
    frame.place(x = 0 , y = 450)
    text = Text(frame)
    text.pack(side='left', fill='both', expand=True)
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side='right', fill='y')
    text['yscrollcommand'] = scrollbar.set
    scrollbar['command'] = text.yview

    old_stdout = sys.stdout    
    sys.stdout = Redirect(text)
    
    window.mainloop()

Tkinder()