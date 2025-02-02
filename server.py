if __name__ == "__main__":
    print(f"\"{__file__}\" is supposed to be imported.")
    exit(1)

from socket import socket as Socket, AF_INET, SOCK_STREAM
from datetime import datetime
from threading import Thread
from typing import Callable
import os.path

class Server(Socket):
    def __init__(self, conf: dict, match_thread_function: Callable[[Socket, Socket, str, int], None]) -> None:
        super().__init__(AF_INET, SOCK_STREAM)
        
        self.addr: tuple[str, int] = (conf["host"], conf["port"])
        self.encoding: str = conf["encoding"]
        self.buffsize: int = conf["buffsize"]
        self.time_stamp_format: str = conf["time_stamp_format"]
        self.logs_directory: str = conf["logs_directory"]

        self.bind(self.addr)
        self.match_thread_target: Callable[[Socket, Socket, str, int], None] = match_thread_function
        self.matchmaking_queue: dict[str, Socket] = {}
        self.match_threads: list[Thread] = []

        self._log_file = None
        if os.path.isdir(self.logs_directory):
            now = datetime.now()
            filename = now.strftime(conf["filename"])
            self._log_file = f"logs/{filename}.log"
            with open(self._log_file, "w+") as file:
                file.write(f"[INFO] {now.strftime(self.time_stamp_format)} Log file created.\n")
        elif conf["logs_directory"] != None:
            print("The provided logs directory couldn't be found. If you don't want log files, just put in `None`.")
            exit(1)
    
    def log(self, status: str, message: str) -> None:
        date_time_stamp = datetime.now().strftime(self.time_stamp_format)
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
    
    def handle_connection(self, conn: Socket, addr: str) -> None:
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

    def listen(self) -> None:
        self.info(f"Listening for clients on {self.addr}")
        super().listen()

        while True:
            try:
                conn, addr = self.accept()
            except KeyboardInterrupt: # this only works on Linux (tested on debian)
                self.info("Server was closed using keyboard interrupt")
                break
            else:
                self.handle_connection(conn, addr)
    
    def try_make_match(self) -> bool:
        if len(self.matchmaking_queue) < 2:
            return False
        
        # implement match making criteria here
        # we could ask each player if they wanna accept the match
        player1 = self.matchmaking_queue.popitem()
        player2 = self.matchmaking_queue.popitem()
        
        new_match_thread = Thread(target=self.match_thread_target, args=(player1[1], player2[1], self.encoding, self.buffsize))
        new_match_thread.start()
        self.match_threads.append(new_match_thread)

        self.info(f"Match created: {player1[0]} vs {player2[0]}")        
        return True
