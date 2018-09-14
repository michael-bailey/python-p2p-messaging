#!/usr/bin/env python3
#top line is a shebang for ease of use in linux

import thread as th
import socket as s
import os


# set the server to use threads instead of non blocking sockets because i discovered daemon threads 
serverSocket = s.socket()
serverSocket.setblocking(0)
serverSocket.bind(("", 9000))
serverSocket.listen()

clients = []

# simple function to get the list of users
def userList():
    x = ""
    for i in userName:
        x += i
    return x


class clientConnection(th.thread, s.socket):
    def __init__(self, UID, username, IP, socket):
        self.Socket = socket
        self.userName
        self.ip = IP
        self.Uid = UID

        self.start(target = self.func, daemon = True)

        def func():
            while True:
                message = self.Socket.recv(65535).split("")
                print(os.get    , username, ":" , message)





while true:
    tmpSocket , address = serverSocket.accept()
    print(address)
