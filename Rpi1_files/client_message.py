import socket
import threading

SERVER_IP = '192.168.0.20'

PORT = 65431

def handle_receive(sock):
	while True:
		data = sock.recv(1024)
		if not data:
			break
		print(f"Server: {data.decode()}")

def handle_send(sock):
	while True:
		msg = input("You: ")
		sock.sendall(msg.encode())

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print(f" connected to server at {SERVER_IP}:{PORT}")

recv_thread = threading.Thread(target=handle_receive, args=(client_socket,))
send_thread = threading.Thread(target=handle_send, args=(client_socket,))

recv_thread.start()
send_thread.start()
