from tkinter import *
from tkvideo import tkvideo
from tkVideoPlayer import TkinterVideo
# create instance fo window
root = Tk()
# set window title
root.title('Video Player')
# create label
video_label = Label(root)
video_label.pack()
# read video to display on label
player = TkinterVideo("D:\\tuc\\Github\\Thesis\\BVH\\kunkun_cut_one_second\\3d_pose.mp4", video_label, size = (700, 500))
player.play()
root.mainloop()