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




class messageFrame(tk.Frame):
    def __init__(self, parent, command=None):
        super().__init__(parent)


        #parent reference
        self.parent = parent
        self.command = command

        #creating widget definitions
        self.messageView = scrollListBox(self)
        self.entryBox = tk.Entry(self)
        self.enterButton = tk.Button(self, text="enter", command=self.update)

        #defining attributes

        #set bindings and events


        #packing widgets
        self.messageView.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.entryBox.pack(fill=tk.X, expand=1, side=tk.LEFT )
        self.enterButton.pack(side=tk.RIGHT)
    


class application(tk.Tk):
    def __init__(self):
        super().__init__()

        #defining variables
        self.active_client

        #creating widget definitions
        self.splitPane = tk.PanedWindow(self, handlepad=16, showhandle=True)
        self.pane1_contacts = scrollListBox(self).listbox.bind("<Button-1>", func=self.cange_connection)
        self.pane2_messages = messageFrame(self)

        self.splitPane.add(self.pane1_contacts)
        self.splitPane.add(self.pane2_messages)

        #packing widgets
        self.splitPane.pack(fill=tk.BOTH,expand=1)

        #create handler threads
        self.connections = th.Thread(target=self.connection_handler)
        self.sync = th.Thread(target=self.server_sync)

        #creating bindings to functions

        tk.mainloop()

    #binding fumctions
    def send_message(self):
        self.pane2_messages.messageView.listbox.insert(tk.END, )

    def change_active_client(self):
        pass

    #thread functions
    def connection_handler(self):
        sock = s.socket()
        sock.listen(5)

        

    def server_sync(self):
        t.sleep(1)


        

a = application()