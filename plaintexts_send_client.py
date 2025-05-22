import socket
import ssl
import RPi.GPIO as GPIO
import time
import os
import csv
from tqdm import tqdm

# === CONFIGURATION ===
SERVER_IP = '192.168.0.70'
PORT = 65431
TRIGGER_PIN = 17

NUM_TRACES = 1000
PLAINTEXT_LENGTH = 16

CSV_FILE = "plaintexts.csv"
HEX_FILE = "plaintexts_hex.txt"

# === GPIO SETUP ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.output(TRIGGER_PIN, GPIO.LOW)

# === TLS CONTEXT ===
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# === PLAINTEXT GENERATOR ===
def generate_plaintext():
    return os.urandom(PLAINTEXT_LENGTH)

# === CSV SAVER ===
def save_csv(plaintexts):
    with open(CSV_FILE, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Index"] + [f"Byte{i}" for i in range(PLAINTEXT_LENGTH)])
        for idx, pt in enumerate(plaintexts):
            writer.writerow([idx] + [b for b in pt])

# === HEX SAVER ===
def save_hex(plaintexts):
    with open(HEX_FILE, "w") as f:
        for pt in plaintexts:
            f.write(pt.hex() + "\n")

# === MAIN FUNCTION ===
plaintexts = []

try:
    with socket.create_connection((SERVER_IP, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=SERVER_IP) as ssock:
            print(f"[✓] Connected securely to {SERVER_IP}:{PORT}")

            for _ in tqdm(range(NUM_TRACES), desc="Sending"):
                pt = generate_plaintext()
                plaintexts.append(pt)

                # GPIO Trigger ON before TLS encryption
                GPIO.output(TRIGGER_PIN, GPIO.HIGH)
                ssock.sendall(pt)
                GPIO.output(TRIGGER_PIN, GPIO.LOW)

                # Optional delay between messages
                time.sleep(0.02)

except Exception as e:
    print(f"[!] Error: {e}")

finally:
    GPIO.cleanup()
    save_csv(plaintexts)
    save_hex(plaintexts)
    print(f"[✓] Saved {len(plaintexts)} plaintexts to {CSV_FILE} and {HEX_FILE}")
