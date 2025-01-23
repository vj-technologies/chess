from enum import Enum

class Color(Enum):
    WHITE = 1
    BLACK = 2

class Piece:
    def __init__(self, name: str, x: int, y: int, color: Color, symbol: str,token:int) -> None:
        self.name = name
        self.symbol = symbol
        self.color = color
        self.x = x
        self.y = y
        self.Token = token
    
    def __str__(self) -> str:
        return f"{self.name} at {self.x}, {self.y}"
    
    def __repr__(self) -> str:
        return self.symbol
    
    def move(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def get_thrown(self) -> None:
        self.x = None
        self.y = None

class GameState(Enum):
    WHITE_TURN = 1
    BLACK_TURN = 2
    WHITE_WON = 3
    BLACK_WON = 4
    DRAW = 5

class Match:
    '''
    Chess match, that gets created when both players accepted the match.
    '''
   
    def __init__(self, white: int, black: int) -> None:
        self.board = []
        self.white_client_index = white
        self.black_client_index = black
        self.game_state: GameState = GameState.WHITE_TURN
   
    def submit_move(start: tuple[int, int], end: tuple[int, int], player: Color) -> bool:
        # check if its his turn
        pass
