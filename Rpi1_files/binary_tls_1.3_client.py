import socket
import ssl

HOST = '192.168.0.20'
PORT = 65432

def string_to_binary(s):
    return ' '.join(format(ord(char), '08b') for char in s)

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Force TLS 1.3 only
context.minimum_version = ssl.TLSVersion.TLSv1_3
context.maximum_version = ssl.TLSVersion.TLSv1_3

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        print(f"🔐 Connected with TLS version: {ssock.version()}")
        try:
            while True:
                msg = input("You (plaintext): ")
                print(f"🧬 Binary (before encryption): {string_to_binary(msg)}")
                ssock.sendall(msg.encode())
                data = ssock.recv(1024)
                if not data:
                    break
                print(f"Server: {data.decode()}")
        except KeyboardInterrupt:
            print("\n🔌 Connection closed.")
