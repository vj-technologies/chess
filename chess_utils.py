from enum import Enum

class Color(Enum):
    WHITE = 1
    BLACK = 2

class Piece:
    def __init__(self, name: str, x: int, y: int, color: Color, symbol: str) -> None:
        self.name = name
        self.symbol = symbol
        self.color = color
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"{self.name} at {self.x}, {self.y}"
    
    def __repr__(self) -> str:
        return self.symbol
    
    def move(self, x, y) -> None:
        self.x = x
        self.y = y

class GameState(Enum):
    WHITE_TURN = 1
    BLACK_TURN = 2
    WHITE_WON = 3
    BLACK_WON = 4
    DRAW = 5
