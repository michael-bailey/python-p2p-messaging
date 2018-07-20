import threading as th
import tkinter as tk
import socket as s
import json as js
import time as t
import sys
import os

COMMUNICATION_PORT = 800

"""
------------notes------------
    - think about Network address translation
    - could use pyqt5

"""

#creating a composite widget that combines the list box and a scroll bar
class scrollListBox(tk.Frame):
    def __init__(self, parent, on_click=None):
        super().__init__(parent)

        self.on_click = on_click

        #creating widget definitions
        self.listbox = tk.Listbox(self)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        #set bindings and events
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        #packing widgets
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def insert(self, item):
        self.listbox.insert(tk.END, item)

    def clear(self):
        self.listbox.delete(0, tk.END)

class menuBar(tk.Menu):
    def __init__(self, parent, server=None):
        super().__init__(parent)

        #references from parameters
        self.server = server

        #making file menu
        self.fileMenu = tk.Menu(self, tearoff=0)

        self.fileMenu.add_command(label="server", command=self.server)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="exit", command=sys.exit)

        self.add_cascade(label="file", menu=self.fileMenu)

class messageFrame(tk.Frame):
    def __init__(self, parent, btn_command=None):
        super().__init__(parent)

        #variables
        self.button_command = btn_command

        #creating widget definitions
        self.listbox = scrollListBox(self)
        self.entryBox = tk.Entry(self)
        self.enterButton = tk.Button(self, text="enter", command=self.button_command)

        #defining bindings

        #packing widgets
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.entryBox.pack(fill=tk.X, expand=1, side=tk.LEFT )
        self.enterButton.pack(side=tk.RIGHT)

        #defining command functions

    def entry_get(self):
        return self.entryBox.get()

    def list_get(self):
        #return self.listbox.
        pass

    def list_insert(self, text):
        self.listbox.insert(text)
    
    def list_update(self):
        pass
    

class serverSelectWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.selector = scrollListBox(self)
        try:
            self.servers = js.load(open("servers.json", "r"))
        except:
            print("file not found")
            pass

    def on_click(self):
        try:
            self.ArgOn_click()
        except:
            print("click failed")
            pass

    def selected_server(self):
        return 

class application(tk.Tk):
    def __init__(self):
        super().__init__()

        #defining variables
        self.active_client = 0
        self.client_details = {}

        self.selected_server = "127.0.0.1"


        #definig menu bars
        self.menubar = menuBar(self, server=self.serverSelector)
        self.config(menu=self.menubar)        

        #creating widget definitions
        self.splitPane = tk.PanedWindow(self, handlepad=16, showhandle=True)
        self.pane1_contacts = scrollListBox(self)
        self.pane2_messages = messageFrame(self, btn_command=self.send_message)

        #linking widgets together
        self.splitPane.add(self.pane1_contacts)
        self.splitPane.add(self.pane2_messages)

        #packing widgets
        self.splitPane.pack(fill=tk.BOTH,expand=1)

        #creating bindings

        #styling

        #create handler threads
        self.connections = th.Thread(target=self.connection_handler)
        self.sync = th.Thread(target=self.server_sync)
        
        tk.mainloop()

    #functions
    def send_message(self):
        self.pane2_messages.list_insert(self.pane2_messages.entry_get())

    def change_active_client(self):
        pass

    def serverSelector(self):
        a = serverSelectWindow()
        self.selected_server = a.get_selection()

    #thread functions
    def connection_handler(self):
        sock = s.socket()
        sock.bind(("",COMMUNICATION_PORT))
        sock.listen(7)
        
        while True:
            connection_socket, address = sock.accept()
            print(address,"connected")
            # USER_ID:TIME:MESSAGE
            msg = str(connection_socket.recv(1024).decode())
            msg.split(":")
            

    def server_sync(self):


        t.sleep(1)


a = application()