import socket
import ssl
import threading

HOST = '192.168.0.70'
PORT = 65431

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

def handle_client(connstream):
    try:
        while True:
            data = connstream.recv(1024)
            if not data:
                break
            print(f"Client: {data.decode()}")
            msg = input("You: ")
            connstream.sendall(msg.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connstream.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"🔐 TLS Server listening on {PORT}...")
    while True:
        conn, addr = sock.accept()
        print("Connection from", addr)
        try:
            connstream = context.wrap_socket(conn, server_side=True)
            threading.Thread(target=handle_client, args=(connstream,), daemon=True).start()
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
            conn.close()
