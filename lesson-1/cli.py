import socket
import threading
import argparse
import signal
import sys

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
args = parser.parse_args()

nickname = args.client
HOST = args.host
PORT = args.port

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

def write():
    while True:
        message = input('')
        if message.lower() == "exit":
            client.send("exit".encode())
            client.close()
            break
        message = f"{nickname}: {message}"
        client.send(message.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()