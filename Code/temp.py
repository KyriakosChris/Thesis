import filecmp
from videopose import inference_video
from threading import *
from tkinter import *   
import sys
from tkinter import filedialog as fd
from PIL import Image,ImageTk
from tkVideoPlayer import TkinterVideo
import os
from tkinter import messagebox
from functions import PositionEdit, fastsmooth

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

class MainMenu():
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        self.current_window = None
        

    def getfile(self):
        return self.file_name

    def getfolder(self):
        return self.folder_name

    def  replace_window(self,root):
        """Destroy current window, create new window"""
        if self.current_window is not None:
            self.current_window.destroy()
        self.current_window = Toplevel(root)
        # if the user kills the window via the window manager,
        # exit the application. 

        return self.current_window
    def EditBvh(self):
        def click():
            if is_float(Xinput.get()) and is_float(Yinput.get()) and is_float(Zinput.get()) and self.file_name != '' and self.folder_name != '':
                X = float(Xinput.get())
                Y = float(Yinput.get())
                Z = float(Zinput.get())
                positions = (X,Y,Z)
                basename = os.path.basename(self.file_name)
                video_name = basename[:basename.rfind('.')]
                bvhpath = f'{self.folder_name}/{video_name}/{video_name}.bvh'
                videoplayer.destroy()
                PositionEdit(bvhpath,positions)
                done.config(text ="Edit completed successfully")
                
        def is_float(element):
            try:
                float(element)
                return True
            except ValueError:
                return False
                
        def open_file(offsetx,offsety):
            global videoplayer
            openbtn.config(state="disabled")
            videoplayer = TkinterVideo(master=window, scaled=True, pre_load=False)
            videoplayer.load(r"{}".format(file))
            videoplayer.place(x=0+offsetx, y=600, height=480, width=700)
            videoplayer.play()

        def playAgain():
            videoplayer.play()
        
        def Reset(offsetx,offsety):

            videoplayer.destroy()
            open_file(offsetx,offsety)

        def PauseVideo():
            videoplayer.pause()
            
        def buttonSmooth(file):
            Smoothbutton.config(state="disabled")
            fastsmooth(file)
            messagebox.showinfo(title="Filter Info", message="Filtering more than once may not improve further the results")
            Smoothbutton.config(state="normal")
            
        window = self.replace_window(self.root)
        frame = Frame(window)
        frame.pack()
        frame2 = Frame(window)
        frame2.pack(side=BOTTOM)
        
        basename = os.path.basename(self.file_name)
        video_name = basename[:basename.rfind('.')] 
        file = f'{self.folder_name}/{video_name}/{"3d_pose"}.mp4'
        bvhName = f'{self.folder_name}/{video_name}/{video_name}.bvh'
        window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
        window.title("BVH Editor")
        #window.resizable(0, 0)
        offsetx = window.winfo_screenwidth()/3
        offsety = window.winfo_screenheight()/16
        im = Image.open(r"TUC.jpg")
        width, height = im.size
        im1 = im.resize((window.winfo_screenwidth() ,300), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(im1)
        tuc = Label(window, image = new_img)
        tuc.place(x=-2, y=-2)

        label0 = Label(window, text = "Give the XYZ thresholds (3 float numbers): ", fg = "black", font= "none 12 bold")
        label0.place(x=0+offsetx, y=290+offsety)

        label1 = Label(window, text = "Give X threshold: ", fg = "black", font= "none 12 bold")
        label1.place(x=0+offsetx, y=310+offsety)
        Xinput = Entry(window,width=5)
        Xinput.place(x=150+offsetx, y=312.5+offsety)
        
        label2 = Label(window, text = "Give Y threshold: ", fg = "black", font= "none 12 bold")
        label2.place(x=200+offsetx, y=310+offsety)
        Yinput = Entry(window,width=5)
        Yinput.place(x=350+offsetx, y=312.5+offsety)

        label3 = Label(window, text = "Give Z threshold: ", fg = "black", font= "none 12 bold")
        label3.place(x=400+offsetx, y=310+offsety)
        Zinput = Entry(window,width=5)
        Zinput.place(x=550+offsetx, y=312.5+offsety)

        submit = Button(window, text = 'Submit', width = 30,command=click)
        submit.place(x=0+offsetx, y=390+offsety)
        Smoothbutton = Button(window, text = "Fast bvh Smoothing: ",width = 30, command=lambda: buttonSmooth(bvhName))
        Smoothbutton.place(x=250+offsetx, y=390+offsety)
        ChangeMenu = Button(window, text = "Animate Another Video: ",width = 30, command=self.Model)
        ChangeMenu.place(x=500+offsetx, y=390+offsety)
        done = Label(window, text="")
        done.place(x=0+offsetx, y=425+offsety)
        lbl1 = Label(window, text="BVH Video Player", font="none 12 bold")
        lbl1.place(x=0+offsetx, y=465+offsety)
        openbtn = Button(window, text='Open Video', command=lambda: open_file(offsetx,offsety))
        openbtn.place(x=10+offsetx, y=500+offsety)

        playbtn = Button(window, text='Play Video', command=lambda: playAgain())
        playbtn.place(x=210+offsetx, y=500+offsety)
        
        stopbtn = Button(window, text='Reset Video', command=lambda: Reset(offsetx,offsety))
        stopbtn.place(x=410+offsetx, y=500+offsety)
        
        pausebtn = Button(window, text='Pause Video', command=lambda: PauseVideo())
        pausebtn.place(x=610+offsetx, y=500+offsety)

        window.wm_protocol("WM_DELETE_WINDOW", self.root.destroy)
        window.mainloop()
    def Model(self):


        def disable_buttons():
            file_button.config(state="disabled")
            folder_button.config(state="disabled")
            submit.config(state="disabled")

        def enable_buttons():
            submit.config(state="normal")
            file_button.config(state="normal")
            folder_button.config(state="normal")
            ChangeMenu.config(state="normal")


        def click():
            if len(self.file_name) == 0 or len(self.folder_name) == 0:
                messagebox.showwarning("Input Warning", "The folder or the file failed to be browsed")
            else:
                disable_buttons()
                inference_video(self.file_name,self.folder_name,'alpha_pose')
                enable_buttons()

        def threading():
            t1=Thread(target=click)
            t1.start()
    
        def select_file():
            filetypes = (('video files', '*.mp4'),('video files', '*.avi'),('All files', '*.*'))

            self.file_name = fd.askopenfilename(title='Browse a file',initialdir='/',filetypes=filetypes)
            if len(self.file_name) == 0:
                messagebox.showwarning("File Warning", "The file failed to load")
            else:
                print('File ', self.file_name, ' ,was loaded successfully!')

        def select_folder():
            window.update()
            self.folder_name = fd.askdirectory(title='Browse a folder',initialdir='/')
            if len(self.folder_name) == 0:
                messagebox.showwarning("Folder Warning", "The folder failed to be browsed")
            else:
                print('Folder ', self.folder_name, ' ,was set successfully!')

        # create a tkinter window
        window = self.replace_window(self.root)     


        # myframe = Frame(window)

        # myframe.pack(fill=BOTH, expand=YES)

        # mycanvas = ResizingCanvas(myframe,width=window.winfo_screenwidth(), height=window.winfo_screenheight(), highlightthickness=0)

        # mycanvas.pack(fill=BOTH, expand=YES)
        
        #setting tkinter window size
        window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
        window.title("Video To BVH Estimator")
        #window.resizable(0, 0)
        #window.resizable(True, True)
        offsetx = window.winfo_screenwidth()/3
        offsety = window.winfo_screenheight()/16
        im = Image.open(r"TUC.jpg")
        width, height = im.size
        im1 = im.resize((window.winfo_screenwidth() ,300), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(im1)
        tuc = Label(window, image = new_img)
        tuc.place(x=-2, y=-2)

        # Create a Button
        button1 = Label(window, text = "Enter video file: ", fg = "black", font= "none 12 bold")
        button1.place(x=0+offsetx, y=290+offsety)
        file_button = Button(window,text='Browse a File',command=select_file)
        file_button.place(x=150+offsetx, y=290+offsety)
        button2 = Label(window, text = "Output folder: ", fg = "black", font= "none 12 bold")
        button2.place(x=250+offsetx, y=290+offsety)
        folder_button = Button(window,text='Browse a Folder',command=select_folder)
        folder_button.place(x=400+offsetx, y=290+offsety)

        submit = Button(window, text = 'Submit', width = 30,command=threading)
        submit.place(x=0+offsetx, y=330+offsety)
        ChangeMenu = Button(window, text = "Animate and the Edit Results: ",width = 30,command=self.EditBvh)
        ChangeMenu.place(x=300+offsetx, y=330+offsety)
        ChangeMenu.config(state="disabled")

        label = Label(window, text = "Console Redirected: ", fg = "black", font= "none 12 bold")
        label.place(x=0+offsetx, y=360+offsety)
        frame = Frame(window)
        frame.place(x = 0+offsetx , y = 390+offsety)
        text = Text(frame)
        #text.place(x=0, y=390, height=30, width=200)
        text.pack(side='left',fill='both', expand=True)
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        text['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = text.yview
        sys.stdout = Redirect(text)
        # mycanvas.addtag_all("all")
        window.wm_protocol("WM_DELETE_WINDOW", self.root.destroy)
        window.mainloop()


if __name__ == '__main__':
    menu = MainMenu()
    menu.Model()