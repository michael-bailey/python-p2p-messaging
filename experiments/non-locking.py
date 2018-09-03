import socket as s


sock = s.socket()
sock.setblocking(0)
sock.bind(("", 0))
sock.listen(5)

while True:
	a, b = sock.accept()
	print(a.recv(65535))