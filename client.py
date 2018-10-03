#!/usr/bin/env python3

# 

import threading as th
import tkinter as tk
import socket as s
import json as js
import time as t
import sys
import os

SERVERPORT = 9000
CLIENTPORT = 9001

SPLITCHAR = '\x00'

LOGINFILE = "login.txt"
PRIMEFILE = "primes.txt"
SERVERFILE = "server.txt"



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

# used for debugging (an evaluation loop)
def debug_console():
    while True:
        t.sleep(0.5)
        try:
            print(eval(input(":>")))
        except e as error:
            print(error.args)

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
        self.listBox = tk.Listbox(self, )
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

# this displays messages to the user 
class messageFrame(tk.Frame):
    def __init__(self, parent, send_command=None):
        super().__init__(parent)

        #creating widget definitions
        self.listBox = scrollListBox(self)
        self.entryBox = tk.Entry(self)
        self.enterButton = tk.Button(self, text="enter", command=send_command)

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

# creates a window to login
class loginBox(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("login")
        
        #create object
        self.userLabel = tk.Label(self, text="username : ")
        self.passwordLabel = tk.Label(self, text="password : ")
        self.usernameInput = tk.Entry(self)
        self.passwordInput = tk.Entry(self, show="*")
        self.enterButton = tk.Button(self,text = "enter", command = self.enter)
        self.exitButton = tk.Button(self,text = "close", command = self.exit)

        # put them on the screen
        self.userLabel.grid(row = 0, column = 0)
        self.passwordLabel.grid(row = 1, column = 0)
        self.usernameInput.grid(row = 0, column = 1)
        self.passwordInput.grid(row = 1, column = 1)
        self.enterButton.grid(row = 2, column = 1)
        self.exitButton.grid(row = 2, column = 0)


        tk.mainloop()

    def enter(self):
        print("pressed") 
        # as this is used for the unique identifier later in the program
        username = self.usernameInput.get()
        password = self.passwordInput.get()

        loginFile = open(LOGINFILE, "w")

        loginFile.write(username + "\n")
        loginFile.write(password + "\n")
        loginFile.close()

        self.destroy()

    def exit(self):
        sys.exit(0)

# the main program
class Program(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("")

        #defining program variables
        self.active_client_uid = ""
        self.active_server = ""
        self.exit = False
        self.changeServer = False
        self.userName = ""
        self.passwd = ""
        self.userID = ""

        self.clients = {}
        self.protocolString = "" + self.userID + SPLITCHAR + self.userName + SPLITCHAR

        # getting user details from a file
        try:
            details_file = open(LOGINFILE, "r")
            details = details_file.readlines()
            self.userName = details[0]
            self.passwd = details[1]
            self.userID = hash(details[0] + details[1])


        #print an error message to describe what happened
        except:
            print("file deleted between the start and the creation of the main program object")

        #defining menu bar
        self.menubar = menuBar(self)
        self.config(menu=self.menubar)        
        #creating widget definitions
        self.paneRoot = tk.PanedWindow(self, handlepad=16, showhandle=True)
        self.paneLeft = tk.PanedWindow(self, showhandle=True, orient=tk.VERTICAL)
        self.paneLeftClients = scrollListBox(self)
        self.paneLeftServers = scrollListBox(self, on_click=self.change_Server)
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
    
    def send_message(self, event):
        print("sending a message")
        pass
        
    # called when any of the clents in the client selection window is clicked 
    def change_client(self, event):
        self.active_server = self.paneLeftServers.get()

    def change_Server(self, event):
        self.active_server = self.paneLeftServers.get()
        self.changeServer = True

    #these functions will be turned into a separate thread that 
    #  this will check for any client connecting
    def connections_Thread(self):
        t.sleep(0.5)
        pass
        """
        ClientSocket = s.socket()
        ClientSocket.bind(("", CLIENTPORT))
        ClientSocket.listen(5)


        while not self.exit:
            
            tmpSocket, address = ClientSocket.accept()
            
            data = tmpsocket.recv(65535).decode().split(SPLITCHAR)

            # update the chat file for the connecting user
            file = open(str(data[1]) + ".txt", "a").append("" + t.strftime("%Y/%m/%d %H:%M") + " " + data)

            # current user is open on the main screen
            if self.active_client = data[1]:
                for i in range(open(data[0]))
        """

    # this gets users from a server
    def server_ping(self):

        servSocket = s.socket()
        currentConnection = ""

        while not self.exit:
            t.sleep(0.5)
            print()
            if currentConnection != self.active_server:
                try:
                    servSocket.send(self.protocolString + SPLITCHAR + "close")
                    servSocket.close()
                    servSocket.connect((self.active_server, SERVERPORT))
                    currentConnection = self.active_server
                except Exception as e:
                    print(e.args)
            


def main():
        # if the login file doesnt exist then open login prompt
    if LOGINFILE not in os.listdir():
        loginWindow = loginBox()
        # wait a second for the file to write
        t.sleep(1)

    P = Program()

if __name__ == "__main__":
    # th.Thread( target = debug_console, daemon=True).start()
    main()