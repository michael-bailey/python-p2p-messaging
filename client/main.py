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
class scrollListBox(tk.Frame):
    def __init__(self, parent, on_click=None):
        super().__init__(parent)

        #parent object reference's
        self.parent = parent
        self.on_click = on_click

        #creating widget definitions
        self.listbox = tk.Listbox(self)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        #defining attributes

        #set bindings and events
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("<Button-1>", on_click)

        #packing widgets
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #internal functions
        def update(self):
            self.state = self.listbox.get()
            self.on_click()



class messageFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #parent reference
        self.parent = parent

        #creating widget definitions
        self.messageView = scrollListBox(self)
        self.entryBox = tk.Entry(self)
        self.enterButton = tk.Button(self)

        #defining attributes

        #set bindings and events

        #packing widgets

"""
class application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.splitPane = tk.PanedWindow(self)
        self.
"""
        

