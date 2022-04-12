# change the frame size by changing content.  padding, whatever. 
# Perhaps this stackoverflow exchange is what you need. 
# https://stackoverflow.com/questions/4399180/how-to-set-the-min-and-max-height-or-width-of-a-frame 
 
import time 
import tkinter 
 
root = tkinter.Tk() 
root.geometry('400x300') 
root.title('expanding frame') 
 
frame_size_label = tkinter.Label(root, text = 'frame size WxH', relief = tkinter.SUNKEN, background = 'orange') 
frame_size_label.pack(anchor = tkinter.SE) 
 
canvas = tkinter.Canvas(root) 
canvas.pack() 
 
expanding_frame = tkinter.Frame(canvas) 
 
canvas.create_window(0,0,window=expanding_frame, anchor='nw') 
 
for i in range(8): 
    # pack additional labels into the frame in the canvas in the toplevel. 
    tkinter.Label(expanding_frame, text='sleep {}'.format(i), font = ('fixed', 2 * (i + 4))).pack() 
    # update the root 
    root.update() 
    # and report, getting frame size from winfo routines. 
    frame_size_label.configure(text = 'frame size {}x{}'.format(expanding_frame.winfo_width(), expanding_frame.winfo_height())) 
    print('{}x{}'.format(expanding_frame.winfo_width(), expanding_frame.winfo_height())) 
    root.update() 
    #time.sleep(i) 
 
 
root.mainloop() 