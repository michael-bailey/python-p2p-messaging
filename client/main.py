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

        #pack the widgets into the frame !--not the root--!
        self.listbox.pack(side=LEFT)
        self.scrollbar.pack(side=RIGHT, fill=Y)

    #functions that should have been inhereted
    def insert(self, index, *elements):
        self.listbox.insert(index, elements)

    def get(self, first, last=None):
        a = self.listbox.get(first, last)
        return a

#starting window class
class login(Tk):
    def __init__(self):
        super().__init__()

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

        #check if the login file exists
        fileExists = 0
        try:
            open("config/login.json","r")
            fileExists = 1
        except FileNotFoundError:
            pass
        
        if fileExists == 1:
            #kill window file exists no need to continue
            self.destroy()
            return
        else:
            #start the main loop
            mainloop()


    #called when enter button 
    def Enter(self):
        #get details from form/window
        self.login = self.login_box.get().encode("ascii")
        self.password = hash(self.password_box.get()).encode("ascii")
        
        #save them to a file
        temp_login = {
            "login":self.login,
            "psk":self.password
        }

        open("login.json","W").write(js.dump(temp_login))
         self.destroy()
        


login_window = login()

server_select_win = serverSelection()

server_connection = serv











"""

def Register(self):
        print("reg pressed")

        #get infomation
        self.server = self.server_select.get(ACTIVE).encode("ascii")
        self.login = self.login_box.get().encode("ascii")
        self.password = hash(self.password_box.get()).encode("ascii")

        #create socket object to send request to register a user 
        sock = s.socket()
        sock.connect((self.server[0], self.port))

        #send register message to the server
        sock.send("REG ".encode("ascii") + self.login + self.password)
        response = sock.recv(1024)

        #error reporting to the user
        if response == "USER_EXISTS":
            pass#error_box = messagebox()
        else:
            sock.close()
            self.destroy()


                

        #close the socket after we're done

"""