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
    - could use pyqt5 (might be easier than tkinter, also look better)
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
        self.fileMenu.add_command(label="exit", command=exitClicked)
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
        

    # inherited from the scroll listbox
    # changed the name to be easy to identify
    def list_get(self):
        return self.listBox.get()
        

    # inherited from the scroll listbox
    # changed the name to be easy to identify
    def list_insert(self, text):
        self.listBox.insert(text)
    
    # inherited from the scroll listbox
    # changed the name to be easy to identify



class loginBox(tk.Toplevel):
    def __init__(self, master = None, cnf = {}, **kw):
            return super().__init__(master, cnf, **kw)

            self.userLabel = tk.Label(self, text="username : ").grid(0,0)
            self.userLabel = tk.Label(self, text="username : ").grid(0,0)



# the main program
class application(tk.Tk):
    def __init__(self):
        super().__init__()

        #defining global variables
        self.active_client = None
        self.active_server = "127.0.0.1"
        self.exit = False
        self.contact_list = []

        # creating user details.
        try:
            details_file = open("user.login", "r")
        #print an error message to describe what happened
        except:
            print("file deleted between the start and the creation of the main program object")

        self.server_socket = s.socket()
        self.server_socket.setblocking(0)

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


        #create handler threads
        self.thread = th.Thread(target=self.connections_Thread).start()    

        #packing widgets
        self.paneRoot.pack(fill=tk.BOTH,expand=1)
        for i in open("servers.txt").readlines():
            self.paneLeftServers.insert(str(i))

        
        tk.mainloop()

    #this function sends a message
    
    def send_message(self):
        client = self.PaneRootMessages.entry_get()

        self.server_socket.send("")
        

    # called when any of the clents in the client selection window is clicked 
    def change_client(self):
        

    def change_Server(self):
        self.server_socket.send("" + )

    def exit_application(self):
        for i in th.enumerate():
            i.join(2)


    # this will recieve data from the server in a non blocking fashion (to not prevent program execution)

    def server_sync(self):
        while true:
            try:
                with th.Lock() as lock:
                    # try recieveing data fron the server (will error if there is no data)
                    self.contact_list = self.server_socket.recv(65535).split(",")
            
            # no data or another error occured
            except:
                print("error occured")
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

        print("connection thread exiting...")

    # signal handlers
    def CTRL_C(self):
        self.exit = True
        sys.exit()


if "user.login" not in os.listdir():
    loginWindow = loginBox()

a = application()


