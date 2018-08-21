#!/usr/env python
# chat program
# michael bailey
# python

import socket as s
import time as t
import threading as th


class program():

    

    def __init__(self):
        
        self.handler = th.thread(target=self.server_connection).start()

        print("online")
        print("send <person> <message>")
        print("menu")
        print("close")
        print("")
        print("all messages will be printed automaticly")
        

        while True:
            command = input(":>").split(" ")

            if command[0] = "send"
                

            

    def send_message(self):
        print()

        client_sock = s.socket()
        try:
            client_sock.connect(connection_info)
            client_sock.send(js.dumps(packet).encode("ascii"))
        except s.error as e:
            print("couldnt connect ... aborting")
            print()

    def server_connection():
        sock = s.socket()
        sock.connect("—")


        




"""
        print()
        option = input("input client data or choose contact (D or C) : ")
        print()
        if option.upper() == "C":

            conversation == 

            contact = input("enter contact name : ")
            print()
            



            while contact not in self.contacts:
                print("{0} isnt in contact".format(contact))
                contact = input("enter contact name : ")
            
            connection_info = (self.contacts[contact]["host"],self.contacts[contact]["port"])
            
            Message = input("enter message : ")
            print
            
            packet = {
                "info":
                {
                    "host":s.gethostname(),
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
                    "host":s.gethostname(),
                    "port":self.client_config["port"]
                },
                "content":Message
                }
            

        client_sock = s.socket()
        try:
            client_sock.connect(connection_info)
            client_sock.send(js.dumps(packet).encode("ascii"))
        except s.error as e:
            print("couldnt connect ... aborting")
            print()
        
        client_sock.close()



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
            "host":ip,
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
                ping_socket.connect(i["host"],i["port"])
                ping_socket.close()
                print(i,"is online")
            except:
                print(i,"isnt online")
        print()

    def change_config(self):

        config = js.load(open("config.json"))

        change = input("change port number : ")
        if change.upper() != "no" or change.upper() != "n":


            js.dump(self.client_config, open("config.json", "w"))

    def connection_handler(self):
        socket_begin = s.socket()
        socket_begin.bind(("", self.client_config["port"]))
        while not self.exit_flag:
            
            socket_begin.listen(5)
            sock, info = socket_begin.accept()
            data = sock.recv(65536).decode("utf-8")
            sock.close()

            data = js.loads(data)

            

            try:
                js.dump(self.messages,open("Messages.json","w"))
            except s.error as e:
                print("error in data recieved")
                print(e.value)
                pass
            
            del sock
            del info
            del data
            t.sleep(1)
"""
start_point = program()