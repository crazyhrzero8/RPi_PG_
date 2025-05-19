import socket
import ssl

# Create an SSL context (insecure for testing)
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Connect using SSL
with context.wrap_socket(socket.socket(), server_hostname='rpi2') as conn:
    conn.connect(('192.168.0.20', 65431))

    # ✅ Print TLS version
    print("🔐 TLS version in use:", conn.version())

    # ✅ Print cipher suite in use
    cipher = conn.cipher()
    print(f"🔒 Cipher suite used: {cipher[0]} ({cipher[1]}, {cipher[2]})")

    # Send message
    conn.send(b'Hello from RPi1 via TLS!')
