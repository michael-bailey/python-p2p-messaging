import threading as th
import tkinter as tk
import socket as s
import time as t
import os

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

        self.listbox.bind("<Button-1>", self.update)

        #packing widgets
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #internal functions
    def update(self, event):
        self.state = self.listbox.get(tk.ACTIVE)
        try:
            self.on_click()
        except:
            pass




class messageFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)



        #parent reference
        self.parent = parent

        #creating widget definitions
        self.messageView = scrollListBox(self)
        self.entryBox = tk.Entry(self)
        self.enterButton = tk.Button(self, text="enter")

        #defining attributes

        #set bindings and events


        #packing widgets
        self.messageView.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.entryBox.pack(fill=tk.X, expand=1, side=tk.LEFT )
        self.enterButton.pack(side=tk.RIGHT)


class application(tk.Tk):
    def __init__(self):
        super().__init__()

        #creating widget definitions
        self.splitPane = tk.PanedWindow(self, handlepad=16, showhandle=True)
        self.pane1_contacts = scrollListBox(self)
        self.pane2_messages = messageFrame(self)

        self.splitPane.add(self.pane1_contacts)
        self.splitPane.add(self.pane2_messages)

        #packing widgets
        self.splitPane.pack(fill=tk.BOTH,expand=1)

        #create handler threads
        self.connections = th.Thread(target=self.connection_handler)
        self.sync = th.Thread(target=self.server_sync)

        tk.mainloop()

    def connection_handler(self):
        pass
    def server_sync(self):
        pass


        

a = application()