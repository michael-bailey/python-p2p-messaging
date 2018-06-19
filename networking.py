import socket as s
import time as t
import threading as th
import json as js
import queue as q

class program():

    def get_menu(self):                                                         #displays and returns a menu option
            print("1. send message.")
            print("2. get message.")
            print("3. show contacts")
            print("4. add contact")
            print("5. remove contact")
            print("6. exit program.")
            return input("enter number of the option : ")

    def __init__(self):

        self.client_config = js.load(open("config.json",'r'))
        self.contacts = js.load(open("contacts.json","r"))
        self.message_queue = q.Queue()
        th.Thread(target=self.connection_handler, args=()).start()

        while True:
            option = self.get_menu()

            if option == "1":
                self.send_data()
            if option == "2":
                self.get_data()

    def send_data(self):
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
        for i in range(self.message_queue.qsize()):
            print(self.message_queue.get())
            print()

    def add_contact(self):
        name = input("enter name of new contact")
        ip = input("enter ip address")
        port = input("enter connection port")

        construct = {
            "ip":ip,
            "port":port,
        }
        self.contacts[name] = construct
        open("contacts.json",'w').write(js.dumps(self.contacts))

    def connection_handler(self):
        socket_begin = s.socket()
        socket_begin.bind((s.gethostname(), self.client_config["port"]))
        while True:
            
            socket_begin.listen(5)
            sock, info = socket_begin.accept()

            data = sock.recv(65536)
            sock.close()
            self.message_queue.put(data)
            
            del sock
            del info
            del data
            t.sleep(1)

    


start_point = program()
