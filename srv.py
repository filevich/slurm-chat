import socket
import threading
import argparse
import datetime
import json

parser = argparse.ArgumentParser(description='TCP Chat Server')
parser.add_argument('--host', default='0.0.0.0', help='Host IP address (default: 0.0.0.0)')
parser.add_argument('--port', type=int, default=65432, help='Port number (default: 65432)')
args = parser.parse_args()

HOST = args.host
PORT = args.port

lock = threading.Lock()
clients = []
total_msgs = 0
we_re_open = None

def stringify_addr(addr:tuple[str,int]) -> str:
    return ":".join(map(str, addr))

def log(data:object) -> None:
    data = json.dumps(data)
    print(data)

def we_re_close():
    delta = datetime.datetime.now() - we_re_open
    log({
        "type": "CLOSED",
        "total": total_msgs,
        "delta": delta.total_seconds(),
    })

def broadcast(message, sender_socket):
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    client.close()
                    clients.remove(client)
                    if not clients:
                        we_re_close()

def handle(client):
    global total_msgs
    while True:
        try:
            message = client.recv(1024)
            if message.decode() == "exit":
                log({
                    "type": "CONN_CLOSED",
                    "addr": stringify_addr(client.getpeername())
                })
                with lock:
                    clients.remove(client)
                    if not clients:
                        we_re_close()
                client.close()
                break
            else:
                broadcast(message, client)
                with lock:
                    n = len(clients)
                    total_msgs += 1
                    delta = datetime.datetime.now() - we_re_open
                    delta = delta.total_seconds()
                    log({
                        "type": "IN",
                        "n":     n,
                        "total": total_msgs,
                        "delta": delta,
                        "msg":   message.decode()
                    })
        except:
            with lock:
                clients.remove(client)
                if not clients:
                    we_re_close()
            client.close()
            break

def receive():
    global we_re_open, total_msgs
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    log({
        "type": "START",
        "addr": f"{HOST}:{PORT}"
    })

    while True:
        client, addr = server_socket.accept()
        with lock:
            clients.append(client)
            if len(clients) == 1:
                total_msgs = 0
                we_re_open = datetime.datetime.now()
                log({
                    "type":  "OPENED",
                    "total": total_msgs,
                    "time":  str(we_re_open),
                })
        
        log({
            "type": "NEW_CONN",
            "addr": stringify_addr(addr)
        })
        
        client.send("Connected to the server!".encode())
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
