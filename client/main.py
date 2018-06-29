import socket as s
import json as js
import threading as th
from tkinter import *


"""
------------notes------------
    - think about Network address translation



class start_window(Tk):
    def __init__(self, selection):
        super().__init__()

        #variables for later
        self.server = ''
        self.port = 1012
        self.login = ''
        self.password =''


        #load list of servers (currently local)
        self.servers = js.load(open("servers.json","r"))


        #create gui widgets
        #button gets the selected server and login details connects to the server 
        #sends details and the server will either accept (send ok signal) or not (close the socket) 
        self.server_select = Listbox(self)
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

    def Enter(self):
        self.server = self.server_select.get(ACTIVE)
        self.login = self.login_box.get()
        self.password = hash(self.password_box.get())
        self.destroy()
    
    def Register(self):

        #get detail's to register
        self.server = self.server_select.get(ACTIVE)
        self.login = self.login_box.get()
        self.password = hash(self.password_box.get())

        try:
            server_connection = s.socket()
            server_connection.connect((self.server,self.port))
            server_connection.send("reg {0} {1}".format(self.login, self.password).encode("ascii"))
            self.response = server_connection.recv(16)
            
            if self.response == "0":
                raise Exception
            else:
                self.destroy()
        except:
            pass

        

class Main_window(Tk):
    def __init__(self, server_ip, login, password):
        


selection = ''
            
main_window = start_window(selection)
print(main_window.response)
print
"""
server_window = server_window(main_window.selection)
"""
