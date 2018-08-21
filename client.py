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
    - could use pyqt5 (might be eiser than tkinter, also look better)
    - think of way of implementing multiple messageing service (MMS)


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

    # inserts an item onto the list
    def insert(self, item):
        self.listbox.insert(tk.END, item)

    # clears all items of the list
    def clear(self):
        self.listbox.delete(0, tk.END)
    
    # moves the list box to the bottom
    def scrollToBottom(self):
        self.listbox.yview_scroll(tk.END, tk.UNITS)
    
    # returns the currently selected element
    def get(self):
        return self.listbox.get(tk.ACTIVE)

# this implements the classic file menu bar 
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

    # returns the contents of the entry box 
    def entry_get(self):
        return self.entryBox.get()
        pass

    # inherited from the scroll listbox
    # changed the name to be easy to identify
    def list_get(self):
        return self.listbox.get()
        pass

    # inherited from the scroll listbox
    # changed the name to be easy to identify
    def list_insert(self, text):
        self.listbox.insert(text)
    
    # inherited from the scroll listbox
    # changed the name to be easy to identify
    def scrollToBottom(self):
        self.listbox.scrollToBottom()

# simple window to display any errors that may occur
# it will be called when an error occurs 
class errorWindow(tk.Toplevel):
    def __init__(self, master = None, message="no error message"):
            super().__init__(master)
            tk.Label(self, Text=message).pack()

class application(tk.Tk):




    
    def __init__(self):
        super().__init__()

        #defining global variables
        self.active_client = None
        self.selected_server = None

        #defining menu bar
        self.menubar = menuBar(self)
        self.config(menu=self.menubar)        

        #creating widget definitions
        self.splitPane = tk.PanedWindow(self, handlepad=16, showhandle=True)
        self.pane1Selection = tk.PanedWindow(self, showhandle=True, orient=tk.VERTICAL)
        self.pane1Clients = scrollListBox(self)
        self.pane1Servers = scrollListBox(self)
        self.pane2Messages = messageFrame(self, send_command=self.send_message)

        #linking widgets together
        self.pane1Selection.add(self.pane1Clients)
        self.pane1Selection.add(self.pane1Servers)

        self.splitPane.add(self.pane1Selection)
        self.splitPane.add(self.pane2Messages)

        #packing widgets
        self.splitPane.pack(fill=tk.BOTH,expand=1)

        #create handler threads
        self.connections = th.Thread(target=self.connection_handler).start()
        self.sync = th.Thread(target=self.server_syncronise).start()

        for i in open("servers.txt").readlines():
            self.pane1Servers.insert(str(i))

        
        tk.mainloop()

    # this function sends a message 
    # to the currently selected client 
    # from the client selection pane
    # this is called when the send button
    # is clicked (may add this when the enter button is also pressed) 
    def send_message(self):
        self.pane2Messages.list_insert(self.pane2Messages.entry_get())
        self.pane2Messages.scrollToBottom()

    # called when any of the clents in the client selection window is clicked 
    def change_reciever(self):
        pass

    #this functions will be turned into a separate thread that 
    #  - will listen for any incoming connections 
    #  - allow them to connect 
    #  - recieve data that is to be sent
    #  - and then close the connection
    #
    # any data sent through will be parsed and saved to files and if needed will display it to the list box
    def connection_handler(self):
        sock = s.socket()
        sock.bind(("",0))
        sock.listen(7)

        #whole code is in a repetative loop so if any error occurs the thread wonnt break 
        while True:
            try:
                connection_socket, address = sock.accept()
                print(address,"connected")
                # USER_ID \x00 TIME\x00 MESSAGE
                # turns 
                msg = str(connection_socket.recv(1024).decode())
                msg.split("\x00")

                # main decoding logic is here


            except Exception as e:
                        # display error window
                        errorWindow(e)

        
    def server_syncronise(self):
        server_socket = s.socket()

        while True:
            if self.pane1Servers.get() == '' or self.pane1Servers.get() == None:
                try:
                    IP = self.pane1Servers.get()

                    server_socket.connect((IP,0))

                    while IP == self.pane1Servers.get():
                        server_socket.recv(65536)

                        self.pane1Clients.clear()


                except Exception as e:
                    errorWindow(e)
            
# this is to debug diffrent classes to see how they 
# look in a window or to easily find errors

x = DEBUG
while x == 1:
    window = tk.Tk()
    eval(input("object window created\n:>"))
else:
    a = application()