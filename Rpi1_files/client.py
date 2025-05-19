import socket

SERVER_IP = '192.168.0.20'
PORT = 65433

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

client_socket.sendall(b"hello from Client RPi 1")
data = client_socket.recv(1024)
print(f"Receibved from the server: {data.decode()}")

client_socket.close()
