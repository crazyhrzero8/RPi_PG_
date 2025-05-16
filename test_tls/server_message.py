import socket
import threading

HOST  =  '192.168.0.20'
PORT = 65431


def handle_receive(conn):
	while True:
		data = conn.recv(1024)
		if not data:
			break
		print (f"Client: {data.decode()}")

def handle_send(conn):
	while True:
		msg = input("You: ")
		conn.sendall(msg.encode())


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on port {PORT}....")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")


recv_thread = threading.Thread(target = handle_receive, args=(conn, ))
send_thread = threading.Thread(target = handle_send, args=(conn, ))

recv_thread.start()
send_thread.start()
