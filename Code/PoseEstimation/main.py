from videopose import inference_video
from threading import *
from tkinter import *   
import sys
from tkinter import filedialog as fd
from PIL import Image,ImageTk
import os
from tkinter import messagebox
from functions import PositionEdit, fastsmooth , new_animation
from tkvideo import tkvideo
from animate_bvh.bvh import *
global  t1
class Redirect():

    def __init__(self, widget, autoscroll=True):
        self.widget = widget
        self.autoscroll = autoscroll

    def write(self, text):
        if "Processing..." in text or "Rendering..." in text:
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
        self.prediction = None
        

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
                PositionEdit(bvhpath,positions)
                messagebox.showinfo(title="Edit Info", message="Edit completed successfully")
                self.prediction[:, 0, 0] /= X
                self.prediction[:, 0, 1] /= Y
                self.prediction[:, 0, 2] /= Z
            else:
                messagebox.showwarning(title="Edit Info", message="Wrong Input")
                
        def is_float(element):
            try:
                float(element)
                return True
            except ValueError:
                return False
                
        def open_file():
            global videoplayer
            global frame10
            frame10 = Frame(window)
            frame10.pack(side=TOP)
            video_label = Label(frame10)
            video_label.pack(side=LEFT)
            videoplayer = tkvideo(self.file, video_label, loop = 0 ,size = (700, 480))
            videoplayer.play()
            openbtn.config(state="disabled")
            playbtn.config(state="normal")
            resetbtn.config(state="normal")
            fastresetbtn.config(state="normal")

        def playAgain():
            videoplayer.play()
        
        def Fast_Reset():
            frame10.destroy()
            open_file()

        def Reset():
            frame10.destroy()
            create_video(self.bvhName , self.file, False)
            #new_animation(self.prediction,file)
            open_file()
            
        def buttonSmooth(file):
            Smoothbutton.config(state="disabled")
            fastsmooth(file)
            messagebox.showinfo(title="Filter Info", message="Filter was applied successfully")
            Smoothbutton.config(state="normal")
            
        window = self.replace_window(self.root)
        frame = Frame(window)
        frame.pack()
        t1.join()
        basename = os.path.basename(self.file_name)
        video_name = basename[:basename.rfind('.')] 
        self.file = f'{self.folder_name}/{video_name}/{"3d_pose"}.mp4'
        self.bvhName = f'{self.folder_name}/{video_name}/{video_name}.bvh'
        window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
        window.title("BVH Editor")
        window.resizable(True, True)
        im = Image.open(r"TUC.jpg")
        im1 = im.resize((window.winfo_screenwidth() ,300), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(im1)
        tuc = Label(frame, image = new_img)
        tuc.pack(side=LEFT)

        frame2 = Frame(window)
        frame2.pack(side=TOP)
        label0 = Label(frame2, text = "Give the XYZ thresholds (3 float numbers): ", fg = "black", font= "none 12 bold")
        label0.pack(side=LEFT)

        frame3 = Frame(window)
        frame3.pack(side=TOP)

        label1 = Label(frame3, text = "Give X threshold: ", fg = "black", font= "none 12 bold")
        label1.pack(side=LEFT)
        Xinput = Entry(frame3,width=5)
        Xinput.pack(side=LEFT)
        
        label2 = Label(frame3, text = "Give Y threshold: ", fg = "black", font= "none 12 bold")
        label2.pack(side=LEFT)
        Yinput = Entry(frame3,width=5)
        Yinput.pack(side=LEFT)

        label3 = Label(frame3, text = "Give Z threshold: ", fg = "black", font= "none 12 bold")
        label3.pack(side=LEFT)
        Zinput = Entry(frame3,width=5)
        Zinput.pack(side=LEFT)


        frame4 = Frame(window)
        frame4.pack(side=TOP)
  
        submit = Button(frame4, text = 'Submit', width = 20 ,command=click)
        submit.pack(side=LEFT)
        temp = Label(frame4, text = "",width = 5, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)
        Smoothbutton = Button(frame4, text = "Fast bvh Smoothing: ", width = 20, command=lambda: buttonSmooth(self.bvhName))
        Smoothbutton.pack(side=LEFT)
        temp = Label(frame4, text = "",width = 5, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)
        ChangeMenu = Button(frame4, text = "Animate Another Video: ", width = 20, command=self.Model)
        ChangeMenu.pack(side=LEFT)

        frame6 = Frame(window)
        frame6.pack(side=TOP)

        frame7 = Frame(window)
        frame7.pack(side=TOP)
        temp = Label(frame7, text = "",height= 1, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)

        frame07 = Frame(window)
        frame07.pack(side=TOP)
        lbl1 = Label(frame07, text="BVH Video Player", font="none 12 bold")
        lbl1.pack(side=LEFT)


        frame8 = Frame(window)
        frame8.pack(side=TOP)
        temp = Label(frame8, text = "",height= 1, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)

        frame9 = Frame(window)
        frame9.pack(side=TOP)

        openbtn = Button(frame9, text='Open Video', command=lambda: open_file())
        openbtn.pack(side=LEFT)
        temp = Label(frame9, text = "",width = 10, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)
        playbtn = Button(frame9, text='Play Video', command=lambda: playAgain())
        playbtn.pack(side=LEFT)
        temp = Label(frame9, text = "",width = 10, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT) 
        resetbtn = Button(frame9, text='Reset Video', command=lambda: Reset())
        resetbtn.pack(side=LEFT)
        temp = Label(frame9, text = "",width = 10, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT) 
        fastresetbtn = Button(frame9, text='Fast Reset Video', command=lambda: Fast_Reset())
        fastresetbtn.pack(side=LEFT)


        playbtn.config(state="disabled")
        resetbtn.config(state="disabled")
        fastresetbtn.config(state="disabled")

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
                self.prediction = inference_video(self.file_name,self.folder_name,'alpha_pose')
                enable_buttons()
                print(self.prediction.shape)

        def threading():
            global t1
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

        frame = Frame(window)
        frame.pack()

        window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
        window.title("Video To BVH Estimator")
        window.resizable(True, True)
        im = Image.open(r"TUC.jpg")

        im1 = im.resize((window.winfo_screenwidth() ,300), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(im1)
        tuc = Label(frame, image = new_img)
        tuc.pack(side=LEFT)
        
        frame2 = Frame(window)
        frame2.pack(side=TOP)
        # Create a Button
        button1 = Label(frame2, text = "Enter video file: ", fg = "black", font= "none 12 bold")
        button1.pack(side=LEFT)
        temp = Label(frame2, text = "",width = 3, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)
        file_button = Button(frame2,text='Browse a File',command=select_file)
        file_button.pack(side=LEFT)
        temp = Label(frame2, text = "",width = 3, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)
        button2 = Label(frame2, text = "Output folder: ", fg = "black", font= "none 12 bold")
        button2.pack(side=LEFT)
        temp = Label(frame2, text = "",width = 3, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)
        folder_button = Button(frame2,text='Browse a Folder',command=select_folder)
        folder_button.pack(side=LEFT)

        frame3 = Frame(window)
        frame3.pack(side=TOP)

        temp = Label(frame3, text = "",width = 30, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)

        frame4 = Frame(window)
        frame4.pack(side=TOP)

        submit = Button(frame4, text = 'Submit', width = 30,command=threading)
        submit.pack(side=LEFT)
        temp = Label(frame4, text = "",width = 5, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)
        ChangeMenu = Button(frame4, text = "Animate and the Edit Results: ",width = 30,command=self.EditBvh)
        ChangeMenu.pack(side=LEFT)
        ChangeMenu.config(state="disabled")

        frame5 = Frame(window)
        frame5.pack(side=TOP)
        temp = Label(frame5, text = "",width = 30, fg = "black", font= "none 12 bold")
        temp.pack(side=LEFT)

        frame6 = Frame(window)
        frame6.pack(side=TOP)

        label = Label(frame6, text = "Console Redirect: ", fg = "black", font= "none 12 bold")
        label.pack(side=LEFT)
        frame = Frame(window)
        frame.pack(side=TOP)
        text = Text(frame)
        text.pack(side='left',fill='both', expand=True)
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        text['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = text.yview
        sys.stdout = Redirect(text)
        window.wm_protocol("WM_DELETE_WINDOW", self.root.destroy)
        window.mainloop()


if __name__ == '__main__':
    menu = MainMenu()
    menu.Model()