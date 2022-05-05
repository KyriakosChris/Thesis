from videopose import inference_video
from threading import *
from tkinter import *   
import sys
from tkinter import filedialog as fd
from PIL import Image,ImageTk
import os
from tkinter import messagebox
from functions import PositionEdit, filter_display,ToolTip
from common.visualize import create_video
import datetime
from common.tkvideoplayer import TkinterVideo

class Redirect():

    def __init__(self, widget, autoscroll=True):
        self.widget = widget
        self.autoscroll = autoscroll
    def __del__(self):
        # Destructor
        pass
    def write(self, text):
        try:
            if "Processing..." in text or "Rendering..." in text:
                self.widget.delete("end-1c linestart", "end")
                self.widget.insert('end', '\n')
            if "===========================>" in text or "--------------" in text:
                self.widget.insert('end', '\n')
            self.widget.insert('end', text)
            if self.autoscroll:
                self.widget.see("end")  # autoscroll
        except:
            pass

    def flush(self):
        pass

class MainMenu():
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        self.current_window = None
        self.prediction = None
        # self.file_name = ""
        # self.folder_name = ""
        self.file_name = "C:\\Users\\msi\\Desktop\\testing\\VideoTo3dPoseAndBvh\\outputs\\inputvideo\\kunkun_cut_one_second.mp4"
        self.folder_name = "D:\\tuc\\Github\\Thesis\\BVH"
        

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
        def check_input():
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

        
        def play_video():
            def update_duration(event):
                
                """ updates the duration after finding the duration """
                end_time["text"] = str(datetime.timedelta(seconds=vid_player.duration()))
                progress_slider["to"] = vid_player.duration()


            def update_scale(event):
                """ updates the scale value """
                progress_slider.set(vid_player.current_duration())


            def load_video():
                """ loads the video """
                if self.file:
                    pass
                vid_player.load(self.file)
                progress_slider.config(to=0, from_=0)
                progress_slider.set(0)
                play_pause_btn["text"] = "Play"


            def seek(value):
                """ used to seek a specific timeframe """
                vid_player.seek(int(value))


            def skip(value: int):
                """ skip seconds """
                vid_player.skip_sec(value)
                progress_slider.set(progress_slider.get() + value)


            def play_pause():
                """ pauses and plays """
                if self.loaded:
                    load_video()
                    self.loaded = False
                if vid_player.is_paused():
                    vid_player.play()
                    play_pause_btn["text"] = "Pause"

                else:
                    vid_player.pause()
                    play_pause_btn["text"] = "Play"


            def video_ended(event):
                """ handle video ended """
                progress_slider.set(progress_slider["to"])
                play_pause_btn["text"] = "Play"
            self.loaded = True
            global frame8
            global vid_player
            frame8 = Frame(window)
            frame8.pack(side=TOP)

            vid_player = TkinterVideo(scaled=True, pre_load=False, master=frame8)
            vid_player.pack(side=LEFT ,expand=True, fill="both")

            vid_player = TkinterVideo(scaled=True, pre_load=False, master=frame8)
            vid_player.pack(expand=True, fill="both")

            play_pause_btn = Button(frame8, text="Play", command=play_pause)
            play_pause_btn.pack()

            skip_plus_5sec = Button(frame8, text="Skip -5 sec", command=lambda: skip(-5))
            skip_plus_5sec.pack(side="left")

            start_time = Label(frame8, text=str(datetime.timedelta(seconds=0)))
            start_time.pack(side="left")

            progress_slider = Scale(frame8, from_=0, to=0, orient="horizontal", command=seek)
            progress_slider.pack(side="left", fill="x", expand=True)

            end_time = Label(frame8, text=str(datetime.timedelta(seconds=0)))
            end_time.pack(side="left")

            vid_player.bind("<<Duration>>", update_duration)
            vid_player.bind("<<SecondChanged>>", update_scale)
            vid_player.bind("<<Ended>>", video_ended )

            skip_plus_5sec = Button(frame8, text="Skip +5 sec", command=lambda: skip(5))
            skip_plus_5sec.pack(side="left")

        def create_threading():
            t1=Thread(target=Reset)
            t1.start()

        def Reset():
            self.loaded = True
            try:              
                vid_player.destroy()
                resetbtn.config(state="disabled")
                for widgets in frame8.winfo_children():
                    widgets.destroy()
                frame8.destroy()
            except:
                pass
            text.pack(side=LEFT)
            create_video(self.bvhName , self.file)
            text.pack_forget()
            play_video()
            resetbtn.config(state="normal")
            
        def buttonSmooth(file):
            win = Toplevel(window)
            win.grab_set()
            filter_display(win,file)


        def change_window():

            try:
                vid_player.destroy()
                for widgets in frame8.winfo_children():
                    widgets.destroy()

                frame8.destroy()
            except:
                pass
            self.file_name = ""
            self.folder_name = ""
            self.file = ""
            self.bvhName = ""
            self.Model()
        def Help():
            filewin = Toplevel(self.root)
            width = filewin.winfo_screenwidth()/3
            height = filewin.winfo_screenheight()/3
            filewin.geometry("%dx%d+%d+%d" % ( width , height , width  , height) )
            text = Label(filewin, text = "TO DO...", fg = "black", font= "none 12 bold")
            text.pack()
        # reset to default the printing method
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


        window = self.replace_window(self.root)
        width = window.winfo_screenwidth()/2.5
        height = window.winfo_screenheight()
        window.geometry("%dx%d+%d+%d" % ( width , height , -8 +1.5*width/2 , 0) )
        #window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
        window.title("BVH Editor")
        window.resizable(0, True)
        frame = Frame(window)
        frame.pack()

        basename = os.path.basename(self.file_name)
        video_name = basename[:basename.rfind('.')] 
        self.file = f'{self.folder_name}\{video_name}\{"3d_pose"}.mp4'
        self.bvhName = f'{self.folder_name}/{video_name}/{video_name}.bvh'
        # window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
        # window.title("BVH Editor")
        # window.resizable(True, True)


        menubar = Menu(window)
        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=Help)
        menubar.add_cascade(label="Help", menu=helpmenu)
        window.config(menu=menubar)
        im = Image.open(r"menu.jpg")
        im1 = im.resize((int(width) ,300), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(im1)
        tuc = Label(frame, image = new_img)
        tuc.pack(side=LEFT)

        frame2 = Frame(window)
        frame2.pack(side=TOP)
        label0 = Label(frame2, text = "Give the XYZ thresholds (3 float numbers): ", fg = "black", font= "none 12 bold")
        label0.pack(side=LEFT)

        frame3 = Frame(window)
        frame3.pack(side=TOP)

        Label(frame3, text = "Give X threshold: ", fg = "black", font= "none 12 bold")
        Xinput = Entry(frame3,width=5)
        Label(frame3, text = "Give Y threshold: ", fg = "black", font= "none 12 bold")
        Yinput = Entry(frame3,width=5)
        Label(frame3, text = "Give Z threshold: ", fg = "black", font= "none 12 bold")
        Zinput = Entry(frame3,width=5)

        for widget in frame3.winfo_children():
            widget.pack(side=LEFT,padx=5, pady=5)

        frame4 = Frame(window)
        frame4.pack(side=TOP)
  
        Button(frame4, text = 'Submit', width = 20 ,command=check_input)
        Button(frame4, text = "Fast bvh Smoothing: ", width = 20, command=lambda: buttonSmooth(self.bvhName))
        Button(frame4, text = "Animate Another Video: ", width = 20, command=change_window)

        for widget in frame4.winfo_children():
            widget.pack(side=LEFT,padx=25, pady=15)

        frame5 = Frame(window)
        frame5.pack(side=TOP)
        lbl1 = Label(frame5, text="BVH Video Player", font="none 12 bold")
        lbl1.pack(side=LEFT,padx=5, pady=0)

        frame6 = Frame(window)
        frame6.pack(side=TOP)


        resetbtn = Button(frame6, text='Reset Video', command=lambda: create_threading())


        for widget in frame6.winfo_children():
            widget.pack(side=LEFT,padx=50, pady=0)

        frame7 = Frame(window)
        frame7.pack(side=TOP)

        text = Text(frame7,width=78 ,height = 1,relief='flat',bg='SystemButtonFace')
        text.pack_forget()
        sys.stdout = Redirect(text)

        play_video()
        window.wm_protocol("WM_DELETE_WINDOW", self.root.destroy)
        window.mainloop()
    def Model(self):
        def disable_buttons():
            # file_button.config(state="disabled")
            # folder_button.config(state="disabled")
            submit.config(state="disabled")

        def enable_buttons():
            submit.config(state="normal")
            # file_button.config(state="normal")
            # folder_button.config(state="normal")
            ChangeMenu.config(state="normal")


        def click():
            if len(self.file_name) == 0 or len(self.folder_name) == 0:
                messagebox.showwarning("Input Warning", "The folder or the file failed to be browsed")
            else:
                disable_buttons()
                self.prediction = inference_video(self.file_name,self.folder_name,'alpha_pose')
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
        def Help():
            filewin = Toplevel(self.root)
            width = filewin.winfo_screenwidth()/3
            height = filewin.winfo_screenheight()/3
            filewin.geometry("%dx%d+%d+%d" % ( width , height , width  , height) )
            text = Label(filewin, text = "TO DO...", fg = "black", font= "none 12 bold")
            text.pack()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        window = self.replace_window(self.root)     
        width = window.winfo_screenwidth()/2.5
        height = window.winfo_screenheight()
        window.geometry("%dx%d+%d+%d" % ( width , height , -8 +1.5*width/2 , 0) )
        #window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
        window.title("Video To BVH Estimator")
        window.resizable(0, True)

        frame = Frame(window)
        frame.pack()


        menubar = Menu(window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Video", command=select_file)
        filemenu.add_command(label="Save To", command=select_folder)
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=window.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=Help)
        menubar.add_cascade(label="Help", menu=helpmenu)
        window.config(menu=menubar)
        im = Image.open(r"menu.jpg")

        im1 = im.resize((int(width) ,300), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(im1)
        tuc = Label(frame, image = new_img)
        tuc.pack(side=LEFT)
        
        # frame2 = Frame(window)
        # frame2.pack(side=TOP)
        # Label(frame2, text = "Enter video file: ", fg = "black", font= "none 12 bold")
        # file_button = Button(frame2,text='Browse a File',command=select_file)
        # Label(frame2, text = "Output folder: ", fg = "black", font= "none 12 bold")
        # folder_button = Button(frame2,text='Browse a Folder',command=select_folder)
  
        # for widget in frame2.winfo_children():
        #     widget.pack(side=LEFT,padx=5, pady=5)

        frame3 = Frame(window)
        frame3.pack(side=TOP)
        submit = Button(frame3, text = 'Submit', width = 30,command=threading)
        ChangeMenu = Button(frame3, text = "Animate and the Edit Results: ",width = 30,command=self.EditBvh)
        ToolTip(widget = ChangeMenu, text = "Animation and a BVH Editor Tool")
        #ChangeMenu.config(state="disabled")
        for widget in frame3.winfo_children():
            widget.pack(side=LEFT,padx=15, pady=15)

        frame4 = Frame(window)
        frame4.pack(side=TOP)

        label = Label(frame4, text = "Terminal: ", fg = "black", font= "none 12 bold")
        label.pack(side=LEFT,padx=15, pady=15)
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