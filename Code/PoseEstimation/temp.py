#Import tkinter package
import tkinter as tk
#Define a window name
root1 = tk.Tk()
text_variable = tk.DoubleVar()
#declare the spinbox widget by assigning values to from_, to and increment
spin_box = tk.Spinbox(
    root1,
    from_=1.01,
    to=50.00,
    increment=1.01,
    textvariable=text_variable
)
#To show the content in the window
spin_box.pack()
root1.mainloop()