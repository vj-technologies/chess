if __name__ != "__main__":
    print(f"\"{__file__}\" is not meant to be imported.")
    exit(1)

from socket import socket as Socket
import json

from chess_utils import GameState
from server import Server
from chess_refac import *

BUFFSIZE = 1024
ENCODING = "utf-8"

def msg_to_move(msg: str) -> dict | None:
    move: dict = json.loads(msg)

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
    match_over_check = lambda: (game.state in [GameState.WHITE_TURN, GameState.BLACK_TURN]) and not network_error

    while match_over_check():
        white.send("ur turn".encode(ENCODING))
        while game.state == GameState.WHITE_TURN:
            try:
                msg = white.recv(BUFFSIZE).decode(ENCODING)
            except Exception:
                network_error = True
                break
            move = msg_to_move(msg)
            if move and game.make_move_if_valid(move, Color.WHITE):
                break
            white.send("try again dumbass".encode(ENCODING))

        if match_over_check(): break

        black.send("ur turn".encode(ENCODING))
        while game.state == GameState.BLACK_TURN:
            try:
                msg = black.recv(BUFFSIZE).decode(ENCODING)
            except Exception:
                network_error = True
                break
            move = msg_to_move(msg)
            if move and game.make_move_if_valid(move, Color.BLACK):
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
            print("unhandled game ending")

    white.close()
    black.close()


if __name__ == "__main__":
    server = Server("localhost", 8080, chess_match, ENCODING)
    server.listen()
