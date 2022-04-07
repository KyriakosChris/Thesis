from tkinter import *  
  
root = Tk()  
  
root.geometry("200x200")  
  
def open():  
    #top = Toplevel(root)  
    root.geometry("300x200")  
  
    labelframe1 = LabelFrame(root, text="Positive Comments")  
    labelframe1.pack(fill="both", expand="yes")  
    
    toplabel = Label(labelframe1, text="Place to put the positive comments")  
    toplabel.pack()  
    
    labelframe2 = LabelFrame(root, text = "Negative Comments")  
    labelframe2.pack(fill="both", expand = "yes")  
    
    bottomlabel = Label(labelframe2,text = "Place to put the negative comments")  
    bottomlabel.pack()  
    root.mainloop()  
  
btn = Button(root, text = "open", command = open)  
  
btn.place(x=75,y=50)  
  
root.mainloop()  