#!/usr/bin/env python3
#top line is a shebang for ease of use in *nix

import threading as th
import socket as s
import json as js
import time as t
import errno
import os

print(s.gethostbyname(s.gethostname()))

THREADWAITTIME = 1
SERVERPORT = 9000
BINDADDRESS = ""     # using the 0.0.0.0 address 
SPLITCHAR = "`"

def removeClient(object):
    index = clients.index(object)
    print("removing object", clients[index], "from the clients")
    clients.remove(clients[index])
    for i in clients:
        print(i)

def getClients():
    clientDict = {}

    for i in clients:
        clientDict[i.Uid] = [i.username, i.ip]

    return clientDict

class clientConnection():
    def __init__(self, UID, username, IP, socket):
        super().__init__()

	    #create properties
        self.Socket = socket
        self.username = username
        self.ip = IP[0]
        self.Uid = UID
        self.exit = False

        self.recv_thread = th.Thread(target = self.recieve_Data, daemon=True)

    def start(self):
        self.recv_thread.start()
    
        # server will only send client info when the client asks for it with a '?'
    def recieve_Data(self):
        while not self.exit:
            try:
                message = self.Socket.recv(65535).decode().strip('\n')
                print(message)
                if message == "close":
                    self.close()
                    t.sleep(2)
                elif message == "?":
                    print(js.dumps(getClients()).encode("ascii"))
                    self.Socket.send(js.dumps(getClients()).encode("ascii"))
                else:
                    print("no message removing client")
                    self.close()
                    
            except Exception as e:
                print("error occured. closing client", self.ip[0], "errno", e.args)
                self.close()
                t.sleep(2)
            t.sleep(THREADWAITTIME)

    def close(self):
        self.exit = True
        self.Socket.close()
        removeClient(self)

serverSocket = s.socket()
serverSocket.bind((BINDADDRESS, SERVERPORT))
serverSocket.listen()

clients = []

while True:
    tmpSocket , address = serverSocket.accept()
    details = tmpSocket.recv(65535).decode().strip("\n").split(SPLITCHAR)
    print(details)
    if len(details) == 1:
        tmpSocket.close()
    elif len(details) == 2:
        print(address)
        try:
            tmpObject = clientConnection(details[0], details[1], address, tmpSocket)
            clients.append(tmpObject)
            clients[clients.index(tmpObject)].start()
            print("current client object : ", clients)
        except Exception as e:
            print("error with connection", e.args)
            tmpSocket.close()
    else:
        tmpSocket.close()
