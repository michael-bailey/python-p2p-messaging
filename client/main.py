import socket as s
import threading as th
import tkinter as tk
import os
import time as t

"""
------------notes------------
    - think about Network address translation

"""



#creating a composite widget that combines the list box and a scroll bar
class scrollListBox(Frame):
    def __init__(self, parent):
        super().__init__(parent, on_click=None)

        #create widgets
        self.listbox = tk.Listbox(self)
        self.scrollbar = tk.Scrollbar(self, orient=VERTICAL)

        #set up scrolling
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        #set bindings
        self.listbox.bind("<Button-1>", on_click, args=)

        #pack the widgets into the frame !--not the root--!
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        def update(self):
            self.state = self.listbox.get()


class messageFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #creating widget definitions
        self.messageView = scrollListBox(self)
        self.entryBox = tk.Entry(self)
        self.enterButton = tk.Button(self)

        #defining attributes

        #setting bindings

        #packing widgets


class application(tk.Tk):
    def __init__(self):
        super().__init__():

        self.splitPane = tk.PanedWindow(self)
        self.

        

