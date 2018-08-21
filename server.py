import threading as th
import socket as s
import os


class connection(th.Thread):
    name = ""
    address = ""
    UID = ""
    socket = None


    def __init__(self, name, address, UID, socket):
        self.name = name
        self.address = address
        self.UID = UID
        self.socket = socket

