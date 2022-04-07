from tkinter import *
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo
from tkinter import messagebox
window = Tk()
window.title("Tkinter Play Videos in Video Player")
window.geometry("700x450")
window.configure(bg="orange red")
 
 
def open_file(filename):

    global videoplayer
    videoplayer = TkinterVideo(master=window, scaled=True, pre_load=False)
    videoplayer.load(r"{}".format(filename))
    videoplayer.pack(expand=True, fill="both")
    videoplayer.play()
 
 
 
def playAgain():
    videoplayer.play()

 
def Reset(file):

    videoplayer.destroy()
    open_file(file)
 
def PauseVideo():
    videoplayer.pause()
    
 
# center this label
lbl1 = Label(window, text="Tkinter Video Player", bg="orange red",
             fg="white", font="none 24 bold")
lbl1.config(anchor=CENTER)
lbl1.pack()
 
# openbtn = Button(window, text='Open', command=lambda: open_file())
# openbtn.pack(side=TOP, pady=2)
file = "D:\\tuc\\Github\\Thesis\\BVH\\alpha_pose_kunkun_cut_one_second\\3d_pose.mp4" 

playbtn = Button(window, text='Play Video', command=lambda: playAgain())
playbtn.pack(side=TOP, pady=2)
 
stopbtn = Button(window, text='Reset Video', command=lambda: Reset(file))
stopbtn.pack(side=TOP, padx=3)
 
pausebtn = Button(window, text='Pause Video', command=lambda: PauseVideo())
pausebtn.pack(side=TOP, padx=4)
open_file(file)
 
window.mainloop()