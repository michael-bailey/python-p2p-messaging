#!/usr/bin/env python3

from select import select
import socket as s
import os


serverSocket = s.socket()
serverSocket.setblocking(0)
serverSocket.bind("", 0)
serverSocket.listen()

userName = [None]
userID = [None]
userAddr = [None]

readSockets = [serverSocket]
writeSockets = [None]
errorSockets = [None]


while True:
    read, write, error = select(readSockets, writeSockets, errorSockets)        # returns when there are any 
                                                                                # readable writable streams avalible

    for i in read:
        if i == serverSocket:                                                   # new client connected as it is readable
            tmpSocket, address = serverSocket.accept()
            readSockets.append(tmpSocket)
            writeSockets.append(tmpSocket)
        else:                                                                   # client has sent a request
            request = i.recv(65536).decode()
            if request == "quit":                                               # erase all details of the user logging in
                index = readSockets.index(i)
                userName[index] = 0
                userID[index] = 0
                userAddr[index] = 0
                userName.remove(0)
                userID.remove(0)
                userAddr.remove(0)
                
                readSockets.remove(i), writeSockets.remove(i)
            if request in userName:
                writeSockets[i].send(userAddr[userID.index(request)])           # find the address of the user requested
            else:
                i.send("error")
                    
    for j in range(1, len(userAddr)-1):                                         # generates a list of all users
                pass
                index = writeSockets.index(j)
                userString = userString + userName[j] + ","
                print(userString)

    for i in write:
        if i == None:
            pass
        else:
            i.send(userString)