import tkinter as tk

root = tk.Tk()
test = tk.Label(root, text="Red", bg="red", fg="white")
test.pack(ipadx=30, ipady=6)
test = tk.Label(root, text="Purple", bg="purple", fg="white")
test.pack(ipadx=8, ipady=12)
tk.mainloop()