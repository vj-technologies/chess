if __name__ != "__main__":
    print(f"\"{__file__}\" is not meant to be imported.")
    exit(1)

from socket import socket as Socket
from chess_utils import GameState
from server import Server
from chess_refac import *
import json

SERVER_CONFIG_FILE = "server.conf"
DEFAULT_SERVER_CONF = {
    "host": "127.0.0.1",
    "port": 9999,
    "buffsize": 1024,
    "encoding": "utf-8",
    "logs_dir": "logs/",
    "filename": "%Y_%m_%d_%Hh%Mm%Ss",
    "time_stamp_format": "%d.%m.%Y %H:%M:%S"
}

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


if __name__ == "__main__":
    conf = DEFAULT_SERVER_CONF

    # load server configuration values
    with open(SERVER_CONFIG_FILE, "r") as file:
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
