import tkinter as tk


class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text

        def enter(event):
            self.showTooltip()
        def leave(event):
            self.hideTooltip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def showTooltip(self):
        self.tooltipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1) # window without border and no normal means of closing
        tw.wm_geometry("+{}+{}".format(self.widget.winfo_rootx(), self.widget.winfo_rooty()))
        label = tk.Label(tw, text = self.text, background = "#ffffff", relief = 'solid', borderwidth = 2).pack()

    def hideTooltip(self):
        tw = self.tooltipwindow
        tw.destroy()
        self.tooltipwindow = None
root = tk.Tk() 

your_widget = tk.Button(root, text = "Hover me!")
your_widget.pack()
ToolTip(widget = your_widget, text = "Hover text!")

root.mainloop()