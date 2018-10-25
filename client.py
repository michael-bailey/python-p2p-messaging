#!/usr/bin/env python3

import threading as th
import hashlib as hashing
import errno as error
import tkinter as tk
import socket as s
import queue as Q
import json as js
import time as t
import sys
import os

SERVERPORT = 9000
CLIENTPORT = 9001
BUFFERSIZE = 65535
THREADWAITTIME = 3
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
    def __init__(self, parent, exitClicked=sys.exit, forceSendWindow=None):
        super().__init__(parent)
        
        #making file menu
        self.fileMenu = tk.Menu(self, tearoff=0)
        if forceSendWindow == None:
            self.fileMenu.add_command(label="not avalible")
        else:
            self.fileMenu.add_command(label="force send menu", command=forceSendWindow)
        self.fileMenu.add_command(label="exit", command=lambda: tk.mess)
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

        # write credentials to a file
        loginFile.write(username + "\n")
        # hash password for security
        loginFile.write(hash(password) + "\n")
        # hash hashed password to generate a userid
        loginFile.write(userID + "\n")
        loginFile.close()

        self.destroy()

    def exit(self):
        sys.exit(0)

"""
class forceSendWindow(tk.toplevel):
    def __init__(self):
        super().__init__()

        # definning the window widgets
        self.ipLabel = tk.Label(text="usersIP:")
        self.messageLabel = tk.Label(text="message:")
        self.ipEntry = tk.Entry()
        self.messageEntry = tk.Entry()
        self.sendButton = tk.Button(text="send!")
        self.closeButton = tk.Button(text="close")

        #setting them to a grid
        self.ipLabel.grid(row=0,column=0)
        self.messageLabel.grid(row=1,column=0)
        self.ipEntry.grid(row=0,column=1)
        self.messageEntry.grid(row=1,column=1)
        self.sendButton.grid(row=2,column=0)
        self.closeButton.grid(row=2,column=1)

    # defining the send message function (will be used in the main window)
    def sendMessage():
        pass
    # function to close the window if not needed   
    def closeWindow():
        self.destroy()
"""   


# the main program
class Program(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("")

        #defining program variables

        # create a message queue for threads
        self.userName = ""
        self.passwd = ""
        self.userID = ""
        self.serverFile = open(SERVERFILE, "r").readlines()
        self.protocolString = ""
        self.changeServer = False
        self.changeClient = False

        # getting user details from a file
        try:
            details_file = open(LOGINFILE, "r")
            details = details_file.readlines()
            print(details)
            self.userName = details[0].strip("\n")
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

    #this function sends a message to the currently selected client
    def send_message(self, event):
        print("sending message")
        pass

    # called when any of the clents in the client selection window is clicked 
    def change_client(self, event):
        print("changing client")
        self.changeClient = True

    # called when a server is selected from the server pane
    def change_Server(self, event):
        print("changing server")
        self.changeServer = True
        t.sleep(1)
        self.changeServer = False

    
    def onClose(self):
        exit(0)

    # check for any user sending a message
    def getIncomingConnections(self):
        # create a listening socket
        clientListenSocket = s.socket()
        clientListenSocket.bind((BINDADDRESS, CLIENTPORT))
        clientListenSocket.listen(5)

        while not self.exit:
            # accept connection
            connectedSocket, address = clientListenSocket.accept()

            # recieve sender details and message
            message = connectedSocket.recv(65535).decode().split(SPLITCHAR)

            # construct path to senders file (double slash to escape the character)
            path = "messages\\" + message[0] + ".txt"

            # test for sender file
            # generate a string to be entered to the file
            # depending on any errors that occur
            try:
                file = open(path, 'a')
                fileEntry = t.strftime("%d %m %Y : ") + message[2]
            # if the file isnt found create the file
            except FileNotFoundError as e:
                file = open(path, 'r')
                fileEntry = t.strftime("%d %m %Y : ") + message[2]
            # any unexpected errors write to a backup file so not to miss it
            except exception as e:
                print("recieving error", e.args, "attempting to save to a backup file")
                file = open("backup messages.txt", 'a')
                fileEntry = t.strftime("%d %m %Y : ") + message[2]
            #eventually write the message to the file and close it
            finally:
                file.append(fileEntry)
                file.close()

            # if the sender is the currently active user insert onto the message view
            

        print("incoming connection lister is closing")

    # get user list from server
    def getOnlineUsers(self):
        onlineUserSocket = s.socket()
        currentConnection = ""
        clients = {}

        while 1:
            # is client changing servers
            if self.changeServer == True:
                # does the client have a connection if so close it
                if currentConnection != "":
                    try:
                        onlineUserSocket.send("close".encode(SOCKETENCODING))
                        print("disconnecting")
                        onlineUserSocket.close()
                        currentConnection = ""
                    # client isnt connected procede anyway
                    except Exception as e:
                        print("not connected [get online user thread]")
                        print(e.args)
                        currentConnection = ""
                
                # get next servers details
                onlineUserSocket = s.socket()
                currentConnection = self.paneLeftServers.get()
                print("next server = ", currentConnection)

                #connect to the server
                try:
                    onlineUserSocket.connect((currentConnection, SERVERPORT))
                    onlineUserSocket.send(self.protocolString.encode("ascii"))
                    self.changeServer == False
                except Exception as e:
                    currentConnection = ""
                    self.changeServer == False
                    pass
            
            # otherwise recieve data from the server
            elif currentConnection != "":
                self.paneLeftClients.clear()
                try:
                    onlineUserSocket.send("?".encode(SOCKETENCODING))
                    clients = js.loads(onlineUserSocket.recv(65535).decode(SOCKETENCODING))
                    for i in clients.keys():
                        if i == self.userID:
                            pass
                        else:
                            self.paneLeftClients.insert(clients[i][0] + ", " + i)
                    self.changeServer == False
                except Exception as e:

                    currentConnection = ""
                    print(e.args)
                    self.changeServer == False
            else:
                print("notconnected")
            t.sleep(THREADWAITTIME)
        return 0
                 

                

        """
        onlineUserSocket = s.socket()
        while not self.exit:
            # check if the client is changing server
            if self.changeServer == True:
                # if not connected?
                if self.serverConnectionActive == "":
                    onlineUserSocket.connect((self.paneLeftServers.get(), SERVERPORT))
                    onlineUserSocket.send(self.protocolString.encode(SOCKETENCODING))
                    self.serverConnectionActive = self.paneLeftServers.get()
                    print("previous connection = ", self.serverConnectionActive)
                    self.changeServer = False
                # otherwise tell current server client is leaving and change connection
                else:
                    onlineUserSocket.send("close".encode(SOCKETENCODING))
                    onlineUserSocket.connect((self.paneLeftServers.get(), SERVERPORT))
                    onlineUserSocket.send(self.protocolString.encode(SOCKETENCODING))
                    self.serverConnectionActive = self.paneLeftServers.get()
                    print("was connected", self.serverConnectionActive)
                    self.changeServer = False
            # otherwise get clients
            elif self.serverConnectionActive != "":
                print("clearing panel")
                self.paneLeftClients.clear()
                try:
                    print("getting users")
                    self.clients = js.loads(onlineUserSocket.recv(BUFFERSIZE).decode())
                    print(":users:")
                    print(self.clients)
                    self.paneLeftClients.clear()
                    for i in self.clients.keys():
                        self.paneLeftClients.insert(self.clients[i][0] + ", " + i)
                except Exception as e:
                    self.serverConnectionActive = ""

                    print(e.args)
            t.sleep(2)
        print("sending", ("close").encode(SOCKETENCODING))
        onlineUserSocket.send("close".encode(SOCKETENCODING))
        t.sleep(1)
        print("closing socket")
        onlineUserSocket.close()
        print("get online user thread is exiting")

"""

    # check for online servers
    def GetOnlineServers(self):
        print(self.serverFile)
        while 1:
            self.paneLeftServers.clear()
            with th.Lock() as lock:
                onlineServerSocket = s.socket()
                
                for i in self.serverFile:
                    try:
                        onlineServerSocket = s.socket()
                        onlineServerSocket.connect((i.strip("\n"),9000))
                        onlineServerSocket.send("1".encode("ascii"))
                        onlineServerSocket.close()
                        self.paneLeftServers.insert(i)
                    except Exception as e:
                        if e.args[0] == 8 or e.args[0] == 10061:
                            pass
                        elif e.args[0] == 51:
                            pass
                        else:
                            print(e.args)
                            print("get online server thread\n", e.args)
            t.sleep(THREADWAITTIME)
        print("get online server thread closing")
        return 0


def main():
        # if the login file doesnt exist then open login prompt
    if LOGINFILE not in os.listdir():
        loginWindow = loginBox()
        # wait a second for the file to write
        t.sleep()

    P = Program()

if __name__ == "__main__":
    main()