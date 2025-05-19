import socket
import ssl
import threading
import RPi.GPIO as GPIO
import time

SERVER_IP = '192.168.0.70'  # Replace with your server's IP
PORT = 65431

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)  # Ensure the pin is low initially

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # Skip certificate verification for self-signed certs

def handle_receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(f"Server: {data.decode()}")
        except:
            break

try:
    with socket.create_connection((SERVER_IP, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=SERVER_IP) as ssock:
            print(f"🔐 Connected securely to {SERVER_IP}:{PORT}")
            threading.Thread(target=handle_receive, args=(ssock,), daemon=True).start()
            while True:
                msg = input("You: ")
                GPIO.output(17, GPIO.HIGH)  # Trigger signal start
                ssock.sendall(msg.encode())
                GPIO.output(17, GPIO.LOW)   # Trigger signal end
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    GPIO.cleanup()  # Clean up GPIO settings
