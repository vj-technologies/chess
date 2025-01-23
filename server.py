from threading import Thread
from socket import socket as Socket, AF_INET, SOCK_STREAM
from typing import Callable

def default_handler(conn: Socket) -> None:
    conn.close()

class Server(Socket):
    def __init__(self, host: str, port: int, handler: Callable[[Socket, int], None] = default_handler) -> None:
        super().__init__(AF_INET, SOCK_STREAM)
        self.bind((host, port))
        self.threads: list[Thread] = []
        self.handler = handler
    
    def listen(self) -> None:
        self.listen()

        while True:
            conn, addr = self.accept()
            client_idx = len(self.threads)
            print(f"[SERVER] New connection: {addr} ({client_idx=})")
            thread = Thread(target=self.handler, args=(conn, addr, client_idx))
            thread.start() # this server is vulnerable to race conditions
            self.threads.append(thread)

if __name__ == "__main__":
    server = Server("localhost", 8080)
    server.listen()
