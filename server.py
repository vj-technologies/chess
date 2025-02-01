if __name__ == "__main__":
    print(f"\"{__file__}\" is supposed to be imported.")
    exit(1)

from socket import socket as Socket, AF_INET, SOCK_STREAM
from datetime import datetime
from threading import Thread
from typing import Callable
import os.path

TIME_STAMP_FORMAT = "%d.%m.%Y %H:%M:%S"

def default_handler(player1: Socket, player2: Socket) -> None:
    player1.close()
    player2.close()

class Server(Socket):
    def __init__(self,
            host: str, port: int,
            match_thread_function: Callable[[Socket, Socket], None] = default_handler,
            encoding: str = "utf-8",
            logs_directory: str = None
        ) -> None:
        super().__init__(AF_INET, SOCK_STREAM)
        self.addr = (host, port)
        self.bind(self.addr)
        self.match_thread_target = match_thread_function
        self.encoding = encoding
        self.matchmaking_queue: dict[str, Socket] = {}
        self.match_threads: list[Thread] = []

        self._log_file = None
        if os.path.isdir(logs_directory):
            now = datetime.now()
            filename = now.strftime('%Y %m %d %Hh%Mm%Ss')
            self._log_file = f"logs/{filename}.log"
            with open(self._log_file, "w+") as file:
                file.write(f"[INFO] {now.strftime(TIME_STAMP_FORMAT)} Log file created.\n")
        elif logs_directory != None:
            print("The provided logs directory couldn't be found. If you don't want log files, just put in `None`.")
            exit(1)
    
    def log(self, status: str, message: str) -> None:
        date_time_stamp = datetime.now().strftime(TIME_STAMP_FORMAT)
        log = f"[{status}] {date_time_stamp} {message}"
        print(log)
        if self._log_file:
            with open(self._log_file, 'a') as logs:
                logs.write(f"{log}\n")

    def info(self, message: str) -> None:
        self.log("INFO", message)

    def warn(self, message: str) -> None:
        self.log("WARN", message)

    def error(self, message: str) -> None:
        self.log("ERROR", message)
    
    def listen(self) -> None:
        self.info(f"Listening for clients on {self.addr}")
        super().listen()

        while True:
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
