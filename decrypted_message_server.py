import socket
import ssl
import threading
import csv

HOST = '192.168.0.70'
PORT = 65431

SAVE_CSV = "received_plaintexts.csv"
SAVE_HEX = "received_plaintexts_hex.txt"

# Shared list to store messages
received_messages = []
lock = threading.Lock()

# Setup TLS context for server
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

def save_logs():
    # Save CSV
    with open(SAVE_CSV, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Index"] + [f"Byte{i}" for i in range(16)])
        for i, msg in enumerate(received_messages):
            writer.writerow([i] + [b for b in msg])

    # Save HEX
    with open(SAVE_HEX, "w") as f:
        for msg in received_messages:
            f.write(msg.hex() + "\n")

def handle_client(connstream, addr):
    print(f"[+] Connection from {addr}")
    try:
        while True:
            data = connstream.recv(1024)
            if not data:
                print(f"[-] Connection closed by {addr}")
                break

            print(f"Client [{addr}]: {data.hex()}")  # Optional: print hex

            with lock:
                received_messages.append(data)

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        connstream.close()
        save_logs()  # Save when client disconnects

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"🔐 TLS Server listening on {PORT} at {HOST}...")
    while True:
        try:
            conn, addr = sock.accept()
            connstream = context.wrap_socket(conn, server_side=True)
            threading.Thread(target=handle_client, args=(connstream, addr), daemon=True).start()
        except ssl.SSLError as e:
            print(f"[SSL ERROR] {e}")
            conn.close()
        except Exception as e:
            print(f"[ERROR] {e}")
