import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


def select_files(prod_type):
    path = f"/home/sam/Pictures/Test/{prod_type}"
    filetypes = (
        ('PDF Files', '*.pdf'),
    )

    filenames = fd.askopenfilenames(
        title='Open files',
        initialdir=path,
        filetypes=filetypes)

    for file in filenames:
        print(file)


class InputFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.__create_widgets()

    def __create_widgets(self):
        # Product
        ttk.Label(self, text='Product:').grid(column=0, row=0, sticky=tk.W)
        self.product_type = tk.StringVar()
        self.product_combo = ttk.Combobox(self, width=30, textvariable=self.product_type)
        self.product_combo['values'] = ('Notepad', 'Flat Notecard', 'Folded Notecard', 'Journal')
        self.product_combo.set('Notepad')
        self.product_combo['state'] = 'readonly'
        self.product_combo.grid(column=1, row=0, sticky=tk.W)

        # Algorithm:
        ttk.Label(self, text='Algorithm:').grid(column=0, row=1, sticky=tk.W)
        algo_var = tk.StringVar()
        algo_combo = ttk.Combobox(self, width=30)
        algo_combo['values'] = ('panel', 'fuzzy')
        algo_combo.set('panel')
        algo_combo.grid(column=1, row=1, sticky=tk.W)

        # Orientation:
        ttk.Label(self, text='Orientation:').grid(column=0, row=2, sticky=tk.W)
        orientation_var = tk.StringVar()
        orientation_combo = ttk.Combobox(self, width=30, textvariable=orientation_var)
        orientation_combo['values'] = ('auto', 'portrait', 'landscape')
        orientation_combo.set('auto')
        orientation_combo.grid(column=1, row=2, sticky=tk.W)

        # Margin:
        ttk.Label(self, text='Margin:').grid(column=0, row=3, sticky=tk.W)
        margin = ttk.Entry(self, width=30)
        margin.grid(column=1, row=3, sticky=tk.W)

        # Gap:
        ttk.Label(self, text='Gap:').grid(column=0, row=4, sticky=tk.W)
        gap = ttk.Entry(self, width=30)
        gap.grid(column=1, row=4, sticky=tk.W)

        # Repeat:
        ttk.Label(self, text='Repeat:').grid(column=0, row=5, sticky=tk.W)
        repeat_number = tk.IntVar()
        repeat = ttk.Spinbox(self, from_=1, to=10, width=30, textvariable=repeat_number)
        repeat.set(1)
        repeat.grid(column=1, row=5, sticky=tk.W)

        for widget in self.winfo_children():
            widget.grid(padx=0, pady=5)


class ButtonFrame(ttk.Frame):
    def __init__(self, parent, product_type): ### EDITED THIS LINE
        super().__init__(parent)
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)

        self.product_type = product_type ### ADDED THIS LINE

        self.__create_widgets()

    def __create_widgets(self):
        ttk.Button(self, text='Select Files', command=self.on_go_pressed).grid(column=0, row=0)
        ttk.Button(self, text='Generate PDF').grid(column=0, row=1)

        for widget in self.winfo_children():
            widget.grid(padx=0, pady=3)

    def on_go_pressed(self):
        select_files(self.product_type.get()) ### EDITED THIS LINE


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF n-up")
        self.eval('tk::PlaceWindow . center')
        self.geometry('400x200')
        self.resizable(0, 0)
        # self.attributes('-toolwindow', True)

        # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        # create the input frame
        input_frame = InputFrame(self)
        input_frame.grid(column=0, row=0)

        # create the button frame
        button_frame = ButtonFrame(self, input_frame.product_type) ### EDITED THIS LINE
        button_frame.grid(column=1, row=0)


if __name__ == '__main__':
    app = App()
    app.mainloop()