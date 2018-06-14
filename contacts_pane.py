import tkinter as tk

#from ../custom.py import *

class messages(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(master)

        mBox = tk.Listbox(self)
        mbox.pack()
        #enterBox = entry(self)
        #enterBox.pack()

        self.Add()

root = tk.Tk()

m = messages(root)
