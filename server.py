from threading import Thread
from socket import socket as Socket, AF_INET, SOCK_STREAM
from typing import Callable

def default_handler(player1: tuple[Socket, str], player2: tuple[Socket, str]) -> None:
    player1.close()
    player2.close()

class Server(Socket):
    def __init__(self,
            host: str, port: int,
            match_thread_function: Callable[
                [tuple[Socket, str], tuple[Socket, str]],
                None] = default_handler
        ) -> None:
        super().__init__(AF_INET, SOCK_STREAM)
        self.bind((host, port))
        self.match_thread_target = match_thread_function
        self.matchmaking_queue: dict[str, Socket] = []
        self.match_threads: list[Thread] = []

        # self.matched: dict[tuple[Socket, str], int] = {}
    
    def info(self, message: str) -> None:
        print(f"[SERVER] {message}")
    
    def listen(self) -> None:
        super().listen()

        while True:
            self.info("Listening for clients...")
            conn, addr = self.accept()
            self.info("New connection: {addr}")
            if addr in self.matchmaking_queue.keys():
                self.matchmaking_queue.pop(addr)
                conn.send(r"removed your from queue")
                self.info("Removed {addr} from queue")
            else:
                self.matchmaking_queue[addr] = conn
                conn.send(r"added to queue")
                self.info("Added {addr} to queue")
                self.try_make_match()
    
    def try_make_match(self) -> bool:
        if len(self.matchmaking_queue) < 2:
            return False
        
        # implement match making criteria here
        # we could ask each player if they wanna accept the match
        player1 = self.matchmaking_queue.popitem()
        player2 = self.matchmaking_queue.popitem()

        self.match_threads.append(
            Thread(target=self.match_thread_target, args=(player1, player2))
        )
        self.match_threads[-1].start()

        return True

if __name__ == "__main__":
    server = Server("localhost", 8080)
    server.listen()
