from  tkinter import *

root = Tk()
root.withdraw()

current_window = None

def first(): 
    
    window = replace_window(root)
    #setting tkinter window size
    window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
    btn = Button(window, text = "first",width = 30, command = second)  
    btn.place(x=0, y=290)  
    window.wm_protocol("WM_DELETE_WINDOW", root.destroy)
def second():
    window = replace_window(root)
    #setting tkinter window size
    window.geometry("%dx%d+-8+0" % (window.winfo_screenwidth() , window.winfo_screenheight()))
    btn = Button(window, text = "second",width = 30, command = first)
    btn.place(x=0, y=290)  
    window.wm_protocol("WM_DELETE_WINDOW", root.destroy)   
def  replace_window(root):
    """Destroy current window, create new window"""
    global current_window
    if current_window is not None:
        current_window.destroy()
    current_window = Toplevel(root)

    # if the user kills the window via the window manager,
    # exit the application. 

    return current_window


window = first()

root.mainloop() 



