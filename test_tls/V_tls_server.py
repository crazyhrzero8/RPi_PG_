import socket, ssl

# Set up SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Bind and listen on port 8443
bindsocket = socket.socket()
bindsocket.bind(('192.168.0.20', 65431))
bindsocket.listen(5)
print("🔐 TLS server is running on 192.168.10.2:8443")

while True:
    newsocket, fromaddr = bindsocket.accept()
    try:
        # Wrap the new socket with SSL
        conn = context.wrap_socket(newsocket, server_side=True)

        # ✅ Print the TLS version used for this connection
        print(f"🔗 Connection from {fromaddr}")
        print("🔐 TLS version in use:", conn.version())

        # Receive data
        data = conn.recv(1024)
        print(f"📩 Received: {data.decode()}")

    except ssl.SSLError as e:
        print("❌ SSL error:", e)
    finally:
        conn.close()
