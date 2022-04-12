from tkinter import *
from tkVideoPlayer import TkinterVideo
import os
from PIL import Image,ImageTk
from tkinter import filedialog as fd
from tkVideoPlayer import TkinterVideo
from BVHsmoother.smooth import smooth

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
        geeky_file = open(file, 'wt')
        for line in Edited:
                geeky_file.write(str(line))
        geeky_file.close()
    except:
        print("Unable to write to file")
            

def Tkinder(self):

    def click():
        if is_float(Xinput.get()) and is_float(Yinput.get()) and is_float(Zinput.get()) and self.file_name != '' and self.folder_name != '':
            X = float(Xinput.get())
            Y = float(Yinput.get())
            Z = float(Zinput.get())
            print(Xinput.get(),Yinput.get(),Zinput.get())
            print(self.file_name)
            print(self.folder_name)
            self.positions = (X,Y,Z)
            self.PositionEdit()

    def is_float(element):
        try:
            float(element)
            return True
        except ValueError:
            return False

    def open_file(filename):

        global videoplayer
        videoplayer = TkinterVideo(master=window, scaled=True, pre_load=False)
        videoplayer.load(r"{}".format(filename))
        videoplayer.place(x=0, y=600, height=400, width=700)
        videoplayer.play()



    def playAgain():
        videoplayer.play()

    
    def Reset(file):

        videoplayer.destroy()
        open_file(file)

    def PauseVideo():
        videoplayer.pause()

    # create a tkinter window
    window = Tk()
    file = "D:\\tuc\\Github\\Thesis\\BVH\\alpha_pose_kunkun_cut_one_second\\3d_pose.mp4"        
    window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
    window.title("BVH Editor")
    logo_img = Image.open("TUC.gif")
    logo_img.resize((window.winfo_screenwidth(), window.winfo_screenheight()),Image.ANTIALIAS)
    logo_img = ImageTk.PhotoImage(logo_img, master = window)
    #photo = PhotoImage(file = "TUC.gif")
    tuc = Label(window, image = logo_img)
    tuc.place(x=-2, y=-2)
    # photo = PhotoImage(file = "TUC.gif")
    # tuc = Label(window, image = photo)
    # tuc.place(x=-2, y=-2)
    
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
    # center this label
    lbl1 = Label(window, text="Tkinter Video Player", font="none 24 bold")
    lbl1.place(x=0, y=450)
    file = "D:\\tuc\\Github\\Thesis\\BVH\\alpha_pose_kunkun_cut_one_second\\3d_pose.mp4" 
    openbtn = Button(window, text='Open Video', command=lambda: open_file(file))
    openbtn.place(x=10, y=550)

    playbtn = Button(window, text='Play Video', command=lambda: playAgain())
    playbtn.place(x=110, y=550)
    
    stopbtn = Button(window, text='Reset Video', command=lambda: Reset(file))
    stopbtn.place(x=210, y=550)
    
    pausebtn = Button(window, text='Pause Video', command=lambda: PauseVideo())
    pausebtn.place(x=310, y=550)
    
    window.mainloop()

# file = "D:\\tuc\\Github\\Thesis\\BVH\\kunkun_cut_one_second\\kunkun_cut_one_second.bvh"
# PositionEdit(file,(5,3,7))



