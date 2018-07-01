import socket as s
import json as js
import threading as th
from tkinter import *
import os


"""
------------notes------------
    - think about Network address translation

"""


#creating a composite widget that combines the list box and a scroll bar
class scrollListBox(Frame):
    def __init__(self, root):
        super().__init__()

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



class start_window(Tk):
    def __init__(self, selection):
        super().__init__()

        #variables for later
        self.server = ''
        self.port = 1012
        self.login = ''
        self.password =''
        

        #load list of servers (currently local)
        self.servers = js.load(open(os.getcwd() + "/client/config/servers.json","r"))


        #create gui widgets
        #button gets the selected server and login details connects to the server 
        #sends details and the server will either accept (send ok signal) or not (close the socket) 
        self.server_select = scrollListBox(self)
        self.login_box = Entry(self)
        self.password_box = Entry(self, show="#")
        self.enter_btn = Button(self, text="enter", command=self.Enter)
        self.register_btn = Button(self, text="register", command=self.Register)


        #generate options
        for i in range(1,len(self.servers)+1):
            self.server_select.insert(END,self.servers[str(i)])


        #packing all widgets

        self.server_select.pack()
        self.login_box.pack()
        self.password_box.pack()
        self.enter_btn.pack(side=LEFT)
        self.register_btn.pack(side=RIGHT)

        #start the main loop
        mainloop()


    #called when enter button 
    def Enter(self):
        print("enter pressed")
        #get infomation
        self.server = self.server_select.get(ACTIVE)
        self.login = self.login_box.get()
        self.password = hash(self.password_box.get())

        # !--enter code to connect to server--!

        sock = s.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server, self.port))


        #kill window ready for next window
        self.destroy()
    
    def Register(self):
        print("reg pressed")

        #get infomation
        self.server = self.server_select.get(ACTIVE)
        self.login = self.login_box.get()
        self.password = hash(self.password_box.get())

        # !--enter code to connect to server--!

        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.connect((self.server, self.port))

"""
class Main_window(Tk):
    def __init__(self, server_ip, login, password):
    def 
"""

selection = ''
            
main_window = start_window(selection)
print(main_window.response)
print
"""
server_window = server_window(main_window.selection)
"""
