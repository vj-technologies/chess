if __name__ != "__main__":
    print(f"\"{__file__}\" is not meant to be imported.")
    exit(1)

from socket import socket as Socket
from threading import Thread
import json

from server import Server
from chess_refac import *

def todo(task):
    print(f"[TODO] {task}")
    exit()

Open_game_token: float | None = None

matches_looking_for_opponent = []
# "example",

matches = {}
# "example": { "board_token": "1671365", "w": addr1, "b": addr2, "s": [addr3] },

active_player_tokens = {}
# addr1: { "match": "example", "type": "w" },
# addr2: { "match": "example", "type": "b" },
# addr3: { "match": "example", "type": "s" },

def join_match(addr: tuple[str, int]):
    active_player_tokens[addr] = {
        "match": "???",
        "type": "?"
    }
    pass

def handle_client(conn: Socket, addr: tuple[str, int], client_idx: int) -> None:
    try:
        request: dict = json.loads(conn.recv(1024).decode("utf-8"))
    except Exception:
        # TODO: close any open matches
        conn.close()
        return

    response: dict | None = None

    match request["type"]:
        case "quit":
            # TODO: close any open matches
            conn.close()
            return
        case "move":
            response = {
                "type": "move-feedback",
                "message": submit_move(request["player_token"], request["start"], request["end"])
            }
        case "join matchmaking":
            # search for matches to join
            if len(matches_looking_for_opponent) > 0:
                join_match(addr, )
                pass # join first match and remove from list
            # if we can't find one, just create one and make it so that others can join
            pass
        case _:
            response = {"type": "bad request"}
    
    if response != None:
        conn.send(json.dumps(response).encode("utf-8"))
    conn.close()

# Start server
server = Server("localhost", 8080, handle_client)
server_thread = Thread(target=server.listen)
server_thread.start()

'''
elif request["type"] == "move":
    if match_token == None: # client in an active match?
        response = {"type": "move blocked", "message": "not in a match"}
    
    try:
        start_x = int(request["start_x"])
        start_y = int(request["start_y"])
        end_x = int(request["end_x"])
        end_y = int(request["end_y"])
    except Exception:
        response = {"type": "move_blocked", "message": "bad request"}
    else:
        feedback = submit_move(
            match_token,
            (start_x, start_y), (end_x, end_y),
            Color.WHITE # or black idk how to determine for now
        )

        if feedback == "success":
            response = {"type": "success"}
        elif feedback == "illegal_move":
            response = {"type": "move blocked", "message": "illegal move"}
        elif feedback == "not_ur_turn":
            response = {"type": "move blocked", "message": "not ur turn"}
        else:
            response = {"type": "move blocked", "message": "unknown error"}
elif request["type"] == "matchmaking join":
    available_for_matchmaking = True
elif request["type"] == "matchmaking leave":
    available_for_matchmaking = False
elif request["type"] == "match accept":
    pass
elif request["type"] == "set options":
    # set match making options
    pass'''