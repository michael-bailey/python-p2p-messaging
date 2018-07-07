import socket as s
import json as js
import threading as th
from tkinter import *
import os
import time as t

"""
------------notes------------
    - think about Network address translation

"""
#creating a memory saving list
class memList():
    def __init__(self):
        super().__init__()

        List = []

    def insert(object)
        if self.List.insert

#creating a composite widget that combines the list box and a scroll bar
class scrollListBox(Frame):
    def __init__(self, root):
        super().__init__(root)

        #create widgets
        self.listbox = Listbox(self)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)

        #set up scrolling
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        #set bindings
        self.listbox.bind("<Button-1>", self.update)

        #pack the widgets into the frame !--not the root--!
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

    #functions that should have been inhereted from listbox
    def insert(self, index, *elements):
        self.listbox.insert(index, elements)

    def get(self, first, last=None):
        return self.listbox.get(first, last)
    
    def clear(self):
        self.listbox.delete(FIRST,END)
    
    def update(self, event):
        self.selected = self.listbox.get(ACTIVE)

class MessageWindow(Tk):
    def __init__(self, socket):
        super().__init__()

        #setting the socket as a attribute
        self.socket = socket

        #cleaning bit
        self.cleaning_bit = 0

        #defining widgets
        self.message_view = scrollListBox(self)
        self.text_box = Entry(self)
        self.send_button = Button(self)

        #packing widgets
        self.message_view.pack(fill=BOTH, expand=True)
        self.text_box.pack(fill=X, expand=True,side=LEFT)
        self.send_button.pack(side=RIGHT)

        #create thread
    
    def send_message(self):
        self.socket.send(self.text_box.get())

    def recieve_thread(self):
        try:
            msg = self.socket.recv(1024)
            self.message_view.insert(END, msg)
        except:
            self.cleaning_bit = 1
            self.destroy

class loginWindow(Tk):
    def __init__(self, start_up):
        super().__init__()

        #assigning passed values
        self.start_up = start_up

        #variables for window
        self.login = ''
        self.password =''
        
        #create gui widgets
        self.tip_label = Label(self, text="enter login details")
        self.login_box = Entry(self)
        self.password_box = Entry(self, show="#")
        self.enter_btn = Button(self, text="enter", command=self.Enter)

        #packing all widgets
        self.tip_label.pack(fill=X)
        self.login_box.pack(fill=X)
        self.password_box.pack(fill=X)
        self.enter_btn.pack(fill=X)

        mainloop()

    def get_values(self):
        return self.login, self.password

    def enter(self):
        self.login = self.login_box.get()
        self.password = hash(self.password_box.get())
        self.destroy

class clientWindow(Tk):
    def __init__(self):
        super().__init__()



        self.scroll_view = scrollListBox(self)
        self.scroll_view.bind("<Button-1>", self.open_window)

        def open_window(self):



loginWin = loginWindow

login, password = loginWin.login, loginWin.password

userWin = clientWindow()


