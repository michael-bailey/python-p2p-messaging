#!/usr/bin/env python3

#top line is a shebang for ease of use in linux ( and mac if your lucky and having a good day)

from select import select
import socket as s
import os


# set the server to listen for connections and set them to be non blocking to be used instead of using many threads 
serverSocket = s.socket()
serverSocket.setblocking(0)
serverSocket.bind(("", 0))
serverSocket.listen()

userName = [None]
userID = [None]
userAddr = [None]

readSockets = [serverSocket]
writeSockets = [serverSocket]
errorSockets = [serverSocket]

# simple function to get the list of users
def userList():
    x = ""
    for i in userName:
        x += i
    return x

def userDetails(username):
    pass


#main server program
while True:

    # returns when there are any readable or writable sockets avalible
    read, write, error = select(readSockets, writeSockets, errorSockets)  
    
    #if there are any sockets to be read then iterate through them
    for i in read:

        # new client connected as the main server socket as it is readable
        if i == serverSocket:
            
            # get the new clients socket from the accept function
            tmpSocket, address = serverSocket.accept()

            # recieve client data will be added to the lists to get 
            data = tmpSocket.recv(65535).decode().strip("\x00")

            # add the new connection to the lists
            readSockets.append(tmpSocket)                                        
            writeSockets.append(tmpSocket)

            userID.append(i[0])
            userName.append(i[1])
            userAddr.append(i[2])


        # otherwise a client has sent a request to the server
        else:                                                                   
            print(i)
            #null byte is used as a sepatator as it is very unlikely that a user will find a way to enter this control character
            request = i.recv(65536).decode().split("\x00")                      #
            if request[3] == "quit":
                #check to see if this user is acctually connected to the server
                if request[0] in userID:

                                                                                    # erase all details of the user logging in
                    index = readSockets.index(i)                                    # get current sockets placement in the lists
                    userName[index] = 0                                             # delete the sockets from the lists
                    userID[index] = 0
                    userAddr[index] = 0
                    userName.remove(0)                                              # clean the lists up (doesnt effect the placement because that is calculated when requested)
                    userID.remove(0)
                    userAddr.remove(0)
                    readSockets.remove(i) 
                    writeSockets.remove(i)
            if request[3] in userName:
                writeSockets[i].send(userAddr[userID.index(request)])           # find the address of the user requested
            else:
                i.send("error")
                    
    

    for i in write:
        # if its the first value (used for the listening erver position) do nothing
        if i == None:
            pass
        # other wise send a list of all connected users (usernames) to the server
    
        else:
            for i in userName:

                # dont put 'none' on 
                if i == None:
                    pass
                else:
                    i.send(userList())
                        

            