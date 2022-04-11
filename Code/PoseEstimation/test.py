#Importing the tkinter library
from tkinter import *
win= Tk()
win.title("Dynamically Resize Buttons")
win.geometry("700x500")

#Configure Rows and column

Grid.rowconfigure(win, 0,weight=1)
Grid.columnconfigure(win,0,weight=1)
#Create buttons

b1= Button(win, text= "C++")
b2= Button(win, text= "Java")

#Create List of buttons
bl= [b1, b2]

row_no=0
#Loop through all the buttons and configure it row-wise
for button in bl:
   Grid.rowconfigure(win,row_no, weight=1)
   row_no+=1

#Adjust the position in grid and make them sticky

b1.grid(row=0, column=0, sticky= "nsew")
b2.grid(row=1, column=0, stick= "nsew")

win.mainloop()