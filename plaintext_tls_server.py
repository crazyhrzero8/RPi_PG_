import socket
import ssl
import threading
import csv
import os

HOST = '192.168.0.70'  # Or 0.0.0.0 for all interfaces
PORT = 65431

SAVE_CSV = "received_plaintexts.csv"
SAVE_HEX = "received_plaintexts_hex.txt"

received_messages = []
lock = threading.Lock()

# Setup TLS context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

def save_logs():
    if not received_messages:
        return
    with open(SAVE_CSV, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Index"] + [f"Byte{i}" for i in range(16)])
        for i, msg in enumerate(received_messages):
            writer.writerow([i] + [b for b in msg])

    with open(SAVE_HEX, "w") as f:
        for msg in received_messages:
            f.write(msg.hex() + "\n")

def handle_client(connstream, addr):
    print(f"[+] Connection from {addr}")
    try:
        while True:
            data = connstream.recv(1024)
            if data:
                print(f"[{addr}] Received: {data.hex()}")
                with lock:
                    received_messages.append(data)
            else:
                # Minor pause to handle TCP buffering
                time.sleep(0.01)
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        connstream.close()
        print(f"[-] Connection closed: {addr}")
        save_logs()

# Start server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"🔐 TLS Server listening on {HOST}:{PORT} ...")
    while True:
        conn, addr = sock.accept()
        connstream = context.wrap_socket(conn, server_side=True)
        threading.Thread(target=handle_client, args=(connstream, addr), daemon=True).start()
