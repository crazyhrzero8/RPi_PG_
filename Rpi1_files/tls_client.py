import socket
import ssl
import threading

SERVER_IP = '192.168.0.70'  # Replace with server IP
PORT = 65431


context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # Skip cert verification (for self-signed)

def handle_receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(f"Server: {data.decode()}")
        except:
            break

with socket.create_connection((SERVER_IP, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=SERVER_IP) as ssock:
        print(f"🔐 Connected securely to {SERVER_IP}:{PORT}")
        threading.Thread(target=handle_receive, args=(ssock,), daemon=True).start()
        while True:
            msg = input("You: ")
            ssock.sendall(msg.encode())

