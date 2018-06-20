#!/usr/env python
# chat program
# michael bailey
# python

import socket as s
import time as t
import threading as th
import json as js
import queue as q

class program():

    def get_menu(self):
            print("1. send message.")
            print("2. get message.")
            print("3. show contacts")
            print("4. add contact")
            print("5. remove contact")
            print("6. who's online")
            print("7. exit program.")
            return input("enter number of the option : ")

    def __init__(self):

        self.client_config = js.load(open("config.json",'r'))
        self.contacts = js.load(open("contacts.json","r"))
        self.message_queue = q.Queue()
        self.messages = js.load(open("Messages.json","r"))
        th.Thread(target=self.connection_handler, args=()).start()

        while True:
            option = self.get_menu()

            if option == "1":
                self.send_data()

            if option == "2":
                self.get_data()

            if option == "3":
                self.show_contacts()

            if option == "4":
                self.add_contact()

            if option == "5":
                self.remove_contact()

            if option == "6":
                self.ping_all()

            if option == "7":
                self.save_all()
                exit()

    def send_data(self):
        print()
        option = input("input client data or choose contact (D or C) : ")
        print()
        if option.upper() == "C":
            contact = input("enter contact name : ")
            print()
            
            while contact not in self.contacts:
                print("{0} isnt in contact".format(contact))
                contact = input("enter contact name : ")
            
            connection_info = (self.contacts[contact]["ip"],self.contacts[contact]["port"])
            
            Message = input("enter message : ")
            print
            
            packet = {
                "info":
                {
                    "ip":s.gethostname(),
                    "port":self.client_config["port"]
                    },
                "content":Message
                }
            print(js.dumps(packet))

        else:
            ip = input("enter ip of client ")
            port = int(input("enter port of the client "))
            Message = input("enter the message to send ")
            print()

            connection_info = (ip,port)

            packet = {
                "info":
                {
                    "ip":s.gethostname(),
                    "port":self.client_config["port"]
                    },
                "content":Message
                }
            

        client_sock = s.socket()
        try:
            client_sock.connect(connection_info)
            client_sock.send(js.dumps(packet))
        except:
            print("couldnt connect ... aborting")
            print()

    def get_data(self):
        print()
        if self.message_queue.qsize() != 0:
            for i in range(self.message_queue.qsize()):
                print("message ", i, " is ", self.message_queue.get())
                print()
        else:
            print("no new messages")
            print()

    def show_contacts(self):
        print()
        for i in iter(self.contacts.keys()):
            print(i)
        print()

    def add_contact(self):
        print()
        name = input("enter name of new contact : ")
        ip = input("enter ip address : ")
        port = int(input("enter connection port : "))

        construct = {
            "ip":ip,
            "port":port,
        }
        self.contacts[name] = construct
        open("contacts.json",'w').write(js.dumps(self.contacts))

    def remove_contact(self):
        print()
        contact = input("enter contact to remove : ")
        if contact not in self.contacts:
            print("contact not found")
        else:
            print(self.contacts.pop(contact))
            open("contacts.json",'w').write(js.dumps(self.contacts))
            print("has been removed")
            print()
    
    def ping_all(self):
        print()
        ping_socket = s.socket()
        for i in iter(self.contacts.keys()):
            try:
                ping_socket.connect(i["ip"],i["port"])
                ping_socket.close()
                print(i,"is online")
            except:
                print(i,"isnt online")
        print()
    
    def save_all(self):
        open("contacts.json",'w').write(js.dumps(self.contacts))
        open("config.json",'w').write(js.dumps(self.client_config))

    def connection_handler(self):
        socket_begin = s.socket()
        socket_begin.bind((s.gethostname(), self.client_config["port"]))
        while True:
            
            socket_begin.listen(5)
            sock, info = socket_begin.accept()

            data = sock.recv(65536).decode("ascii")

            self.messages[str(len(self.messages)+1)] = js.loads(data)
            self.message_queue.put(data)

            
            sock.close()
            
            try:
                open("Messages.json",'w').write(js.dumps(self.messages)).close()
            except:
                print("error in data recieved")
                pass
            
            del sock
            del info
            del data
            t.sleep(1)

start_point = program()