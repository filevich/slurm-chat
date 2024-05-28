import socket
import threading
import argparse
import signal
import sys
import random
import time

def signal_handler(client, sig=None, frame=None):
    try:
        client.send("exit".encode())
        client.close()
    except:
        pass
    finally:
        sys.exit(0)

def receive(client):
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

def write(client, nickname, n:int=10, base:int=5):
    for i in range(n):
        message = f"{nickname}: {i+1}/{n}"
        client.send(message.encode())
        random_dur = random.uniform(0, 1) # seconds
        time.sleep(base + random_dur)

    client.send("exit".encode())
    client.close()

import atexit
import resource

def print_max_memory_usage():
    max_mem_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    max_mem_mib = max_mem_kb / 1024  # Convert KiB to MiB
    print(f"Maximum memory usage: {max_mem_mib:.2f} MiB")

if __name__ == "__main__":
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

    atexit.register(print_max_memory_usage)
    signal.signal(signal.SIGINT, lambda: signal_handler(client))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    receive_thread = threading.Thread(target=receive, args=(client,))
    receive_thread.start()

    write_thread = threading.Thread(target=write, args=(client, nickname, N, 0))
    write_thread.start()

    # will execute this