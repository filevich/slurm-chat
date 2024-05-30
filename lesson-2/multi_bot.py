import argparse
import signal
import sys
import atexit
import resource
from conn import Conn
import random
import time
import hashlib

def print_max_memory_usage():
    max_mem_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    max_mem_mib = max_mem_kb / 1024  # Convert KiB to MiB
    print(f"Maximum memory usage: {max_mem_mib:.2f} MiB")

def signal_handler(client, sig=None, frame=None):
    try:
        client.send("exit".encode())
        client.close()
    except:
        pass
    finally:
        sys.exit(0)

def parse_servers(servers:str) -> list[tuple[str,int]]:
    """comma separated host:port tuples"""
    servers = servers.split(',')
    servers = [server.strip().split(':') for server in servers]
    servers = [(server[0],int(server[1])) for server in servers]
    return servers

def sha256_int(input_string:str) -> int:
    sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()
    hash_int = int(sha256_hash, 16)
    return hash_int

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TCP Chat Client')
    parser.add_argument('client', help='Client name')
    parser.add_argument('--servers', default='0.0.0.0', help='list of host:port separated by comma of server to connect to')
    parser.add_argument('--num_msgs', type=int, default=100, help='Total number of messages')
    args = parser.parse_args()

    atexit.register(print_max_memory_usage)

    num_msgs = args.num_msgs
    nick     = args.client
    servers  = parse_servers(args.servers)
    n        = len(servers)
    base     = 0
    conns    = []
    
    for server in servers:
        host,port = server
        conn = Conn(host, port, nick)
        conn.run() # non-blocking
        conns += [conn]
    
    # sending the msgs

    total_sent = 0

    for i in range(num_msgs):
        message = f"{nick}: {i+1}/{num_msgs}"
        # obtain a random server to send it to
        i = sha256_int(message) % n
        conns[i].client.send(message.encode())
        random_dur = random.uniform(0, 1) # seconds
        total_sent += 1
        print(f"sent {total_sent}")
        time.sleep(base + random_dur)

    # closing conns...

    for conn in conns:
        conn.client.send("exit".encode())
        conn.client.close()

    signal.signal(signal.SIGINT, lambda: signal_handler(conn.client))
