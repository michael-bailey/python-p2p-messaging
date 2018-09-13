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
SERVERPORT = 9000
CLIENTPORT = 9001

"""
------------notes------------
    - could use pyqt5 (might be easier than tkinter, also look better)
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
        super().__init__(master, cnf, **kw)

        self.userLabel = tk.Label(self, text="username : ").grid(row = 0, column = 0)
        self.userLabel = tk.Label(self, text="password : ").grid(row = 1, column = 0)
        self.userNameInput = tk.Entry(self).grid(row = 0, column = 1)
        self.passWordInput = tk.Entry(self).grid(row = 1, column = 1)
        self.enterButton = tk.Button(text = "enter", command = self.enter).grid(row = 2, column = 1)
        self.exitButton = tk.Button(text = "close", command = self.exit).grid(row = 2, column = 0)

        tk.mainloop()

    def enter():
        loginfile = open("user.login", "w")

        # encoding them in base 64 to prevent users modifying there 
        # username or password without knowing what they are doing 
        # as this is used for the unique identifyer later in the program
        username = self.userNameInput.get().encode("base64_codec")
        password = self.passWordInput.get().encode("base64_codec")

        loginfile.write(username)
        loginfile.write(password)



        
    def exit(self):
        sys.exit(0)


# the main program
class application(tk.Tk):
    def __init__(self):
        super().__init__()

        #defining global variables
        self.active_client = None
        self.active_server = ""
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
        self.connectionThread = th.Thread(target=self.connections_Thread, daemon=True).start()    
        self.serverPing = th.Thread(target=self.server_ping, daemon=True).start()

        #packing widgets
        self.paneRoot.pack(fill=tk.BOTH,expand=1)
        for i in open("servers.txt").readlines():
            self.paneLeftServers.insert(str(i))

        
        tk.mainloop()

    #this function sends a message
    
    def send_message(self):
        client = self.active_client

        print("selected client is {} and message is"self.clientclient)
        self.server_socket.send("")
        

    # called when any of the clents in the client selection window is clicked 
    def change_client(self):
        pass

    def change_Server(self):
        self.server_socket.send("" + userid)

    def exit_application(self):
        for i in th.enumerate():
            i.join(2)


    # this will recieve data from the server in a non blocking fashion (to not prevent program execution)


    #these functions will be turned into a separate thread that 
    #  this will check for any client connecting
    def connections_Thread(self):
        ClientSocket = 

        while not self.exit:
            print("client is listenening")


    # not acctually a standard ping
    def server_ping(self):
        while not self.exit:
            self.paneLeftClients.clear()
            for i in self.server_socket.recv(65535).decode().split(","):
                self.paneLeftClients.insert(i)


    # signal hadlers (probably not going to use for a while)
    def CTRL_C(self):
        self.exit = True
        sys.exit()

"""
if "user.login" not in os.listdir():
    loginWindow = loginBox()
"""
a = application()


