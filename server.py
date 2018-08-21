import socket as s
import os
import threading as th

class connection(th.Thread):
    name = ""
    address = ""
    UID ""
    s.socket: socket = None

