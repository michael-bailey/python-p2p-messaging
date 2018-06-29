import tkinter as tk
import socket as s
import json as js
import threading as th

class window:

    current_connecton = ("127.0.0.1",1000)
    contacts = {}


    def __init__(self):
        self.window = tk.Tk()

        self.right_frame = tk.Frame(self.window)


        self.messages = tk.Listbox(self.right_frame)
        self.messages.pack(fill=tk.BOTH, expand=1)

        self.entry_frame = tk.Frame(self.right_frame)

        self.enter_box = tk.Entry(self.entry_frame)
        self.enter_box.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.enter_button = tk.Button(self.entry_frame, text="enter")
        self.enter_button.pack(side=tk.RIGHT, fill=tk.X)

        self.entry_frame.pack(fill=tk.X)


        self.right_frame.pack(fill=tk.BOTH, expand=1)

        self.start_threads()

        tk.mainloop()

    def start_threads():
        th.Thread(target=self.accept_connections,args=())
        self.messages.ad
        



    def accept_connections(self):
        raise NotImplementedError
        
    def send(self):
        raise NotImplementedError

a = window()