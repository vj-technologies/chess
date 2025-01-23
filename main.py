if __name__ != "__main__":
    print(f"\"{__file__}\" is not meant to be imported.")
    exit(1)

from socket import socket as Socket
from threading import Thread
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

def chess_match(white: tuple[Socket, str], black: tuple[Socket, str]) -> None:
    game = Game()
    black[0].send(r"match start")
    white[0].send(r"match start")

    while game.state in [GameState.WHITE_TURN, GameState.BLACK_TURN]:
        white[0].send(r"ur turn")
        while game.state == GameState.WHITE_TURN:
            msg = white[0].recv(BUFFSIZE).decode(ENCODING)
            move = msg_to_move(msg)
            if move != None and game.make_move_if_valid(move, Color.WHITE):
                break
            white[0].send(r"try again dumbass")

        if game.state not in [GameState.WHITE_TURN, GameState.BLACK_TURN]:
            break

        black[0].send(r"ur turn")
        while game.state == GameState.BLACK_TURN:
            msg = black[0].recv(BUFFSIZE)
            was_move_valid = game.make_move_if_valid(msg, Color.BLACK)
            if not was_move_valid:
                black[0].send(r"try again dumbass")
    
    match game.state:
        case GameState.DRAW:
            white[0].send(r"draw")
            black[0].send(r"draw")
        case GameState.WHITE_WON:
            white[0].send(r"you won")
            black[0].send(r"you lost")
        case GameState.BLACK_WON:
            white[0].send(r"you lost")
            black[0].send(r"you won")
        case _:
            print("unhandled game ending")

    white[0].close()
    black[0].close()


if __name__ == "__main__":
    server = Server("localhost", 8080, chess_match, ENCODING)
    server_thread = Thread(target=server.listen)
    server_thread.start()
