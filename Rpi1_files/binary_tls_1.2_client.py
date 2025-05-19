import socket
import ssl

HOST = '192.168.0.20'  # Server IP
PORT = 65432

def string_to_binary(s):
    """Convert string to its binary representation."""
    return ' '.join(format(ord(char), '08b') for char in s)

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # Not secure in production!

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        print(f"🔐 Connected to TLS server at {HOST}:{PORT}")
        try:
            while True:
                msg = input("You (plaintext): ")
                
                # Show binary representation of the plaintext
                binary_msg = string_to_binary(msg)
                print(f"🧬 Binary (before encryption): {binary_msg}")

                # Send the plaintext message
                ssock.sendall(msg.encode())

                # Receive and print response
                data = ssock.recv(1024)
                if not data:
                    break
                print(f"Server: {data.decode()}")
        except KeyboardInterrupt:
            print("\n🔌 Connection closed.")
