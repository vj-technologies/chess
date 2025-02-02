from socket import socket as Socket, AF_INET, SOCK_STREAM
from datetime import datetime
from threading import Thread
from typing import Callable
import os.path, json

from chess_utils import GameState
from chess_refac import *

def msg_to_move(msg: str) -> dict | None:
    try:
        move: dict = json.loads(msg)
    except Exception:
        return None

    if not isinstance(move["start_x"], int) or 7 < move["start_x"] or move["start_x"] < 0: return None
    if not isinstance(move["start_y"], int) or 7 < move["start_y"] or move["start_y"] < 0: return None
    if not isinstance(move["end_x"  ], int) or 7 < move["end_x"  ] or move["end_x"  ] < 0: return None
    if not isinstance(move["end_y"  ], int) or 7 < move["end_y"  ] or move["end_y"  ] < 0: return None
    
    return move

def chess_match(white: Socket, black: Socket, encoding: str, buffsize: int) -> None:
    game = Game()
    black.send("match start".encode(encoding))
    white.send("match start".encode(encoding))
    network_error = False

    while game.state == GameState.WHITE_TURN and not network_error:
        white.send("ur turn".encode(encoding))
        while game.state == GameState.WHITE_TURN:
            try:
                msg = white.recv(buffsize).decode(encoding)
            except Exception as e:
                print(f"Network Error occoured: {e}")
                network_error = True
                break
            
            move = msg_to_move(msg)
            if game.make_move_if_valid(move, Color.WHITE):
                # TODO: Send current board configuration or latest move to the other player.
                break
            white.send("try again dumbass".encode(encoding))

        if game.state != GameState.BLACK_TURN or network_error:
            break

        black.send("ur turn".encode(encoding))
        while game.state == GameState.BLACK_TURN:
            try:
                msg = black.recv(buffsize).decode(encoding)
            except Exception as e:
                print(f"Network Error occoured: {e}")
                network_error = True
                break
            
            move = msg_to_move(msg)
            if game.make_move_if_valid(move, Color.BLACK):
                # TODO: Send current board configuration or latest move to the other player.
                break
            black.send("try again dumbass".encode(encoding))
    
    match game.state:
        case GameState.DRAW:
            white.send("draw".encode(encoding))
            black.send("draw".encode(encoding))
        case GameState.WHITE_WON:
            white.send("you won".encode(encoding))
            black.send("you lost".encode(encoding))
        case GameState.BLACK_WON:
            white.send("you lost".encode(encoding))
            black.send("you won".encode(encoding))
        case _:
            print(f"Unhandled game ending: {game.state}")

    white.close()
    black.close()

class Server(Socket):
    def __init__(self, conf: dict, match_thread_function: Callable[[Socket, Socket, str, int], None]) -> None:
        super().__init__(AF_INET, SOCK_STREAM)
        
        # Explicitly take needed values for readability & autocomlete
        self.addr: tuple[str, int] = (conf["host"], conf["port"])
        self.encoding: str = conf["encoding"]
        self.buffsize: int = conf["buffsize"]
        self.time_stamp_format: str = conf["time_stamp_format"]
        self.logs_dir: str = conf["logs_directory"]

        self.bind(self.addr)
        self.match_thread_target: Callable[[Socket, Socket, str, int], None] = match_thread_function
        self.matchmaking_queue: dict[str, Socket] = {}
        self.match_threads: list[Thread] = []

        self._log_file = None
        if os.path.isdir(self.logs_dir):
            now = datetime.now()
            filename = now.strftime(conf["filename"])
            self._log_file = f"logs/{filename}.log"
            with open(self._log_file, "w+") as file:
                file.write(f"[INFO] {now.strftime(self.time_stamp_format)} Log file created.\n")
        elif self.logs_dir != None:
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

if __name__ == "__main__":
    # Define the server's default configuration values here:
    conf = {
        "host": "127.0.0.1",
        "port": 9999,
        "buffsize": 1024,
        "encoding": "utf-8",
        "logs_dir": "logs/",
        "filename": "%Y_%m_%d_%Hh%Mm%Ss",
        "time_stamp_format": "%d.%m.%Y %H:%M:%S"
    }

    # load server configuration values
    server_config_file = "server.conf"
    if os.path.isfile(server_config_file):
        with open(server_config_file, "r") as file:
            for line in file.readlines():
                line = line.strip()
                val_key = line.split("=", 1)
                conf[val_key[0]] = val_key[1]
    
    try:
        conf["port"] = int(conf["port"])
        conf["buffsize"] = int(conf["buffsize"])
    except Exception as e:
        print(e)
    else:
        server = Server(conf, chess_match)
        server.listen()
