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
from functions import PositionEdit


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
        def open_file():
            global videoplayer
            videoplayer = TkinterVideo(master=window, scaled=True, pre_load=False)
            videoplayer.load(r"{}".format(file))
            videoplayer.place(x=0, y=600, height=480, width=700)
            videoplayer.play()

        def playAgain():
            videoplayer.play()
        
        def Reset():

            videoplayer.destroy()
            open_file()

        def PauseVideo():
            videoplayer.pause()

        window = self.replace_window(self.root)
        basename = os.path.basename(self.file_name)
        video_name = basename[:basename.rfind('.')] 
        file = f'{self.folder_name}/{video_name}/{"3d_pose"}.mp4'

        window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
        window.title("BVH Editor")
        photo = PhotoImage(file = "TUC.gif")
        tuc = Label(window, image = photo)
        tuc.place(x=-2, y=-2)
        
        label0 = Label(window, text = "Give the XYZ thresholds (3 float numbers): ", fg = "black", font= "none 12 bold")
        label0.place(x=0, y=290)

        label1 = Label(window, text = "Give X threshold: ", fg = "black", font= "none 12 bold")
        label1.place(x=0, y=310)
        Xinput = Entry(window,width=5)
        Xinput.place(x=150, y=312.5)
        
        label2 = Label(window, text = "Give Y threshold: ", fg = "black", font= "none 12 bold")
        label2.place(x=200, y=310)
        Yinput = Entry(window,width=5)
        Yinput.place(x=350, y=312.5)

        label3 = Label(window, text = "Give Z threshold: ", fg = "black", font= "none 12 bold")
        label3.place(x=400, y=310)
        Zinput = Entry(window,width=5)
        Zinput.place(x=550, y=312.5)

        submit = Button(window, text = 'Submit', width = 30,command=click)
        submit.place(x=0, y=390)
        ChangeMenu = Button(window, text = "Animate Another Video: ",width = 30, command=self.Model)
        ChangeMenu.place(x=300, y=390)
        done = Label(window, text="")
        done.place(x=0, y=425)
        lbl1 = Label(window, text="BVH Video Player", font="none 12 bold")
        lbl1.place(x=0, y=465)
        openbtn = Button(window, text='Open Video', command=lambda: open_file())
        openbtn.place(x=10, y=500)

        playbtn = Button(window, text='Play Video', command=lambda: playAgain())
        playbtn.place(x=110, y=500)
        
        stopbtn = Button(window, text='Reset Video', command=lambda: Reset())
        stopbtn.place(x=210, y=500)
        
        pausebtn = Button(window, text='Pause Video', command=lambda: PauseVideo())
        pausebtn.place(x=310, y=500)

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
            self.folder_name = fd.askdirectory(title='Browse a folder',initialdir='/')
            if len(self.folder_name) == 0:
                messagebox.showwarning("Folder Warning", "The folder failed to be browsed")
            else:
                print('Folder ', self.folder_name, ' ,was set successfully!')

        # create a tkinter window
        window = self.replace_window(self.root)     

        
        #setting tkinter window size
        window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
        window.title("Video To BVH Estimator")
        photo = PhotoImage(file = "TUC.gif")
        tuc = Label(window, image = photo)
        tuc.place(x=-2, y=-2)

        # Create a Button
        button1 = Label(window, text = "Enter video file: ", fg = "black", font= "none 12 bold")
        button1.place(x=0, y=290)
        file_button = Button(window,text='Browse a File',command=select_file)
        file_button.place(x=150, y=290)
        button2 = Label(window, text = "Output folder: ", fg = "black", font= "none 12 bold")
        button2.place(x=250, y=290)
        folder_button = Button(window,text='Browse a Folder',command=select_folder)
        folder_button.place(x=400, y=290)

        submit = Button(window, text = 'Submit', width = 30,command=click)
        submit.place(x=0, y=330)
        ChangeMenu = Button(window, text = "Animate and the Edit Results: ",width = 30,command=self.EditBvh)
        ChangeMenu.place(x=300, y=330)
        ChangeMenu.config(state="disabled")

        # label = Label(window, text = "Console Redirected: ", fg = "black", font= "none 12 bold")
        # label.place(x=0, y=360)
        # frame = Frame(window)
        # frame.place(x = 0 , y = 390)
        # text = Text(frame)
        # #text.place(x=0, y=390, height=30, width=200)
        # text.pack(side='left',fill='both', expand=True)
        # scrollbar = Scrollbar(frame)
        # scrollbar.pack(side='right', fill='y')
        # text['yscrollcommand'] = scrollbar.set
        # scrollbar['command'] = text.yview
        # sys.stdout = Redirect(text)
   
        window.wm_protocol("WM_DELETE_WINDOW", self.root.destroy)
        window.mainloop()


if __name__ == '__main__':
    menu = MainMenu()
    menu.Model()