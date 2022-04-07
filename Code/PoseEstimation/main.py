from videopose import inference_video
import tkinter as tk
import sys
import subprocess
from threading import *
from tkinter import *   
from tkinter import filedialog as fd
# --- classes ---

class Redirect():

    def __init__(self, widget, autoscroll=True):
        self.widget = widget
        self.autoscroll = autoscroll

    def write(self, text):
        if "Processing" in text:
            self.widget.delete("end-1c linestart", "end")
            self.widget.insert('end', '\n')
        if "===========================>" in text or "--------------" in text:
            self.widget.insert('end', '\n')
        self.widget.insert('end', text)
        if self.autoscroll:
            self.widget.see("end")  # autoscroll

    def flush(self):
        pass
def Tkinder():
    def click():
        global file_name
        global folder_name
        inference_video(file_name,folder_name,'alpha_pose')

    def threading():
        # Call work function
        t1=Thread(target=click)
        t1.start()
  
    def select_file():
        global file_name
        filetypes = (
            ('video files', '*.mp4'),
            ('video files', '*.avi'),
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
    canvas = Canvas(window, width= 1700 , height= 900)
    canvas.grid(columnspan=3)
    #window.geometry('900x900')
    window.title("Video To BVH Estimator")
    photo = PhotoImage(file = "TUC.gif")
    tuc = Label(window, image = photo, bg = "white")
    tuc.place(x=-2, y=-2)

    # Create a Button
            # open button
    button1 = Label(window, text = "Enter video file: ", bg = "white", fg = "black", font= "none 12 bold")
    button1.place(x=0, y=290)
    open_button = Button(
        window,
        text='Browse a File',
        command=select_file
    )
    open_button.place(x=150, y=290)
    button2 = Label(window, text = "Output folder: ", bg = "white", fg = "black", font= "none 12 bold")
    button2.place(x=250, y=290)
    open_button = Button(
        window,
        text='Browse a Folder',
        command=select_folder
    )
    open_button.place(x=400, y=290)
    
    # #open_button.pack(expand=True)
    submit = Button(window, text = 'Submit', width = 30,command=threading)
    submit.place(x=0, y=330)

    label = Label(window, text = "Console Redirected: ", bg = "white", fg = "black", font= "none 12 bold")
    label.place(x=0, y=360)
    frame = Frame(window)
    frame.place(x = 0 , y = 390)
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
