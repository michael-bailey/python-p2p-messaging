from threading import Thread, RLock, ThreadError
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import NotificationCenter
from tkinter import ttk
import Preferences
import os


class client(object):
    _instance = None

    def __init__(self):
        if not hasattr(self, 'preferences'):
            self.preferences = Preferences()
            self.notificationCenter = NotificationCenter()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

