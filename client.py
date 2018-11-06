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

NETWORKERRORCODES = [
                        8,
#                       10061,
                        51,
#                       11001,
#                       111,
#                       10060,
                        61
                    ]


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
        self.fileMenu.add_command(label="exit", command=sys.exit)
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

        if password == "":
            return 0

        userID = username + password
        userID = str(hash(userID))

        loginFile = open(LOGINFILE, "w")

        # write credentials to a file
        loginFile.write(username + "\n")
        # hash password for security
        loginFile.write(userID + "\n")
        # hash hashed password to generate a userid
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

        # create a message queue for threads
        self.userName = ""
        self.passwd = ""
        self.userID = ""
        self.currentClient = ""
        self.serverFile = open(SERVERFILE, "r").readlines()
        print(self.serverFile)
        self.protocolString = ""
        self.changeServer = False
        self.changeClient = False
        self.clients = {}

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
            details_file.close()

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
        self.paneLeftClients = scrollListBox(self, on_click=self.change_client)
        self.paneLeftServers = scrollListBox(self, on_click=self.change_Server)
        self.PaneRootMessages = messageFrame(self, send_command=self.send_message)
        # linking widgets together
        self.paneLeft.add(self.paneLeftClients)
        self.paneLeft.add(self.paneLeftServers)
        self.paneRoot.add(self.paneLeft)
        self.paneRoot.add(self.PaneRootMessages)
        
        # create handler threads    
        self.getIncomingConnectionThread = th.Thread(target=self.getIncomingConnections, daemon=True)
        self.getOnlineUsersThread = th.Thread(target=self.getOnlineUsers, daemon=True)
        self.getOnlineServerThread = th.Thread(target=self.GetOnlineServers, daemon=True)

        # set the name of them for debugging
        self.getIncomingConnectionThread.setName("get imcomming connections")
        self.getOnlineUsersThread.setName("get online servers")
        self.getOnlineServerThread.setName("online server thread")

        # start threads
        self.getIncomingConnectionThread.start()
        self.getOnlineUsersThread.start()
        self.getOnlineServerThread.start()

        # packing widgets
        self.paneRoot.pack(fill=tk.BOTH,expand=1)

        tk.mainloop()











    #this function sends a message to the currently selected client
    def send_message(self):
        if self.currentConnection != "" and self.currentClient != "":
            print("sending message")

            senderror = 0

            # get current client details
            clientID = self.currentClient[1]
            clientIP = self.clients[clientID][1]

            # get message from text box
            message = self.PaneRootMessages.entry_get()

            # try send to the client and write to file
            try:
                #make object
                sender_socket = s.socket()

                # attept to open the file and socket to capture any errors befor they occur
                sender_socket.connect(clientIP, CLIENTPORT)
                file = open("messages/" + clientID + ".txt", "a")

                # try send to the client and write to file
                sender_socket.send((self.protocolString + "`" + message).encode("ascii"))
                file.write(t.strftime("%d %m %Y : ") + message)

                #then add them to the message box (as this will be the active client)
                self.PaneRootMessages.list_insert(t.strftime("%d %m %Y : ") + messages)

            except Exception as e:
                print("failed to send", e.args, "not sent")
                sender_socket.close()
                file.close()



    # called when any of the clents in the client selection window is clicked 
    def change_client(self, event):

        # construct path to messages file
        self.currentClient = self.paneLeftClients.get().split(", ")
        filepath = "messages/" + self.currentClient[1] + ".txt"

        # check if tkinter didnt pick up on the listbox click (usually common) then clear the list box
        if self.currentClient[1] != "":
            
            # open file and get any saved messages
            try:
                file = open(filepath, "r")
                messages = file.readlines()

            except Exception as e:
                if e.args[0] == 2:
                    file = open(filepath, "w")
                    
                self.PaneRootMessages.list_clear()

                print("error changing client", e.args)

            for i in messages:
                self.PaneRootMessages.list_insert(i)
        # clear the list because tkinter diddnt pick up on the click
        else:
            self.PaneRootMessages.list_clear()



            filepath = "messages/" + self.currentClient
        # read from the file
        userFile = None
        # output each line as a separate item on the messages list box
        # change the currentClient variable to reflect changes














    # called when a server is selected from the server pane
    def change_Server(self, event):
        print("changing server")
        self.changeServer = True
        

    
    def onClose(self):
        t.sleep(1)
        
        sys.exit()

    # check for any user sending a message
    def getIncomingConnections(self):
        # create a listening socket
        clientListenSocket = s.socket()
        clientListenSocket.bind((BINDADDRESS, CLIENTPORT))
        clientListenSocket.listen(5)

        while 1:
            # accept connection
            connectedSocket, address = clientListenSocket.accept()
            print(address)
            # recieve sender details and message
            message = connectedSocket.recv(65535).decode().split(SPLITCHAR)
            print(message)

            # construct path to senders file (double slash to escape the character)
            path = "messages/" + message[0] + ".txt"

            # test for sender file

            # generate a string to be entered to the file
            # depending on any errors that occur
            with th.Lock():
                try:
                    file = open(path, 'a')
                    fileEntry = t.strftime("%d %m %Y : ") + message[2]
                    file.write(fileEntry)
                # if the file isnt found create the file
                except FileNotFoundError as e:
                    file = open(path, 'w')
                    fileEntry = t.strftime("%d %m %Y : ") + message[2]
                    file.write(fileEntry)
                # any unexpected errors write to a backup file so not to miss it
                except Exception as e:
                    print("recieving error", e.args, "attempting to save to a backup file")
                    file = open("backup messages.txt", 'a')
                    fileEntry = message[0] + " " + message[1] + " " + t.strftime("%d %m %Y : ") + message[2]
                    file.write(fileEntry)
                #eventually write the message to the file and close it
                finally:
                    file.close()

            # if the sender is the currently active user insert onto the message view
            if self.active_Client == message[0]:
                self.PaneRootMessages.list_insert(fileEntry)
   
        print("incoming_connection lister is closing")

    # get user list from server
    def getOnlineUsers(self):
        onlineUserSocket = s.socket()
        self.currentConnection = ""
        
        while 1:
            # is client changing servers
            if self.changeServer == True:
                self.changeServer = False
                # does the client have a connection if so close it
                if self.currentConnection != "":
                    try:
                        onlineUserSocket.send("close".encode(SOCKETENCODING))
                        print("disconnecting")
                        t.sleep(1)
                        onlineUserSocket.close()
                        self.currentConnection = ""
                    # client didnt connect then reset
                    except Exception as e:
                        # if error code is recognised the pas over the error
                        if e.args[0] in NETWORKERRORCODES:
                            self.currentConnection = ""
                            print("network error", e.args)
                            pass
                        else:
                            print("not connected\nonline user thread", e.args)
                            self.currentConnection = ""
                
                # get next servers details
                onlineUserSocket = s.socket()
                self.currentConnection = self.paneLeftServers.get().strip("\n")
                print("next server = ", self.currentConnection)

                #connect to the server
                try:
                    onlineUserSocket.connect((self.currentConnection, SERVERPORT))
                    onlineUserSocket.send(self.protocolString.encode("ascii"))
                    self.changeServer == False
                except Exception as e:
                    if e.args[0] in NETWORKERRORCODES:
                        self.currentConnection = ""
                        self.changeServer == False
                    pass
            
            # otherwise recieve data from the server
            elif self.currentConnection != "":
                self.paneLeftClients.clear()
                try:
                    onlineUserSocket.send("?".encode(SOCKETENCODING))
                    self.clients = js.loads(onlineUserSocket.recv(65535).decode(SOCKETENCODING))
                    for i in self.clients.keys():
                        if i == self.userID:
                            pass
                        else:
                            self.paneLeftClients.insert(self.clients[i][0] + ", " + i)
                    self.changeServer == False
                except Exception as e:
                    if e.args in NETWORKERRORCODES:
                        onlineUserSocket.send("close".encode("ascii"))
                        self.currentConnection = ""
                        self.changeServer == False
                    else:
                        print("not connected\nonline user thread", e.args)
                        self.currentConnection = ""
                        self.changeServer == False
            # otherwise do noting
            else:
                pass
            t.sleep(THREADWAITTIME)
        
        onlineUserSocket.close()
        return 0
                

    # check for online servers
    def GetOnlineServers(self):
        print(self.serverFile)
        while 1:
            self.paneLeftServers.clear()
            with th.Lock() as lock:
                onlineServerSocket = s.socket()
                onlineServerSocket.settimeout(1)
                
                for i in self.serverFile:
                    print(i.strip("\n",))
                    if i.find("#") > -1:
                        pass
                    try:
                        onlineServerSocket = s.socket()
                        onlineServerSocket.connect((i.strip("\n"),9000))
                        onlineServerSocket.send("1".encode("ascii"))
                        onlineServerSocket.close()
                        self.paneLeftServers.insert(i)
                    except Exception as e:
                        # error code 8 for unix error code 10060 or 10061 for nt
                        if e.args[0] in NETWORKERRORCODES:
                            pass
                        else:
                            print(i)
                            raise
                            pass
            t.sleep(THREADWAITTIME)
        print("get online server thread closing")
        return 0


def main():
        # if the login file doesnt exist then open login prompt
    if LOGINFILE not in os.listdir():
        loginWindow = loginBox()
        # wait a second for the file to write
        t.sleep(1)

    P = Program()

if __name__ == "__main__":
    main()