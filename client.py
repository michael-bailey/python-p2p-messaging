#!/usr/bin/env python3

import threading as th
import hashlib as hashing
import tkinter as tk
import socket as s
import json as js
import time as t
import sys
import os

# import settings 
try:
    CONFIG = js.load(open("settings.json"))
    # standard variables shouldn't change
    SERVERPORT = 9000
    CLIENTPORT = 9001
    BINDADDRESS = "0.0.0.0"
    SPLITCHAR = '`'
    SOCKETENCODING = "ascii"
    # non standard variables 
    BUFFERSIZE = CONFIG["buffer_size"]
    THREADWAITTIME = CONFIG["thread_delay"]                 
    LOGINFILE = CONFIG["login_file_name"]
    SERVERFILE = CONFIG["server_list_file_name"]

# if an error occurs use default settings
except:
    SERVERPORT = 9000
    CLIENTPORT = 9001
    BUFFERSIZE = 65535
    THREADWAITTIME = 3
    BINDADDRESS = "0.0.0.0"
    SPLITCHAR = '`'
    LOGINFILE = "login.txt"
    SERVERFILE = "servers.txt"
    SOCKETENCODING = "ascii"

NETWORKERRORCODES = [
                        8,
                        10061,
                        51,
                        11001,
                        10060,
                        61,
                        64
                    ]

# setting the new line char to a variable for ease of use
NEWLN = "\n"

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
    
    def curSelection(self):
        return self.listBox.curselection()

# this implements the classic file menu bar 
# found at the top of many applications this 
# will be used to add a exit butto
# and other features in the future
class menuBar(tk.Menu):
    def __init__(self, parent, serverClicked, exitClicked=sys.exit):
        super().__init__(parent)
        
        #making file menu
        self.fileMenu = tk.Menu(self, tearoff=0)
        self.fileMenu.add_command(label="exit", command=sys.exit)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="update server list", command=serverClicked)
        self.add_cascade(label="file", menu=self.fileMenu)

# simple message box for displaying messages
class messageBox(tk.Toplevel):
    def __init__(self, message):
        super().__init__()
        self.messageLabel = tk.Label(self, text=message)
        self.messageLabel.pack()

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

        # create a login variable to be checked
        self.didLogin = False

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

        # if no password or username then dont login
        if password == "" or username == "":
            self.didLogin = False
            messageBox("no username or password entered")
            return 0

        if LOGINFILE not in os.listdir():
            # pass the password into a sha256 hash function
            password = hashing.sha256(password.encode("ascii")).hexdigest()
            print(password)

            # combine to form the uid string to be hashed
            userID = username + password
            print(userID)

            # generate user id
            userID = str(hashing.sha256(userID.encode("ascii")).hexdigest())
            print(userID)

            # open the file for writing
            loginFile = open(LOGINFILE, "w")

            # write credentials to a file
            loginFile.write(username + NEWLN)

            # hash password for security
            loginFile.write(password + NEWLN)

            # hash hashed password to generate a userid
            loginFile.write(userID + NEWLN)
            loginFile.close()

            # created a new user, login 
            self.didLogin = True

            # kill the window
            self.destroy()
        else:

            # generate password hash for comparison
            password = hashing.sha256(password.encode("ascii")).hexdigest()
            print(password)
            loginFile = open(LOGINFILE, "r").readlines()
            print(loginFile)

            # if details correct then let the user login
            if username == loginFile[0].strip(NEWLN) and password == loginFile[1].strip(NEWLN):
                self.didLogin = True
                self.destroy()

            # other wise then dont let them login and display a message
            else:
                self.didLogin = False
                messageBox("incorrect login")
            return 0

    def exit(self):
        sys.exit(0)

# the main program
class Program(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("main window")

        #defining program variables

        # create a message queue for threads
        self.userName = ""
        self.passwd = ""
        self.userID = ""
        self.currentClient = ""

        # check if message folder is there
        if "messages" not in os.listdir():
            os.mkdir("./messages")
        
        #attempt to open the server file and load contents
        try:
            self.serverFile = open(SERVERFILE, "r").readlines()
        except FileNotFoundError as e:
            print("file {} not found creating empty file".format(SERVERFILE))
            open(SERVERFILE,"w").close()
            self.serverfile = []

        self.protocolString = ""
        self.changeServer = False
        self.changeClient = False
        self.clients = {}

        # getting user details from a file
        try:
            details_file = open(LOGINFILE, "r")
            details = details_file.readlines()
            print(details)
            self.userName = details[0].strip(NEWLN)
            self.passwd = details[1].strip(NEWLN)
            self.userID = details[2].strip(NEWLN)

        #print an error message to describe what happened
        except Exception as e:
            print(e.args)
            details_file.close()

        self.protocolString = self.userID + SPLITCHAR + self.userName
        print(self.protocolString)

        # creating the gui
        # defining menu bar
        self.menubar = menuBar(self, serverClicked=self.update_server_list)
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

    # changes a variable for easy server file updates
    def update_server_list(self):
        self.serverFile = open(SERVERFILE, "r").readlines()

    #this function sends a message to the currently selected client
    def send_message(self): 
        if self.currentConnection != "" and self.currentClient != "":
            print("sending message")

            # get current client details
            currentClientID = self.currentClient[1]
            currentClientIP = self.clients[currentClientID][1]

            # get message from text box
            message = self.PaneRootMessages.entry_get()

            # try send to the client and write to file
            try:
                #make object
                sender_socket = s.socket()

                # attept to open the file and socket to capture any errors befor they occur
                sender_socket.connect((currentClientIP, CLIENTPORT))
                file = open("messages/" + currentClientID + ".txt", "a")

                # try send to the client and write to file
                sender_socket.send((self.protocolString + "`" + message).encode("ascii"))
                file.write(t.strftime("%d %m %Y : ") + self.userName + " : " + message + NEWLN)

                #then add them to the message box (as this will be the active client)
                self.PaneRootMessages.list_insert(t.strftime("%d %m %Y : ")  + self.userName + " : " + message)

            except Exception as e:
                print("failed to send", e.args, "not sent")
                try:
                    sender_socket.close()
                    file.close()
                except:
                    pass

    # called when any of the clents in the client selection window is clicked 
    def change_client(self, event):
        self.changeClient = True
        self.PaneRootMessages.list_clear()

        # try construct path to messages file
        try:
            self.currentClient = self.paneLeftClients.get().split(", ")
            filepath = "messages/" + self.currentClient[1] + ".txt"
        except:
            # if the list box is empty an error occurs with lists
            filepath = ""

        # clear the listbox
        self.PaneRootMessages.list_clear()

        # check if the filepath contains a path
        if filepath != "":
            # open file and get any saved messages
            try:
                file = open(filepath, "r")
                messages = file.readlines()
                
                for i in messages:
                    print(i)
                    self.PaneRootMessages.list_insert(i)


            # usually called when the file doent exist
            except Exception as e:
                if e.args[0] == 2:
                    file = open(filepath, "w")
                    
                self.PaneRootMessages.list_clear()
                print("error changing client", e.args)
        else:
            print("error handled")
            return
        self.changeClient = False

    # called when a server is selected from the server pane
    def change_Server(self, event):
        print("changing server")
        self.currentClient = ""
        self.paneLeftClients.clear()
        self.PaneRootMessages.list_clear()

        #self.nextConnection = self.paneLeftServers.get().strip(NEWLN)

        self.changeServer = True
        
    # destroy window to exit program (avoids ide errors)
    def onClose(self):
        self.destroy()

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
                    print("got connection from", message)
                    fileEntry = t.strftime("%d %m %Y : ") + message[1] + " : " + message[2] + NEWLN
                    file.write(fileEntry)

                    # if the sender is the currently active user insert onto the message view
                    if self.currentClient[1] == message[0]:
                        self.PaneRootMessages.list_insert(fileEntry)
                # if the file isnt found create the file
                except FileNotFoundError as e:
                    file = open(path, 'w')
                    fileEntry = t.strftime("%d %m %Y : ")  + message[1] + " : " + message[2] + NEWLN
                    file.write(fileEntry)
                # any unexpected errors write to a backup file so not to miss it
                except Exception as e:
                    print("recieving error", e.args, "attempting to save to a backup file")
                    file = open("backup messages.txt", 'a')
                    fileEntry = message[0] + " " + message[1] + " " + t.strftime("%d %m %Y : ") + message[2]  + NEWLN
                    file.write(fileEntry)
                #eventually write the message to the file and close it
                finally:
                    file.close()
   
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
                self.changeServer = False
                onlineUserSocket = s.socket()
                self.currentConnection = self.paneLeftServers.get().strip(NEWLN)
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
            elif self.currentConnection != "" or self.changeClient == False:
                #self.paneLeftClients.clear()
                self.connectedClients = []
                try:
                    onlineUserSocket.send("?".encode(SOCKETENCODING))
                    self.clients = js.loads(onlineUserSocket.recv(65535).decode(SOCKETENCODING))
                    for i in self.clients.keys():
                        if i == self.userID:
                            pass
                        else:
                            self.connectedClients.append(self.clients[i][0] + ", " + i)
                            #self.paneLeftClients.insert(self.clients[i][0] + ", " + i)
                    self.paneLeftClients.clear()
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
                
                # refresh the client list
                self.paneLeftClients.clear()
                for i in self.connectedClients:
                    self.paneLeftClients.insert(i)
            # otherwise do noting
            else:
                pass
            t.sleep(THREADWAITTIME)
        
        onlineUserSocket.close()
        return 0
                
    # check for online servers
    def GetOnlineServers(self):
        self.serverFile = open(SERVERFILE, "r").readlines()
        print(self.serverFile)
        onlineServers = []
        Lock = th.RLock()
        while 1:
            #self.paneLeftServers.clear()
            # get a lock over variables
            if self.changeServer == False:
                onlineServers = []
                Lock.acquire()
                for i in self.serverFile:
                    print(i.strip(NEWLN))
                    # allows servers to be commented out
                    if i.find("#") > -1:
                        pass

                    # try connecting to see if the server is online
                    try:
                        onlineServerSocket = s.socket()
                        onlineServerSocket.settimeout(1)
                        onlineServerSocket.connect((i.strip(NEWLN),9000))
                        onlineServerSocket.send("1".encode("ascii"))
                        onlineServerSocket.close()

                        # if connected add to a list of active servers
                        onlineServers.append(i)
                        #self.paneLeftServers.insert(i)



                    except Exception as e:

                        # error code 8 for unix, error code 10060 or 10061 for nt (windows)
                        if e.args[0] in NETWORKERRORCODES or e.args[0] == "timed out":
                            pass
                        else:
                            print(e.args)
                            print(i)
                            pass

                # add the servers to the list after scanning
                self.paneLeftServers.clear()
                for i in onlineServers:
                    self.paneLeftServers.insert(i)

                # release the lock
                Lock.release()
                
            # allow other threads to operate, with a delay
            t.sleep(THREADWAITTIME)
            
        print("get online server thread closing")
        return 0

# main function
def main():
    
    # run login window to check user details
    loginWindow = loginBox()

    # if login passed then load program
    if loginWindow.didLogin == True:
        Program()

    # return a value to say that the program ended
    return 0

if __name__ == "__main__":
    main()
