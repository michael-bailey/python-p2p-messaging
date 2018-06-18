import socket as s
import time as t
import threading as th
import json as js
import sys

def connection_handler():
    while True:
        socket_begin = s.socket()
        socket_begin.bind((s.gethostname(), 2000))

        print("listening for connections\n")
        socket_begin.listen(5)
        sock, info = socket_begin.accept()

        data = sock.recv(65536)
        sock.close()
        print(data)
        print("got connection from {0} on port {1}\n".format(sock.getsockname(),info))

        del socket_begin
        del sock
        del info
        del data
        t.sleep(1)
     
handler_thread = th.Thread(target=connection_handler, args=())
handler_thread.start()

while True:
    connection_info = input("enter info (ip | port)\n").split(" ")
