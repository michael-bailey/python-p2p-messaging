#!/usr/bin/env python3

import threading as th
import tkinter as tk
import socket as s
import json as js
import time as t
import sys
import os

SERVERPORT = 9000
CLIENTPORT = 9001
BUFFERSIZE = 65535
BINDADDRESS = "0.0.0.0"
SPLITCHAR = '`'
LOGINFILE = "login.txt"
PRIMEFILE = "primes.txt"
SERVERFILE = "servers.txt"
SOCKETENCODING = "ascii"

"""
------------notes------------
    - could use pyqt5 (might be easier than tkinter, also look better)
    - think of way of implementing multiple messageing service (MMS)


    @server
    - using a hybrid model of a peer to peer network with the help of a server
        to handle user infomation : ip address, userName, user iD 
        no data is saved permenently on the server
    - protocol for this is sent in plain text with 
        grave chars seperating each part of the message
        json is sent back to the client every second 
        containing UIDs usernames and ip addresses

    @client
    - data is sent in a plain text format 
        with grave characters seperating the parts of the message
        structure of a message follows

    $Variables
    - SERVERPORT
    - CLIENTPORT
    - PRIMEFILE
    - SERVERfILE
    - LOGINFILE
    - SPLITCHAR

    $classes
    - scrollListBox
        properties:
            listBox : tk.Listbox
            scrollBar : tk.scrollbar
        methods:
            __init__
            get
            insert
            clear
        events:
            onClick

    - messageFrame
        properties
            listBox : scrollListBox
            entryBox : tk.Entry
            enterButton : tk.Button
        methods:
            __init__
            entry_get
            list_Insert
            listClear
            getActive
        events:
            onButtonClick

    - menuBar
        properties:
            fileMenu : tk.menu
        methods:
            __init__
        events:
            exitClicked
        
    - Program
        properties:
            paneRoot
            paneLeft
            PaneLeftClient
            paneLeftServers
            PaneRootMessages
            MenuBar

            userID
            username

            Clients
            active_Client
            active_Server

            exit

        methods:
            __init__
            change_server
            change_client
            send_Message
            connections_Thread
            server_ping

    - LoginBox
        properties:
            usernameInput : Tk.entry
            userLabel : Tk.label
            passwordinput : Tk.entry
            passwordLabel : Tk.label
            enterButton : Tk.button
            exitButton : Tk.button
        methods:
            exit
            enter
"""

# to be used as part of the Ext' Euclid algorithm
def GCD(num1, num2):
    if num2 == 0: return num1
    else: return GCD(num2, num1 % num2)

# creating a composite widget that 
# adds a scroll bar to the list widget
# this enables: 
#  - scrolling down chat messages
#  - scrolling down active clients
#  - scrolling down servers
class scrollListBox(tk.Frame):
    def __init__(self, parent, on_click=None):
        super().__init__(parent)

        #creating widget definitions
        self.listBox = tk.Listbox(self)
        self.scrollBar = tk.Scrollbar(self, orient=tk.VERTICAL)
        #set bindings and events for the scroll bar so contents scroll
        self.listBox.config(yscrollcommand=self.scrollBar.set)
        self.scrollBar.config(command=self.listBox.yview)
        self.listBox.bind("<Button-1>", on_click)

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
    
    def list_clear(self):
        self.listBox.clear()
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
        userID = username + password
        userID = str(hash(userID))

        loginFile = open(LOGINFILE, "w")

        loginFile.write(username + "\n")
        loginFile.write(password + "\n")
        loginFile.write(userID + "\n")
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
        self.exit = False
        self.serverConnectionActive = ""
        self.userName = ""
        self.passwd = ""
        self.userID = ""
        self.serverFile = open(SERVERFILE, "r").readlines()
        self.clients = {}
        self.protocolString = ""
        self.changeServer = False

        # getting user details from a file
        try:
            details_file = open(LOGINFILE, "r")
            details = details_file.readlines()
            print(details)
            self.username = details[0].strip("\n")
            self.passwd = details[1].strip("\n")
            self.userID = details[2].strip("\n")
        #print an error message to describe what happened
        except Exception as e:
            print(e.args)

        self.protocolString = self.userID + SPLITCHAR + self.userName 
        print(self.protocolString)

        # creating the gui
        # defining menu bar
        self.menubar = menuBar(self)
        self.config(menu=self.menubar)
        self.protocol("WM_DELETE_WINDOW", self.onClose)        
        # creating widget definitions
        self.paneRoot = tk.PanedWindow(self, handlepad=16, showhandle=True)
        self.paneLeft = tk.PanedWindow(self, showhandle=True, orient=tk.VERTICAL)
        self.paneLeftClients = scrollListBox(self)
        self.paneLeftServers = scrollListBox(self, on_click=self.change_Server)
        self.PaneRootMessages = messageFrame(self, send_command=self.send_message)
        # linking widgets together
        self.paneLeft.add(self.paneLeftClients)
        self.paneLeft.add(self.paneLeftServers)
        self.paneRoot.add(self.paneLeft)
        self.paneRoot.add(self.PaneRootMessages)
        
        # create handler threads
        #self. = th.Thread(target=self., daemon=True).start()    
        self.getOnlineUsersThread = th.Thread(target=self.getOnlineUsers, daemon=True).start()
        self.getOnlineServerThread = th.Thread(target=self.GetOnlineServers, daemon=True).start()

        # packing widgets
        self.paneRoot.pack(fill=tk.BOTH,expand=1)

        tk.mainloop()

    #this function sends a message
    def send_message(self, event):
        print("sending message")
        pass

    # called when any of the clents in the client selection window is clicked 
    def change_client(self, event):
        print("changing client")



    def change_Server(self, event):
        print("changing server")
        self.changeServer = True
    
    def onClose(self):
        self.close = False
        sys.exit()

    # check for any user sending a message
    def getIncomingConnections(self):

        while not self.exit:
            t.sleep(1)
        print("incoming connection lister is closing")
        
    # get user list from server
    def getOnlineUsers(self):
        onlineUserSocket = s.socket()
        while not self.exit:
            # check if the client is changing server
            if self.changeServer == True:
                # get a lock on variavbles
                # if not connected
                if self.serverConnectionActive == "":
                    onlineUserSocket.connect((self.paneLeftServers.get(), SERVERPORT))
                    onlineUserSocket.send(self.protocolString.encode(SOCKETENCODING))
                    self.serverConnectionActive = self.paneLeftServers.get()
                    print("prevoios connection = ''", self.serverConnectionActive)
                    self.changeServer = False
                # otherwise tell current server client is leaving and change connection
                else:
                    onlineUserSocket.send((self.protocolString + "`close").encode(SOCKETENCODING))
                    onlineUserSocket.connect((self.paneLeftServers.get(), SERVERPORT))
                    onlineUserSocket.send(self.protocolString.encode(SOCKETENCODING))
                    self.serverConnectionActive = self.paneLeftServers.get()
                    print("was connected", self.serverConnectionActive)
                    self.changeServer = False
            # otherwise get clients
            elif self.serverConnectionActive != "":
                self.paneLeftClients.clear()
                try:
                    self.clients = js.loads(onlineUserSocket.recv(BUFFERSIZE).decode())
                    print(self.clients)
                    self.paneLeftClients.clear()
                    for i in self.clients.keys():
                        self.paneLeftClients.insert(self.clients[i][0] + ", " + i)
                except Exception as e:
                    self.serverConnectionActive = ""
                    print(e.args)
            t.sleep(2)

        onlineUserSocket.send((self.protocolString + "`close").encode(SOCKETENCODING))
        onlineUserSocket.close()
        print("get online user thread is exiting")


    # check for online servers
    def GetOnlineServers(self):
        count = 0
        while not self.exit:
            self.paneLeftServers.clear()
            onlineServerSocket = s.socket()
            count = count + 1
            for i in self.serverFile:
                try:
                    print("connecting to", i)
                    onlineServerSocket.connect((i,9000))
                    onlineServerSocket.send("1".encode("ascii"))
                    onlineServerSocket.close()
                    self.paneLeftServers.insert(i)
                except Exception as e:
                    print("failed to connect to", i)
                    pass
            del onlineServerSocket
            print(count)
            t.sleep(5)
        print("get online server thread closing")


def main():
        # if the login file doesnt exist then open login prompt
    if LOGINFILE not in os.listdir():
        loginWindow = loginBox()
        # wait a second for the file to write
        t.sleep(1)

    P = Program()

if __name__ == "__main__":
    main()