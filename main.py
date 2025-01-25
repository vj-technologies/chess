if __name__ != "__main__":
    print(f"\"{__file__}\" is not meant to be imported.")
    exit(1)

from socket import socket as Socket
from chess_utils import GameState
from server import Server
from chess_refac import *
import json

BUFFSIZE = 1024
ENCODING = "utf-8"
LOGS_DIR = "logs/"

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

def chess_match(white: Socket, black: Socket) -> None:
    game = Game()
    black.send("match start".encode(ENCODING))
    white.send("match start".encode(ENCODING))
    network_error = False

    while game.state == GameState.WHITE_TURN and not network_error:
        white.send("ur turn".encode(ENCODING))
        while game.state == GameState.WHITE_TURN:
            try:
                msg = white.recv(BUFFSIZE).decode(ENCODING)
            except Exception as e:
                print(f"Network Error occoured: {e}")
                network_error = True
                break
            
            move = msg_to_move(msg)
            if game.make_move_if_valid(move, Color.WHITE):
                # TODO: Send current board configuration or latest move to the other player.
                break
            white.send("try again dumbass".encode(ENCODING))

        if game.state != GameState.BLACK_TURN or network_error:
            break

        black.send("ur turn".encode(ENCODING))
        while game.state == GameState.BLACK_TURN:
            try:
                msg = black.recv(BUFFSIZE).decode(ENCODING)
            except Exception as e:
                print(f"Network Error occoured: {e}")
                network_error = True
                break
            
            move = msg_to_move(msg)
            if game.make_move_if_valid(move, Color.BLACK):
                # TODO: Send current board configuration or latest move to the other player.
                break
            black.send("try again dumbass".encode(ENCODING))
    
    match game.state:
        case GameState.DRAW:
            white.send("draw".encode(ENCODING))
            black.send("draw".encode(ENCODING))
        case GameState.WHITE_WON:
            white.send("you won".encode(ENCODING))
            black.send("you lost".encode(ENCODING))
        case GameState.BLACK_WON:
            white.send("you lost".encode(ENCODING))
            black.send("you won".encode(ENCODING))
        case _:
            print(f"Unhandled game ending: {game.state}")

    white.close()
    black.close()


if __name__ == "__main__":
    server = Server("localhost", 8080, chess_match, ENCODING, LOGS_DIR)
    server.listen()
