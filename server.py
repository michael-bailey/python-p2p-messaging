#!/usr/bin/env python3
#top line is a shebang for ease of use in linux

import threading as th
import socket as s
import os

SERVERPORT = 9000

# set the server to use threads instead of non blocking sockets because i discovered daemon threads 
serverSocket = s.socket()
serverSocket.setblocking(0)
serverSocket.bind(("", SERVERPORT))
serverSocket.listen()

clients = []

# simple function to get the list of users
def userList():
    x = ""
    for i in clients:
        x = x + i.username + ","
    return x


class clientConnection():
    def __init__(self, UID, username, IP, socket):
        self.Socket = socket
        self.userName
        self.ip = IP
        self.Uid = UID

        self.start(target = self.func, daemon = True)

        def func():
            while True:
                message = self.Socket.recv(65535).split("")
                print(os.getpid()    , username, ":" , message)





while True:
    tmpSocket , address = serverSocket.accept()
    print(address)
    clients.append(th.thread(target = clientConnection, daemon=True, args=()).start())
