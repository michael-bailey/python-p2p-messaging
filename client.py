#!/usr/bin/env python3

import threading as th
import signal as sig
import tkinter as tk
import socket as s
import json as js
import time as t
import sys
import os

DEBUG = False

"""
------------notes------------
    - could use pyqt5 (might be eiser than tkinter, also look better)
    - think of way of implementing multiple messageing service (MMS)
    - connections will be using the udp protocol


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


    $classes
    - scrollListBox
        properties:
            listBox : tk.Listbox
            scrollBar : tk.scrollbar
        methods:
            getActive
            Insert
            Clear
        events:
            onClick
            onDoubleClick

    - messageFrame
        properties
            listBox : scrollListBox
            entryBox : tk.Entry
            enterButton : tk.Button
        methods:
            entry_get
            listInsert
            listClear
            getActive
        events:
            onButtonClick

    
    - menuBar
        properties:
            fileMenu : tk.menu
        methods:
        events:
            exitClicked
        

    - application
        properties:
            paneRoot
            paneLeft
            PaneLeftClient
            paneLeftServer
            PaneRootMessages
            MenuBar

            activeClient
            activeServer
        methods:
            sendMessage
            connectionsThread

            



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
        self.listBox = tk.Listbox(self)
        self.scrollBar = tk.Scrollbar(self, orient=tk.VERTICAL)

        #set bindings and events for the scroll bar so contents scroll
        self.listBox.config(yscrollcommand=self.scrollBar.set)
        self.scrollBar.config(command=self.listBox.yview)

        #packing widgets
        self.listBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    # inserts an item onto the list
    def insert(self, item):
        self.listBox.insert(tk.END, item)

    # clears all items of the list
    def clear(self):
        self.listBox.delete(0, tk.END)
    
    # returns the currently selected element
    def get(self):
        return self.listBox.get(tk.ACTIVE)

# this implements the classic file menu bar 
# found at the top of many applications this 
# will be used to add a exit butto
# and other features in the future
class menuBar(tk.Menu):
    def __init__(self, parent, exitClicked=sys.exit):
        super().__init__(parent)
        #making file menu
        self.fileMenu = tk.Menu(self, tearoff=0)
        self.fileMenu.add_command(label="exit", command=exitClicked())
        self.add_cascade(label="file", menu=self.fileMenu)

# this is a compound class that displays messages 
# sent to and from a person and handles messages to be sent to a person
class messageFrame(tk.Frame):
    def __init__(self, parent, send_command=None):
        super().__init__(parent)

        #creating widget definitions
        self.listBox = scrollListBox(self)
        self.entryBox = tk.Entry(self)
        self.enterButton = tk.Button(self, text="enter", command=send_command)

        #defining bindings

        #packing widgets
        self.listBox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.entryBox.pack(fill=tk.X, expand=1, side=tk.LEFT )
        self.enterButton.pack(side=tk.RIGHT)

    # returns the contents of the entry box 
    def entry_get(self):
        return self.entryBox.get()
        pass

    # inherited from the scroll listbox
    # changed the name to be easy to identify
    def list_get(self):
        return self.listBox.get()
        pass

    # inherited from the scroll listbox
    # changed the name to be easy to identify
    def list_insert(self, text):
        self.listBox.insert(text)
    
    # inherited from the scroll listbox
    # changed the name to be easy to identify
    def reset_Scroll(self):
        self.listBox.reset_Scroll()

# simple window to display any errors that may occur
# it will be called when an error occurs 
class errorWindow(tk.Toplevel):
    def __init__(self, master = None, message="no error message"):
            super().__init__(master)
            tk.Label(self, Text=message).pack()

# the main program
class application(tk.Tk):
    def __init__(self):
        super().__init__()

        #defining global variables
        self.active_client = None
        self.active_server = None
        self.exit = False

        #defining menu bar
        self.menubar = menuBar(self)
        self.config(menu=self.menubar)        

        #creating widget definitions
        self.paneRoot = tk.PanedWindow(self, handlepad=16, showhandle=True)
        self.paneLeft = tk.PanedWindow(self, showhandle=True, orient=tk.VERTICAL)
        self.paneLeftClients = scrollListBox(self)
        self.paneLeftServers = scrollListBox(self)
        self.PaneRootMessages = messageFrame(self, send_command=self.send_message)

        #linking widgets together
        self.paneLeft.add(self.paneLeftClients)
        self.paneLeft.add(self.paneLeftServers)
        self.paneRoot.add(self.paneLeft)
        self.paneRoot.add(self.PaneRootMessages)

        #packing widgets
        self.paneRoot.pack(fill=tk.BOTH,expand=1)

        #create handler threads
        #self.connections = th.Thread(target=self.connection_handler).start()  not in use causes the gui to lag when trying to recieve data from th sever due to wait times
        self.thread = th.Thread(target=self.connections_Thread).start()    

        for i in open("servers.txt").readlines():
            self.paneLeftServers.insert(str(i))

        
        tk.mainloop()

    # this function sends a message 
    # to the currently selected client 
    # from the client selection pane
    # it sends a message to the server to collect user conention info
    # it then send a message to the collected address
    def send_message(self):
        if True:
            self.PaneRootMessages.list_insert(self.PaneRootMessages.entry_get())
            self.PaneRootMessages.reset_Scroll()

    # called when any of the clents in the client selection window is clicked 
    def change_reciever(self):
        pass

    def change_Server(self):
        pass

    #this functions will be turned into a separate thread that 
    #  - will listen for any incoming connections 
    #  - allow them to connect 
    #  - recieve data that is to be sent
    #  - and then close the connection
    #
    # any data sent through will be parsed and saved to files and if needed will display it to the list box
    def connections_Thread(self):
        while not self.exit:

            if self.paneLeftServers.get() != "":
                print(self.paneLeftServers.get().strip("\n"))

    # signal handlers
    def CTRL_C(self):
        self.exit()

if DEBUG == True:
    while True:
        try:
            exec(input(":>"))                
        except Exception as e:
            print(e)
else:
    a = application()