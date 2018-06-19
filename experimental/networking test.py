import socket as s
import threading as th

#thread for sending messages (client)
#thread for accepting connectons
# -- creates thread for each connection

def reciever(socket, output, ipaddress):
    message = json.dumps(socket.recv(65536))
    message
    


def connection_manager(number)
    while True:
        conector = s.socket()
        conector.listen(5)
        

    