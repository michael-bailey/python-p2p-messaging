import threading as th
import tkinter as tk
import socket as s
import json as js
import time as t
import sys
import os

DEBUG = 0

"""
------------notes------------
    - think about Network address translation
    - could use pyqt5

    @server
    - using a hybrid model of a peer to peer network with the help of a server
        to handle user infomation : ip address, userName, user iD 
        no data is saved permenently on the server
    - protocol for this is sent in plain text with 
        null bytes seperating each part of the message
        structure of a transmission follows
        userName


    @client
    - data is sent in a plain text format 
        with null bytes seperating the parts of the message
        structure of a message follows


"""

# creating a composite widget that 
# adds a scroll bar to the list widget
# this enables: 
#  - scrolling down chat messages
#  - scrolling down active clients
#  - scrolling down servers
class scrollListBox(tk.Frame):
    def __init__(self, parent, on_click=None):
        super().__init__(parent)

        self.on_click = on_click

        #creating widget definitions
        self.listbox = tk.Listbox(self)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        #set bindings and events
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        #packing widgets
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def insert(self, item):
        self.listbox.insert(tk.END, item)

    def clear(self):
        self.listbox.delete(0, tk.END)
    
    def scrollYSet(value):
        self.scrollbar.set(tk.END)

# this implements the classic file edit menu bar 
# found at the top of many applications this 
# will be used to add a exit button 
# and other features in the future
class menuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        #making file menu
        self.fileMenu = tk.Menu(self, tearoff=0)
        self.fileMenu.add_command(label="exit", command=sys.exit)
        self.add_cascade(label="file", menu=self.fileMenu)

# this is a compound class that displays messages 
# sent to and from a person and handles messages to be sent to a person
class messageFrame(tk.Frame):
    def __init__(self, parent, send_command=None):
        super().__init__(parent)

        #variables

        #creating widget definitions
        self.listbox = scrollListBox(self)
        self.entryBox = tk.Entry(self)
        self.enterButton = tk.Button(self, text="enter", command=send_command)

        #defining bindings

        #packing widgets
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.entryBox.pack(fill=tk.X, expand=1, side=tk.LEFT )
        self.enterButton.pack(side=tk.RIGHT)

        #defining command functions

    def entry_get(self):
        return self.entryBox.get()

    def list_get(self):
        #return self.listbox.
        pass

    def list_insert(self, text):
        self.listbox.insert(text)
    
    def list_update(self):
        pass
    
    def setYScroll():
        pass
# simple window to display any errors that may occur
class errorWindow(tk.Toplevel):
    def __init__(self, master = None, message="no error message"):
            super().__init__(master)
            tk.Label(self, Text=message).pack()

class application(tk.Tk):
    def __init__(self):
        super().__init__()

        #defining variables
        self.active_client = None
        self.selected_server = None

        #defining menu bars
        self.menubar = menuBar(self)
        self.config(menu=self.menubar)        

        #creating widget definitions
        self.splitPane = tk.PanedWindow(self, handlepad=16, showhandle=True)
        self.pane1_contacts = scrollListBox(self)
        self.pane2_messages = messageFrame(self, send_command=self.send_message)

        #linking widgets together
        self.splitPane.add(self.pane1_contacts)
        self.splitPane.add(self.pane2_messages)

        #packing widgets
        self.splitPane.pack(fill=tk.BOTH,expand=1)

        #create handler threads
        self.connections = th.Thread(target=self.connection_handler)
        self.sync = th.Thread(target=self.server_syncronise)
        
        tk.mainloop()

    # this function sends a message 
    # to the currently selected client 
    # from the client selection pane
    # this is called when the send button
    # is clicked (may add this when the enter button is also pressed) 
    def send_message(self):
        self.pane2_messages.list_insert(self.pane2_messages.entry_get())
        self.pane2_messages.set

    # called when any of the clents in the client selection window is clicked 
    def change_reciever(self):
        pass

    #thread functions
    def connection_handler(self):
        sock = s.socket()
        sock.bind(("",0))
        sock.listen(7)
        
        while True:
            connection_socket, address = sock.accept()
            print(address,"connected")
            # USER_ID:TIME:MESSAGE
            msg = str(connection_socket.recv(1024).decode())
            msg.split("\x00")
            
    def server_syncronise(self):
        print("tick!")
        t.sleep(1)



x = DEBUG
while x == 1:
    eval(input(":>"))
else:
    a = application()