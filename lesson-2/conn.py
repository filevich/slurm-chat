import threading
import socket
import time
import random

class Conn:
    def __init__(self, host:str, port:str, nick:str) -> None:
        self.nick = nick
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive(self) -> None:
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message == "NICKNAME":
                    self.client.send(self.nickname.encode())
                else:
                    print(message)
            except:
                print("Disconnected from the server")
                self.client.close()
                break
    
    # def write(self, n:int=10, base:int=0) -> None:
    #     for i in range(n):
    #         message = f"{self.nick}: {i+1}/{n}"
    #         self.client.send(message.encode())
    #         random_dur = random.uniform(0, 1) # seconds
    #         time.sleep(base + random_dur)

    #     self.client.send("exit".encode())
    #     self.client.close()

    def run(self) -> None:
        receive_thread = threading.Thread(target=self.receive, args=())
        receive_thread.start()
        # write_thread = threading.Thread(target=self.write, args=(n, base))
        # write_thread.start()
        # non blocking! so this function will exit but threads will keep running