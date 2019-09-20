from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from program import NotificationCenter, Preferences
from threading import *
from tkinter import ttk
from socket import *
import os

class LocalResponderDaemon():

    def __init__(self):

        # getting the preferences object nd loading settings.
        self.preferences = Preferences()


        # setting up the socket listener + run variables
        self.listening_socket = socket(AF_INET, SOCK_DGRAM)
        self.listening_socket.bind(("192.168.0.255", 9000))
        self.listening_socket.setblocking(False)
        self.quit = False


        # setting up the notification center.
        self.center = NotificationCenter()
        self.setupNotifications()
        self.center.add_observer

        # starting the thread
        self.thread = Thread(self.run())

    # thread loop function
    def run(self):
        self.listening_socket.listen()
        

        while not self.quit:
            tmp_conn, addr = self.listening_socket.accept()
            print("got local connection")

    # setting up notification center bindings
    def setupNotifications():
        self.center.add_observer(self.ProgramQuit, "ProgramQuit", client)

    # start of recieved notification functions
    def ProgramQuit(self, sender, notification, info):
        pass

    def ProgramStart(self, sender, notification, info):
        pass
    # END