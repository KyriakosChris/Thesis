
from tkinter import *
from PIL import Image, ImageTk
from threading import *
import imageio
# create instance for window
root = Tk()
# set window title
root.title('Video Player')
# read video
video = imageio.get_reader("D:\\tuc\\Github\\Thesis\BVH\\alpha_pose_kunkun_cut_one_second\\3d_pose.mp4")


def display_video(label):
   # iterate through video data
   for image in video.iter_data():
      # convert array into image
      img = Image.fromarray(image)
      # Convert image to PhotoImage
      image_frame = ImageTk.PhotoImage(image = img)
      # configure video to the lable
      label.config(image=image_frame)
      label.image = image_frame
# create label for video
video_label = Label(root)
video_label.pack()
# create and start threadY

submit = Button(root, text = 'Submit', width = 30,command=display_video(video_label))
submit.pack()
root.mainloop()