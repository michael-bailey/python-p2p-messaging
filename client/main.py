import threading as th
import tkinter as tk
import socket as s
import json as js
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

        #creating widget definitions
        self.listbox = tk.Listbox(self)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        #set bindings and events
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        #packing widgets
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

class messageFrame(tk.Frame):
    def __init__(self, parent, command=None, on_click=None):
        super().__init__(parent)


        #parent reference
        self.ArgCommand = command
        self.ArgOn_click = on_click

        #creating widget definitions
        self.messageView = scrollListBox(self, on_click=self.on_click)
        self.entryBox = tk.Entry(self)
        self.enterButton = tk.Button(self, text="enter", command=self.update)

        #defining bindings
        self.entryBox.bind("<Key>", self.command)


        #packing widgets
        self.messageView.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.entryBox.pack(fill=tk.X, expand=1, side=tk.LEFT )
        self.enterButton.pack(side=tk.RIGHT)

        #defining command functions
    def command(self, event=None):
        if event == None:
            try:
                self.ArgCommand()
            except:
                print("ArgCommand failed")
                pass
        else:
            if event.char === "\n":
                self.ArgCommand()
    
    def on_click(self):
        try:
            self.ArgOn_click()
        except:
            print("ArgCommand failed")
            pass
    
class serverSelectWindow(tk.Toplevel):
    def __init__(self, on_click=None):
        super().__init__()
        self.selector = scrollListBox(self)

        self.ArgOn_click = on_click
    
    def on_click(self):
        try:
            self.ArgOn_click()
        except:
            print("click failed")
            pass

class application(tk.Tk):
    def __init__(self):
        super().__init__()

        #defining variables
        self.active_client = 0
        self.client_details = {}

        #defining other toplevel widgets
        self.server_selector = serverSelectWindow()

        #creating widget definitions
        self.splitPane = tk.PanedWindow(self, handlepad=16, showhandle=True)
        self.pane1_contacts = scrollListBox(self)
        self.pane2_messages = messageFrame(self)
        #linking widgets together
        self.splitPane.add(self.pane1_contacts)
        self.splitPane.add(self.pane2_messages)

        #setting up bindings


        #packing widgets
        self.splitPane.pack(fill=tk.BOTH,expand=1)

        #create handler threads
        self.connections = th.Thread(target=self.connection_handler)
        self.sync = th.Thread(target=self.server_sync)
        
        tk.mainloop()

    #binding fumctions
    def send_message(self):

        

        self.pane2_messages.messageView.listbox.insert(tk.END, self.pane2_messages.entryBox.get())

    def change_active_client(self):
        pass

    #thread functions
    def connection_handler(self):
        sock = s.socket()
        sock.listen(5)

        sock.accept()

    def server_sync(self):


        t.sleep(1)


a = application()