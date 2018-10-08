#!/usr/bin/env python3
#top line is a shebang for ease of use in *nix

import threading as th
import socket as s
import json as js
import time as t
import errno
import os

# print(s.gethostbyname(s.gethostname()))

SERVERPORT = 9000
SPLITCHAR = "`"

# set the server to use threads instead of non blocking sockets because i discovered daemon threads


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

        self.recv_thread = th.Thread(target = self.recieve_Data, daemon=True, args=())
        self.send_thread = th.Thread(target = self.send_Data, daemon=True, args=())

    def start(self):
        self.recv_thread.start()
        self.send_thread.start()
    
    def recieve_Data(self):
        while not self.exit:
            t.sleep(1)
            try:
                message = self.Socket.recv(65535).decode().strip('\n').split(SPLITCHAR)
                print(message)

                # if the close message is sent then delete everything about the client
                if message[2] == "close":
                    print("closing connection", self.ip)
                    self.close()
            except s.error as error:
                print("error occured. closing client", self.ip[0], "errno", error.errno)

                self.close()

    def send_Data(self):
        while not self.exit:
            t.sleep(1)
            with th.Lock():
                try:
                    self.Socket.send(js.dumps(getClients()).encode("ascii"))
                except s.error as error:
                    print("error occured. closing client", self.ip[0], "errno", error.errno)
                    self.close()
            t.sleep(1)

    def close(self):

        self.Socket.close()
        removeClient(self)
        self.exit = True

serverSocket = s.socket()
serverSocket.bind(("", SERVERPORT))
serverSocket.listen()

clients = []

while True:
    tmpSocket , address = serverSocket.accept()
    print(address)
    details = tmpSocket.recv(65535).decode().strip("\n").split(SPLITCHAR)
    if details == "1":
        tmpSocket.close()
    else:
        try:
            tmpObject = clientConnection(details[0], details[1], address, tmpSocket)
            clients.append(tmpObject)
            print("debug1", clients)
            clients[clients.index(tmpObject)].start()
            print(clients)
        except Exception as e:
            print(e.args)
            tmpSocket.close()
