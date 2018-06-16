import socket as s
import time as t
import threading as th
import json as js
import sys


connection_threads = []

def connection_handler(shell):
    while True:
        socket_begin = s.socket()
        socket_begin.bind((s.gethostname(), 2000))
        socket_begin.listen(5)
        sock, info = socket_begin.accept()
        connection_threads.append(th.Thread(target=recieve_data,args=(sock, info)))
        connection_threads[len(connection_threads) - 1].start()
        t.sleep(1)
     

def recieve_data(socket, info):
    data = socket.recieve(65536)
    print(data)
    t.sleep(5)


handler_thread = th.Thread(target=connection_handler)

while True:
    handle = th.Thread(target=connection_handler,args=())
    handle.start()

    send_socket = s.socket()
    while True:
        send_ip = input("enter ip")
        send_port = int(input("enter port"))
        connection_info = (send_ip, send_port)
        try:
            send_socket.connect(connection_info)
            send_socket.send(input("enter message").encode("ascii"))
            socket.close()
        except:
            print("couldn't connect peer must be offline")

