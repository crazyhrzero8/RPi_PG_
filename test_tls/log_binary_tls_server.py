import socket
import ssl
import threading

HOST = '192.168.0.20'  # Change to your server IP
PORT = 65432

# Create TLS 1.3 context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
context.minimum_version = ssl.TLSVersion.TLSv1_3
context.maximum_version = ssl.TLSVersion.TLSv1_3

def string_to_binary(s):
    return ' '.join(format(ord(c), '08b') for c in s)

def handle_client(connstream):
    print(f"🔒 Cipher Suite: {connstream.cipher()[0]}")
    while True:
        try:
            data = connstream.recv(1024)
            if not data:
                break
            print(f"Client: {data.decode()}")
            msg = input("You (plaintext): ")
            print(f"🧬 Binary (before encryption): {string_to_binary(msg)}")
            connstream.sendall(msg.encode())
        except:
            break
    connstream.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"🔐 TLS 1.3 Server listening on {PORT}...")
    while True:
        conn, addr = sock.accept()
        print("📶 Connection from", addr)
        connstream = context.wrap_socket(conn, server_side=True)
        threading.Thread(target=handle_client, args=(connstream,), daemon=True).start()
