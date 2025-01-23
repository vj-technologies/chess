from typing import Literal
from random import random

from chess_utils import Color, Piece

# Pieces_on_board = []
# Last_board_position = []
Games_of_chess = {}


def setup_a_game():
    pieces_on_board = []
    Last_board_position = []
    Session = []
    cur_token= create_token()

    for i in range(8):
        pieces_on_board.append(Pawn(1, i, Color.WHITE,cur_token))
        pieces_on_board.append(Pawn(6, i, Color.BLACK,cur_token))

    pieces_on_board.append(Rook(0, 0, Color.WHITE,cur_token))
    pieces_on_board.append(Rook(0, 7, Color.WHITE,cur_token))
    pieces_on_board.append(Rook(7, 0, Color.BLACK,cur_token))
    pieces_on_board.append(Rook(7, 7, Color.BLACK,cur_token))

    pieces_on_board.append(Knight(0, 1, Color.WHITE,cur_token))
    pieces_on_board.append(Knight(0, 6, Color.WHITE,cur_token))
    pieces_on_board.append(Knight(7, 1, Color.BLACK,cur_token))
    pieces_on_board.append(Knight(7, 6, Color.BLACK,cur_token))

    pieces_on_board.append(Bishop(0, 2, Color.WHITE,cur_token))
    pieces_on_board.append(Bishop(0, 5, Color.WHITE,cur_token))
    pieces_on_board.append(Bishop(7, 2, Color.BLACK,cur_token))
    pieces_on_board.append(Bishop(7, 5, Color.BLACK,cur_token))

    pieces_on_board.append(Queen(0, 3, Color.WHITE,cur_token))
    pieces_on_board.append(Queen(7, 3, Color.BLACK,cur_token))

    pieces_on_board.append(King(0, 4, Color.WHITE,cur_token))
    pieces_on_board.append(King(7, 4, Color.BLACK,cur_token))
    
    Session=[pieces_on_board, Last_board_position]
    # token = create_token()
    Games_of_chess[cur_token] = Session
    return cur_token


def create_token():
    token = random()
    if token in Games_of_chess.keys():
        token = create_token()
    return token


def checkmate(x: int, y: int, color: Color) -> bool:  
    '''
    checks if a given cordinate is in check and gives a bool \n
    x , y , Color of the king -> Boolean
    '''  
    for i in range(8):
        if i + x > 7:
           break
        piece_y = find_piece_on_square(x + i, y)
        if piece_y != None:
            if piece_y.color != color:
                if piece_y.name == "Rook" or piece_y.name == "Queen":
                    return True
                else:
                    break
            else:
                break
    
    for i in range(8):
        if x < i:
           break
        piece_y = find_piece_on_square(x - i, y)
        if piece_y != None:
            if piece_y.color != color:
                if piece_y.name == "Rook" or piece_y.name == "Queen":
                    return True
                else:
                    break
            else:
                break
    
    for i in range(8):
        if i + y > 7:
           break 
        piece_y = find_piece_on_square(x, y + i)
        if piece_y != None:
            if piece_y.color != color:
                if piece_y.name == "Rook" or piece_y.name == "Queen":
                    return True
                else:
                    break
            else:
                break
    
    for i in range(8):
        if y - i < 0:
           break 
        piece_y = find_piece_on_square(x, y - i)
        if piece_y != None:
            if piece_y.color != color:
                if piece_y.name == "Rook" or piece_y.name == "Queen":
                    return True
                else:
                    break
            else:
                break
    
    for i in range(8):
        if x + i > 7 or y + i > 7:
           break 
        piece_y = find_piece_on_square(x + i, y + i)
        if piece_y != None:
            if piece_y.color != color:
                if piece_y.name == "Bishop" or piece_y.name == "Queen":
                    return True
                else:
                    break
            else:
                break
    
    for i in range(8):
        if x - i < 0 or y - i < 0:
           break 
        piece_y = find_piece_on_square(x - i, y - i)
        if piece_y != None:
            if piece_y.color != color:
                if piece_y.name == "Bishop" or piece_y.name == "Queen":
                    return True
                else:
                    break
            else:
                break
    
    for i in range(8):
        if x + i > 7 or y - i < 0:
           break 
        piece_y = find_piece_on_square(x + i, y - i)
        if piece_y != None:
            if piece_y.color != color:
                if piece_y.name == "Bishop" or piece_y.name == "Queen":
                    return True
                else:
                    break
            else:
                break
    
    for i in range(8):
        if x - i < 0 or y + i > 7:
           break 
        piece_y = find_piece_on_square(x - i, y + i)
        if piece_y != None:
            if piece_y.color != color:
                if piece_y.name == "Bishop" or piece_y.name == "Queen":
                    return True
                else:
                    break
            else:
                break
    
    if color == Color.WHITE:
        pawn_piece = find_piece_on_square(x + 1, y + 1)
        if pawn_piece != None:
            if pawn_piece.color == Color.BLACK and pawn_piece.name == "Pawn":
                return True
        pawn_piece = find_piece_on_square(x + 1, y - 1)
        if pawn_piece != None:
            if pawn_piece.color == Color.BLACK and pawn_piece.name == "Pawn":
                return True
    elif color == Color.BLACK:
        pawn_piece = find_piece_on_square(x - 1, y + 1)
        if pawn_piece != None:
            if pawn_piece.color == Color.WHITE and pawn_piece.name == "Pawn":
                return True
        pawn_piece = find_piece_on_square(x - 1, y - 1)
        if pawn_piece != None:
            if pawn_piece.color == Color.WHITE and pawn_piece.name == "Pawn":
                return True
    
    knight_piece = find_piece_on_square(x + 2, y + 1)
    if knight_piece != None:
        if knight_piece.color != color and knight_piece.name == "Knight":
            return True
    knight_piece = find_piece_on_square(x + 2, y - 1)
    if knight_piece != None:
        if knight_piece.color != color and knight_piece.name == "Knight":
            return True
    knight_piece = find_piece_on_square(x - 2, y + 1)
    if knight_piece != None:
        if knight_piece.color != color and knight_piece.name == "Knight":
            return True
    knight_piece = find_piece_on_square(x - 2, y - 1)
    if knight_piece != None:
        if knight_piece.color != color and knight_piece.name == "Knight":
            return True
    knight_piece = find_piece_on_square(x + 1, y + 2)
    if knight_piece != None:
        if knight_piece.color != color and knight_piece.name == "Knight":
            return True
    knight_piece = find_piece_on_square(x + 1, y - 2)
    if knight_piece != None:
        if knight_piece.color != color and knight_piece.name == "Knight":
            return True
    knight_piece = find_piece_on_square(x - 1, y + 2)
    if knight_piece != None:
        if knight_piece.color != color and knight_piece.name == "Knight":
            return True
    knight_piece = find_piece_on_square(x - 1, y - 2)
    if knight_piece != None:
        if knight_piece.color != color and knight_piece.name == "Knight":
            return True
    return False


class Pawn(Piece):
    def __init__(self, x: int, y: int, color: Color,token:int) -> None:
        super().__init__("Pawn", x, y, color, "P" if color == Color.WHITE else "p", token)
    
    def get_thrown(self) -> None:
        super().get_thrown()
        Games_of_chess[self.token][0].remove(self)
    
    def check_if_legal(self, x, y, board) -> None | bool:
        curr_holder = find_piece_on_square(x, y, board)

        if self.color == Color.WHITE:
            if x == self.x + 1 and y == self.y and curr_holder == None:
                return True
            elif x == self.x + 1 and (y == (self.y - 1) or (y == self.y + 1) ) and curr_holder.color == Color.BLACK:
                curr_holder.get_thrown()
                return True
            elif self.x == 1 and y == self.y and x == self.x + 2 and curr_holder == None:
                return True
            else:
                return False
        
        elif self.color == Color.BLACK:
            if x == self.x - 1 and y == self.y and curr_holder == None:
                return True
            elif x == self.x - 1 and (y == (self.y - 1) or (y == self.y + 1)) and curr_holder.color == Color.WHITE:
                curr_holder.get_thrown()
                return True
            elif self.x == 1 and y == self.y and x == self.x - 2 and curr_holder == None:
                return True
            else:
                return False

class Rook(Piece):
    def __init__(self, x: int, y: int, color: Color,token:int) -> None:
        self.casteling = True
        super().__init__("Rook", x, y, color, "R" if color == Color.WHITE else "r",token)
    
    def get_thrown(self) -> None:
        super().get_thrown()
        Games_of_chess[self.token][0].remove(self)
    
    def check_if_legal(self, x, y) -> bool:
        legal_moves = []
        for i in range(1 , 8 - self.x):
            if find_piece_on_square(self.x + i, self.y) != None:
                if find_piece_on_square(self.x + i, self.y).color == self.color:
                    break
                elif find_piece_on_square(self.x + i, self.y).color != self.color:
                    legal_moves.append((self.x + i, self.y))
                    break
            else:
                legal_moves.append((self.x + i, self.y))
        
        for i in range(1, self.x + 1):
            if find_piece_on_square(self.x - i, self.y) != None:
                if find_piece_on_square(self.x - i, self.y).color == self.color:
                    break
                elif find_piece_on_square(self.x - i, self.y).color != self.color:
                    legal_moves.append((self.x - i, self.y))
                    break
                else:
                    print("something went wrong")
            else:
                legal_moves.append((self.x - i, self.y))
        
        for i in range(1, 8 - self.y):
            if find_piece_on_square(self.x, self.y + i) != None:
                if find_piece_on_square(self.x, self.y + i).color == self.color:
                    break
                elif find_piece_on_square(self.x, self.y + i).color != self.color:
                    legal_moves.append((self.x, self.y + i))
                    break
            else:
                legal_moves.append((self.x, self.y + i))
        
        for i in range(1, self.y + 1):
            if find_piece_on_square(self.x, self.y - i) != None:
                if find_piece_on_square(self.x, self.y - i).color == self.color:
                    break
                elif find_piece_on_square(self.x, self.y - i).color != self.color:
                    legal_moves.append((self.x, self.y - i))
                    break
            else:
                legal_moves.append((self.x, self.y - i))
        
        if (x, y) in legal_moves:
            if find_piece_on_square(x, y) != None:
                find_piece_on_square(x, y).get_thrown()
            return True
        else:
            return False

    def move(self, x, y) -> None:
        self.x = x
        self.y = y
        self.casteling = False

class Knight(Piece):
    def __init__(self, x: int, y: int, color: Color,token:int) -> None:
        super().__init__("Knight", x, y, color, "N" if color == Color.WHITE else "n",token)
    
    def get_thrown(self) -> None:
        super().get_thrown()
        Games_of_chess[self.token][0].remove(self)
    
    def check_if_legal(self, x, y) -> None | bool:
        curr_holder = find_piece_on_square(x, y)
        
        if x > 7 or x < 0 or y > 7 or y < 0:
            return False
        
        booly = False
        if   x == self.x + 2 and y == self.y + 1: booly = True
        elif x == self.x + 2 and y == self.y - 1: booly = True
        elif x == self.x - 2 and y == self.y + 1: booly = True
        elif x == self.x - 2 and y == self.y - 1: booly = True
        elif x == self.x + 1 and y == self.y + 2: booly = True
        elif x == self.x + 1 and y == self.y - 2: booly = True
        elif x == self.x - 1 and y == self.y + 2: booly = True
        elif x == self.x - 1 and y == self.y - 2: booly = True
        
        if booly:
            if curr_holder != None:
                if curr_holder.color != self.color:
                    curr_holder.get_thrown()
                    return True
                elif curr_holder.color == self.color:
                    return False
            else:
                return True

class Bishop(Piece):
    def __init__(self, x: int, y: int, color: Color,token:int) -> None:
        super().__init__("Bishop", x, y, color, "B" if color == Color.WHITE else "b",token)
    
    def get_thrown(self) -> None:
        super().get_thrown()
        Games_of_chess[self.token][0].remove(self)
    
    def check_if_legal(self, x, y) -> bool:
        legal_moves = []
        
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            if find_piece_on_square(self.x + i, self.y + i,self.Token) != None:
                if find_piece_on_square(self.x + i, self.y + i).color == self.color:
                    break
                elif find_piece_on_square(self.x + i, self.y + i,self.Token).color != self.color:
                    legal_moves.append((self.x + i, self.y + i))
                    break
            else:
                legal_moves.append((self.x + i, self.y + i))
        
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            if find_piece_on_square(self.x + i, self.y - i,self.Token) != None:
                if find_piece_on_square(self.x + i, self.y - i,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x + i, self.y - i,self.Token).color != self.color:
                    legal_moves.append((self.x + i, self.y - i))
                    break
            else:
                legal_moves.append((self.x + i, self.y - i))
                
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            if find_piece_on_square(self.x - i, self.y + i,self.Token) != None:
                if find_piece_on_square(self.x - i, self.y + i,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x - i, self.y + i,self.Token).color != self.color:
                    legal_moves.append((self.x - i, self.y + i))
                    break
            else:
                legal_moves.append((self.x - i, self.y + i))
        
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            if find_piece_on_square(self.x - i, self.y - i,self.Token) != None:
                if find_piece_on_square(self.x - i, self.y - i,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x - i, self.y - i,self.Token).color != self.color:
                    legal_moves.append((self.x - i, self.y - i))
                    break
            else:
                legal_moves.append((self.x - i, self.y - i))
        
        if (x, y) in legal_moves:
            if find_piece_on_square(x, y,) != None:
                find_piece_on_square(x, y).get_thrown()
            return True
        else:
            return False

class Queen(Piece):
    def __init__(self, x: int, y: int, color: Color,token:int) -> None:
        super().__init__("Queen", x, y, color, "Q" if color == Color.WHITE else "q",token)
    
    def get_thrown(self) -> None:
        super().get_thrown()
        Games_of_chess[self.token][0].remove(self)
    
    def check_if_legal(self, x, y):
        legal_moves = []
        
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            if find_piece_on_square(self.x + i, self.y + i,self.Token) != None:
                if find_piece_on_square(self.x + i, self.y + i,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x + i, self.y + i,self.Token).color != self.color:
                    legal_moves.append((self.x + i, self.y + i))
                    break
            else:
                legal_moves.append((self.x + i, self.y + i))
        
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            if find_piece_on_square(self.x + i, self.y - i,self.Token) != None:
                if find_piece_on_square(self.x + i, self.y - i).color == self.color:
                    break
                elif find_piece_on_square(self.x + i, self.y - i,self.Token).color != self.color:
                    legal_moves.append((self.x + i, self.y - i))
                    break
            else:
                legal_moves.append((self.x + i, self.y - i))
                
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            if find_piece_on_square(self.x - i, self.y + i,self.Token) != None:
                if find_piece_on_square(self.x - i, self.y + i,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x - i, self.y + i,self.Token).color != self.color:
                    legal_moves.append((self.x - i, self.y + i))
                    break
            else:
                legal_moves.append((self.x - i, self.y + i))
        
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            if find_piece_on_square(self.x - i, self.y - i,self.Token) != None:
                if find_piece_on_square(self.x - i, self.y - i,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x - i, self.y - i,self.Token).color != self.color:
                    legal_moves.append((self.x - i, self.y - i))
                    break
            else:
                legal_moves.append((self.x - i, self.y - i))
        
        for i in range(1 , 8 - self.x):
            if find_piece_on_square(self.x + i, self.y,self.Token) != None:
                if find_piece_on_square(self.x + i, self.y,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x + i, self.y,self.Token).color != self.color:
                    legal_moves.append((self.x + i, self.y))
                    break
            else:
                legal_moves.append((self.x + i, self.y))
        
        for i in range(1, self.x + 1):
            if find_piece_on_square(self.x - i, self.y,self.Token) != None:
                if find_piece_on_square(self.x - i, self.y,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x - i, self.y,self.Token).color != self.color:
                    legal_moves.append((self.x - i, self.y))
                    break
                else:
                    print("something went wrong")
            else:
                legal_moves.append((self.x - i, self.y))
        
        for i in range(1, 8 - self.y):
            if find_piece_on_square(self.x, self.y + i,self.Token) != None:
                if find_piece_on_square(self.x, self.y + i,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x, self.y + i,self.Token).color != self.color:
                    legal_moves.append((self.x, self.y + i))
                    break
            else:
                legal_moves.append((self.x, self.y + i))
        
        for i in range(1, self.y + 1):
            if find_piece_on_square(self.x, self.y - i,self.Token) != None:
                if find_piece_on_square(self.x, self.y - i,self.Token).color == self.color:
                    break
                elif find_piece_on_square(self.x, self.y - i,self.Token).color != self.color:
                    legal_moves.append((self.x, self.y - i))
                    break
            else:
                legal_moves.append((self.x, self.y - i))
        
        if (x, y) in legal_moves:
            if find_piece_on_square(x, y,self.Token) != None:
                find_piece_on_square(x, y,self.Token).get_thrown()
            return True
        else:
            return False

class King(Piece):
    def __init__(self, x: int, y: int, color: Color,token:int) -> None:
        self.casteling = True
        super().__init__("King", x, y, color, "K" if color == Color.WHITE else "k",token)
    
    def get_thrown(self) -> None:
        super().get_thrown()
        Games_of_chess[self.token][0].remove(self)
        print(f"{self.color} won!")
        exit() # TODO
    
    def move(self, x, y) -> None:
        super().move(x, y)
        self.casteling = False

    def check_if_legal(self, x, y):
        curr_holder = find_piece_on_square(x, y,self.Token)

        if x > 7 or x < 0 or y > 7 or y < 0:
            return False

        booly = False
        if   x == self.x + 1 and y == self.y: booly = True
        elif x == self.x - 1 and y == self.y: booly = True
        elif x == self.x and y == self.y + 1: booly = True
        elif x == self.x and y == self.y - 1: booly = True
        elif x == self.x + 1 and y == self.y + 1: booly = True
        elif x == self.x + 1 and y == self.y - 1: booly = True
        elif x == self.x - 1 and y == self.y + 1: booly = True
        elif x == self.x - 1 and y == self.y - 1: booly = True              #if piece on square is not a rook this might be a problem
        elif self.casteling == True and x == self.x and y == self.y + 2 :
            maybe_rook=find_piece_on_square(self.x + 3,self.y,self.Token)
            if find_piece_on_square(self.x + 1,self.y,self.Token) == None and find_piece_on_square(self.x + 2,self.y,self.Token) == None and maybe_rook != None and maybe_rook.name == "Rook" and maybe_rook.casteling == True:
                maybe_rook.move(self.x - 2,self.y)
                return True
        elif self.casteling == True and x == self.x and y == self.y - 2 :
            maybe_rook=find_piece_on_square(self.x - 4,self.y,self.Token)
            if find_piece_on_square(self.x - 1,self.y,self.Token) == None and find_piece_on_square(self.x - 2,self.y,self.Token) == None and find_piece_on_square(self.x - 3,self.y,self.Token) == None and maybe_rook != None and maybe_rook.name == "Rook" and maybe_rook.casteling == True:
                maybe_rook.move(self.x+3,self.y )
                return True
            
        if checkmate(x, y, self.color):
            return False
        
        if booly == True:
            if curr_holder != None:
                if curr_holder.color != self.color:
                    curr_holder.get_thrown()
                    return True
                elif curr_holder.color == self.color:
                    return False
            else:
                return True

def find_piece_on_square(x, y, token):
    pieces_on_board_loc = Games_of_chess[token][0]
    for piece in pieces_on_board_loc:
        if piece.x == x and piece.y == y:
            return piece
    return None

# def selection(board_index):
#     while True:
#         x = int(input("X: "))
#         y = int(input("Y: "))
#         sel = find_piece_on_square(x, y,board_index)
#         if sel != None:
#             return sel
#         else:
#             print("Nothing Found Try agian")

# def move_to(piece) -> Literal[1]:
#     while True:
#         x = int(input("Move x: "))
#         y = int(input("Move y: "))

#         if piece.check_if_legal(x, y):
#             piece.move(x, y)
            
#             return 1
#         else:
#             print("not a legal Move")

def print_board(board: list[list], ) -> None:
    for i in range(8):
        for j in range(8):
            print(board[i][j], end = ' ')
        print()
    print("--------------------")

def update_board(board_index):
    # update board
    Pieces_on_board_loc = Games_of_chess[board_index][0]
    for piece in Pieces_on_board_loc:
        board[piece.x][piece.y] = piece.symbol
    for i in range(len(board)):
        for y in range(len(board[i])):
            if find_piece_on_square(i, y, board_index) == None:
                board[i][y] = " "
    
    return board

def submit_move(match_tok: int, start: tuple[int, int], end: tuple[int, int], color: Color) -> str:
    '''
    Return: "illegal_move", "not_ur_turn","king_in_check","success"
    '''
    curBoard         = Games_of_chess[match_tok][0]
    start_x, start_y = start
    end_x,end_y      = end 
    selction_obj     = find_piece_on_square(start_x,start_y,match_tok)

    if selction_obj.color == color:
        if selction_obj.check_if_legal(end_x,end_y):
            selction_obj.move_to(end_x,end_y)
            lasBoard = curBoard
            curBoard = Games_of_chess[match_tok][0]
            for pieces in curBoard:
                if pieces.name == "King" and pieces.color == color:
                    ur_king_obj= pieces 
            if checkmate(ur_king_obj.x,ur_king_obj.y,ur_king_obj.color):
                Games_of_chess[match_tok][0] = lasBoard
                print("INFO: Reverting Move")
                return "king_in_check"
            else :
                return "success"

            

        else:
            return "illegal_move"

    else:
        return "not_ur_turn"


    pass

if __name__ == "__main__":
    board_terminal = [[" " for _ in range(8)] for _ in range(8)]

    Board_index = setup_a_game()
    while True:
        # update board
        board = update_board(Board_index)
        print_board(board_terminal)
