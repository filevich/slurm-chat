import socket
import threading
import argparse
import signal
import sys
import random
import time

def signal_handler(sig, frame):
    try:
        client.send("exit".encode())
        client.close()
    except:
        pass
    finally:
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(description='TCP Chat Client')
parser.add_argument('client', help='Client name')
parser.add_argument('--host', default='0.0.0.0', help='Host IP address (default: 0.0.0.0)')
parser.add_argument('--port', type=int, default=65432, help='Port number (default: 65432)')
parser.add_argument('-n', type=int, default=100, help='Total number of messages')
args = parser.parse_args()

nickname = args.client
HOST     = args.host
PORT     = args.port
N        = args.n

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "NICKNAME":
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("Disconnected from the server")
            client.close()
            break

def write(n:int=10):
    for i in range(n):
        message = f"{nickname}: {i+1}/{n}"
        client.send(message.encode())
        base = 5
        random_dur = random.uniform(0, 1) # seconds
        time.sleep(base + random_dur)

    client.send("exit".encode())
    client.close()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write, args=(N,))
write_thread.start()