#!/usr/bin/env python3
#top line is a shebang for ease of use in *nix

import threading as th
import socket as s
import os

# print(s.gethostbyname(s.gethostname()))

SERVERPORT = 9000
SPLITCHAR = "§"

# set the server to use threads instead of non blocking sockets because i discovered daemon threads
serverSocket = s.socket()
serverSocket.bind(("", SERVERPORT))
serverSocket.listen()

clients = []


def getClients():
    clientDict = {}

    for i in clients:
        clientDict[i.userid] = [i.username, i.ip]

    return clientDict

class clientConnection():
    def __init__(self, UID, username, IP, socket):
        super().__init__()
		
	    #create properties
        self.Socket = socket
        self.userName = ""
        self.ip = IP
        self.Uid = UID

        self.recv_thread = th.Thread(target = self.recieve_Data, daemon=True, args=(self))
        self.send_thread = th.Thread(target = self.send_Data, daemon=True, args=(self))

        self.recv_thread.start()
        self.send_thread.start()
    
    def recieve_Data(self):
        while True:
            message = self.Socket.recv(65535).decode().split(SPLITCHAR)
            if message[2] = ""
			
    def send_Data(self):
        self.Socket.send(getClients())

		
while True:
    tmpSocket , address = serverSocket.accept()
    print(address)
    details = tmpSocket.recv(65535).decode().split(SPLITCHAR)
    try:
        clients.append(th.Thread(target = clientConnection, daemon=True, args=(details[0], details[1], address, tmpSocket)).start())
    except:
        tmpSocket.close()
    print(clients)


