import socket

HOST = '192.168.0.20'
PORT = 65433


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server is listening")

conn,addr = server_socket.accept()

print("Connected")

while True:
	data = conn.recv(1024)
	if not data:
		break
	print("Received")
	conn.sendall(b"ACK")
conn.close()
