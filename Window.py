import tkinter as tk
import socket as s
import json as js
import threading as th

class window:

    current_connecton = ("127.0.0.1",1000)



    def __init__(self):
        self.window = tk.Tk()

        self.menu = tk.Menu(window)
        
        self.menu.add()

        self.pane = tk.PanedWindow(self.window, orient=tk.HORIZONTAL)

        self.left_frame = tk.Frame()

        self.contacts = tk.Listbox(self.left_frame)
        self.contacts.pack(fill=tk.BOTH, expand=1)
        
        self.left_frame.pack(fill=tk.BOTH, expand=1)


        self.right_frame = tk.Frame()


        self.messages = tk.Listbox(self.right_frame)
        self.messages.pack(fill=tk.BOTH, expand=1)

        self.entry_frame = tk.Frame(self.right_frame)

        self.enter_box = tk.Entry(self.entry_frame)
        self.enter_box.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.enter_button = tk.Button(self.entry_frame, text="enter")
        self.enter_button.pack(side=tk.RIGHT, fill=tk.X)

        self.entry_frame.pack(fill=tk.X)


        self.right_frame.pack(fill=tk.BOTH, expand=1)

        self.pane.pack(fill=tk.BOTH, expand=1)

        self.pane.add(self.left_frame)
        self.pane.add(self.right_frame)



        tk.mainloop()
    def accept_connections():
        raise NotImplementedError
    def send

a = window()