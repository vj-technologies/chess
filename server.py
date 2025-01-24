if __name__ == "__main__":
    print(f"\"{__file__}\" is supposed to be imported.")
    exit(1)

from threading import Thread
from socket import socket as Socket, AF_INET, SOCK_STREAM
from typing import Callable

def default_handler(player1: Socket, player2: Socket) -> None:
    player1.close()
    player2.close()

class Server(Socket):
    def __init__(self,
            host: str, port: int,
            match_thread_function: Callable[[Socket, Socket], None] = default_handler,
            encoding: str = "utf-8"
        ) -> None:
        super().__init__(AF_INET, SOCK_STREAM)
        self.addr = (host, port)
        self.bind(self.addr)
        self.match_thread_target = match_thread_function
        self.encoding = encoding
        self.matchmaking_queue: dict[str, Socket] = {}
        self.match_threads: list[Thread] = []
    
    def info(self, message: str) -> None:
        print(f"[SERVER] {message}")
    
    def listen(self) -> None:
        self.info(f"Listening on ({self.addr})")
        super().listen()

        while True:
            self.info("Listening for clients...")
            conn, addr = self.accept()
            self.info(f"New connection: {addr}")

            if addr in self.matchmaking_queue:
                self.matchmaking_queue.pop(addr)
                conn.send("removed your from queue".encode(self.encoding))
                self.info(f"Removed {addr} from queue")
            else:
                self.matchmaking_queue[addr] = conn
                conn.send("added to queue".encode(self.encoding))
                self.info(f"Added {addr} to queue")

                self.try_make_match()
    
    def try_make_match(self) -> bool:
        if len(self.matchmaking_queue) < 2:
            return False
        
        # implement match making criteria here
        # we could ask each player if they wanna accept the match
        player1 = self.matchmaking_queue.popitem()
        player2 = self.matchmaking_queue.popitem()
        
        new_match_thread = Thread(target=self.match_thread_target, args=(player1[1], player2[1]))
        new_match_thread.start()
        self.match_threads.append(new_match_thread)

        self.info(f"Match created: {player1[0]} vs {player2[0]}")        
        return True
