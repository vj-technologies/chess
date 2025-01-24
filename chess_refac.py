from chess_utils import Color, GameState, Piece

def default_pieces() -> list[Piece]:
    pieces = []

    for i in range(8):
        pieces.append(Pawn(1, i, Color.WHITE))
        pieces.append(Pawn(6, i, Color.BLACK))

    pieces.append(Rook(0, 0, Color.WHITE))
    pieces.append(Rook(0, 7, Color.WHITE))
    pieces.append(Rook(7, 0, Color.BLACK))
    pieces.append(Rook(7, 7, Color.BLACK))

    pieces.append(Knight(0, 1, Color.WHITE))
    pieces.append(Knight(0, 6, Color.WHITE))
    pieces.append(Knight(7, 1, Color.BLACK))
    pieces.append(Knight(7, 6, Color.BLACK))

    pieces.append(Bishop(0, 2, Color.WHITE))
    pieces.append(Bishop(0, 5, Color.WHITE))
    pieces.append(Bishop(7, 2, Color.BLACK))
    pieces.append(Bishop(7, 5, Color.BLACK))

    pieces.append(Queen(0, 3, Color.WHITE))
    pieces.append(Queen(7, 3, Color.BLACK))

    pieces.append(King(0, 4, Color.WHITE))
    pieces.append(King(7, 4, Color.BLACK))
    
    return pieces

class Pawn(Piece):
    def __init__(self, x: int, y: int, color: Color) -> None:
        super().__init__("Pawn", x, y, color, "P" if color == Color.WHITE else "p")
    
    def check_if_legal(self, x: int, y: int, game) -> None | bool:
        curr_holder = game.find_piece(x, y)

        if self.color == Color.WHITE:
            if x == self.x + 1 and y == self.y and curr_holder == None:
                return True
            elif x == self.x + 1 and (y == (self.y - 1) or (y == self.y + 1) ) and curr_holder.color == Color.BLACK:
                game.throw_piece(curr_holder)
                return True
            elif self.x == 1 and y == self.y and x == self.x + 2 and curr_holder == None:
                return True
            else:
                return False
        
        elif self.color == Color.BLACK:
            if x == self.x - 1 and y == self.y and curr_holder == None:
                return True
            elif x == self.x - 1 and (y == (self.y - 1) or (y == self.y + 1)) and curr_holder.color == Color.WHITE:
                game.throw_piece(curr_holder)
                return True
            elif self.x == 1 and y == self.y and x == self.x - 2 and curr_holder == None:
                return True
            else:
                return False

class Rook(Piece):
    def __init__(self, x: int, y: int, color: Color) -> None:
        self.casteling = True
        super().__init__("Rook", x, y, color, "R" if color == Color.WHITE else "r")
    
    def check_if_legal(self, x: int, y: int, game) -> bool:
        legal_moves = []
        for i in range(1 , 8 - self.x):
            if game.find_piece(self.x + i, self.y) != None:
                if game.find_piece(self.x + i, self.y).color == self.color:
                    break
                elif game.find_piece(self.x + i, self.y).color != self.color:
                    legal_moves.append((self.x + i, self.y))
                    break
            else:
                legal_moves.append((self.x + i, self.y))
        
        for i in range(1, self.x + 1):
            if game.find_piece(self.x - i, self.y) != None:
                if game.find_piece(self.x - i, self.y).color == self.color:
                    break
                elif game.find_piece(self.x - i, self.y).color != self.color:
                    legal_moves.append((self.x - i, self.y))
                    break
                else:
                    print("something went wrong")
            else:
                legal_moves.append((self.x - i, self.y))
        
        for i in range(1, 8 - self.y):
            if game.find_piece(self.x, self.y + i) != None:
                if game.find_piece(self.x, self.y + i).color == self.color:
                    break
                elif game.find_piece(self.x, self.y + i).color != self.color:
                    legal_moves.append((self.x, self.y + i))
                    break
            else:
                legal_moves.append((self.x, self.y + i))
        
        for i in range(1, self.y + 1):
            if game.find_piece(self.x, self.y - i) != None:
                if game.find_piece(self.x, self.y - i).color == self.color:
                    break
                elif game.find_piece(self.x, self.y - i).color != self.color:
                    legal_moves.append((self.x, self.y - i))
                    break
            else:
                legal_moves.append((self.x, self.y - i))
        
        if (x, y) in legal_moves:
            piece = game.find_piece(x, y)
            if piece != None:
                game._throw(piece)
            return True
        else:
            return False

    def move(self, x, y) -> None:
        self.x = x
        self.y = y
        self.casteling = False

class Knight(Piece):
    def __init__(self, x: int, y: int, color: Color) -> None:
        super().__init__("Knight", x, y, color, "N" if color == Color.WHITE else "n")
    
    def check_if_legal(self, x: int, y: int, game) -> None | bool:
        curr_holder = game.find_piece(x, y)
        
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
                    game.throw_piece(curr_holder)
                    return True
                elif curr_holder.color == self.color:
                    return False
            else:
                return True

class Bishop(Piece):
    def __init__(self, x: int, y: int, color: Color) -> None:
        super().__init__("Bishop", x, y, color, "B" if color == Color.WHITE else "b")
    
    def check_if_legal(self, x: int, y: int, game) -> bool:
        legal_moves = []
        
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            if game.find_piece(self.x + i, self.y + i) != None:
                if game.find_piece(self.x + i, self.y + i).color == self.color:
                    break
                elif game.find_piece(self.x + i, self.y + i).color != self.color:
                    legal_moves.append((self.x + i, self.y + i))
                    break
            else:
                legal_moves.append((self.x + i, self.y + i))
        
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            if game.find_piece(self.x + i, self.y - i) != None:
                if game.find_piece(self.x + i, self.y - i).color == self.color:
                    break
                elif game.find_piece(self.x + i, self.y - i).color != self.color:
                    legal_moves.append((self.x + i, self.y - i))
                    break
            else:
                legal_moves.append((self.x + i, self.y - i))
                
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            if game.find_piece(self.x - i, self.y + i) != None:
                if game.find_piece(self.x - i, self.y + i).color == self.color:
                    break
                elif game.find_piece(self.x - i, self.y + i).color != self.color:
                    legal_moves.append((self.x - i, self.y + i))
                    break
            else:
                legal_moves.append((self.x - i, self.y + i))
        
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            if game.find_piece(self.x - i, self.y - i) != None:
                if game.find_piece(self.x - i, self.y - i).color == self.color:
                    break
                elif game.find_piece(self.x - i, self.y - i).color != self.color:
                    legal_moves.append((self.x - i, self.y - i))
                    break
            else:
                legal_moves.append((self.x - i, self.y - i))
        
        if (x, y) in legal_moves:
            piece = game.find_piece(x, y)
            if piece != None:
                game._throw(piece)
            return True
        else:
            return False

class Queen(Piece):
    def __init__(self, x: int, y: int, color: Color) -> None:
        super().__init__("Queen", x, y, color, "Q" if color == Color.WHITE else "q")
    
    def check_if_legal(self, x: int, y: int, game):
        legal_moves = []
        
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            if game.find_piece(self.x + i, self.y + i) != None:
                if game.find_piece(self.x + i, self.y + i).color == self.color:
                    break
                elif game.find_piece(self.x + i, self.y + i).color != self.color:
                    legal_moves.append((self.x + i, self.y + i))
                    break
            else:
                legal_moves.append((self.x + i, self.y + i))
        
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            if game.find_piece(self.x + i, self.y - i) != None:
                if game.find_piece(self.x + i, self.y - i).color == self.color:
                    break
                elif game.find_piece(self.x + i, self.y - i).color != self.color:
                    legal_moves.append((self.x + i, self.y - i))
                    break
            else:
                legal_moves.append((self.x + i, self.y - i))
                
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            if game.find_piece(self.x - i, self.y + i) != None:
                if game.find_piece(self.x - i, self.y + i).color == self.color:
                    break
                elif game.find_piece(self.x - i, self.y + i).color != self.color:
                    legal_moves.append((self.x - i, self.y + i))
                    break
            else:
                legal_moves.append((self.x - i, self.y + i))
        
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            if game.find_piece(self.x - i, self.y - i) != None:
                if game.find_piece(self.x - i, self.y - i).color == self.color:
                    break
                elif game.find_piece(self.x - i, self.y - i).color != self.color:
                    legal_moves.append((self.x - i, self.y - i))
                    break
            else:
                legal_moves.append((self.x - i, self.y - i))
        
        for i in range(1 , 8 - self.x):
            if game.find_piece(self.x + i, self.y) != None:
                if game.find_piece(self.x + i, self.y).color == self.color:
                    break
                elif game.find_piece(self.x + i, self.y).color != self.color:
                    legal_moves.append((self.x + i, self.y))
                    break
            else:
                legal_moves.append((self.x + i, self.y))
        
        for i in range(1, self.x + 1):
            if game.find_piece(self.x - i, self.y) != None:
                if game.find_piece(self.x - i, self.y).color == self.color:
                    break
                elif game.find_piece(self.x - i, self.y).color != self.color:
                    legal_moves.append((self.x - i, self.y))
                    break
                else:
                    print("something went wrong")
            else:
                legal_moves.append((self.x - i, self.y))
        
        for i in range(1, 8 - self.y):
            if game.find_piece(self.x, self.y + i) != None:
                if game.find_piece(self.x, self.y + i).color == self.color:
                    break
                elif game.find_piece(self.x, self.y + i).color != self.color:
                    legal_moves.append((self.x, self.y + i))
                    break
            else:
                legal_moves.append((self.x, self.y + i))
        
        for i in range(1, self.y + 1):
            if game.find_piece(self.x, self.y - i) != None:
                if game.find_piece(self.x, self.y - i).color == self.color:
                    break
                elif game.find_piece(self.x, self.y - i).color != self.color:
                    legal_moves.append((self.x, self.y - i))
                    break
            else:
                legal_moves.append((self.x, self.y - i))
        
        if (x, y) in legal_moves:
            piece = game.find_piece(x, y)
            if piece != None:
                game._throw(piece)
            return True
        else:
            return False

class King(Piece):
    def __init__(self, x: int, y: int, color: Color) -> None:
        self.casteling = True
        super().__init__("King", x, y, color, "K" if color == Color.WHITE else "k")
    
        # FIXME wtf is this? xd
        # print(f"{self.color} won!")
        # exit() # TODO
    
    def move(self, x, y) -> None:
        super().move(x, y)
        self.casteling = False

    def check_if_legal(self, x: int, y: int, game):
        curr_holder = game.find_piece(x, y)

        if x > 7 or x < 0 or y > 7 or y < 0:
            return False

        booly = False # What does `booly` do?
        if   x == self.x + 1 and y == self.y    : booly = True
        elif x == self.x - 1 and y == self.y    : booly = True
        elif x == self.x     and y == self.y + 1: booly = True
        elif x == self.x     and y == self.y - 1: booly = True
        elif x == self.x + 1 and y == self.y + 1: booly = True
        elif x == self.x + 1 and y == self.y - 1: booly = True
        elif x == self.x - 1 and y == self.y + 1: booly = True
        elif x == self.x - 1 and y == self.y - 1: booly = True              #if piece on square is not a rook this might be a problem
        elif self.casteling == True and x == self.x and y == self.y + 2 :
            maybe_rook=game.find_piece(self.x + 3,self.y)
            if game.find_piece(self.x + 1,self.y) == None and game.find_piece(self.x + 2,self.y) == None and maybe_rook != None and maybe_rook.name == "Rook" and maybe_rook.casteling == True:
                maybe_rook.move(self.x - 2,self.y)
                return True
        elif self.casteling == True and x == self.x and y == self.y - 2 :
            maybe_rook=game.find_piece(self.x - 4,self.y)
            if game.find_piece(self.x - 1,self.y) == None and game.find_piece(self.x - 2,self.y) == None and game.find_piece(self.x - 3,self.y) == None and maybe_rook != None and maybe_rook.name == "Rook" and maybe_rook.casteling == True:
                maybe_rook.move(self.x+3,self.y )
                return True
            
        if game.checkmate(x, y, self.color):
            return False
        
        if booly:
            if curr_holder != None:
                if curr_holder.color != self.color:
                    game.throw_piece(curr_holder)
                    return True
                elif curr_holder.color == self.color:
                    return False
            else:
                return True
        # FIXME/TODO: What to return when `booly == False`?

# def selection(board_index):
#     while True:
#         x = int(input("X: "))
#         y = int(input("Y: "))
#         sel = game.find_piece(x, y,board_index)
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

class Game:
    def __init__(self) -> None:
        self.state: GameState = GameState.WHITE_TURN
        self.active_color = Color.WHITE
        self.pieces: list[Piece] = default_pieces()
    
    def find_piece(self, x: int, y: int) -> Piece | None:
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
    
    def _update_board(self, board) -> None:
        for piece in self.pieces:
            board[piece.x][piece.y] = piece.symbol
        for x in range(len(board)):
            for y in range(len(board[x])):
                if self.find_piece(x, y) == None:
                    board[x][y] = " "
    
    def _print_board(self, board) -> None:
        for i in range(8):
            for j in range(8):
                print(board[i][j], end = ' ')
            print()
        print("--------------------")

    def _throw_piece(self, piece: Piece) -> None:
        self.pieces.remove(piece)

    def checkmate(self, x: int, y: int, color: Color) -> bool:  
        '''
        checks if a given cordinate is in check and gives a bool \n
        x, y, color of the king -> Boolean
        '''  
        for i in range(8):
            if i + x > 7:
                break
            piece_y = self.find_piece(x + i, y)
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
            piece_y = self.find_piece(x - i, y)
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
            piece_y = self.find_piece(x, y + i)
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
            piece_y = self.find_piece(x, y - i)
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
            piece_y = self.find_piece(x + i, y + i)
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
            piece_y = self.find_piece(x - i, y - i)
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
            piece_y = self.find_piece(x + i, y - i)
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
            piece_y = self.find_piece(x - i, y + i)
            if piece_y != None:
                if piece_y.color != color:
                    if piece_y.name == "Bishop" or piece_y.name == "Queen":
                        return True
                    else:
                        break
                else:
                    break
        
        if color == Color.WHITE:
            pawn_piece = self.find_piece(x + 1, y + 1)
            if pawn_piece and pawn_piece.color == Color.BLACK and pawn_piece.name == "Pawn":
                    return True
            pawn_piece = self.find_piece(x + 1, y - 1)
            if pawn_piece and pawn_piece.color == Color.BLACK and pawn_piece.name == "Pawn":
                    return True
        elif color == Color.BLACK:
            pawn_piece = self.find_piece(x - 1, y + 1)
            if pawn_piece and pawn_piece.color == Color.WHITE and pawn_piece.name == "Pawn":
                    return True
            pawn_piece = self.find_piece(x - 1, y - 1)
            if pawn_piece and pawn_piece.color == Color.WHITE and pawn_piece.name == "Pawn":
                    return True
        
        knight_piece = self.find_piece(x + 2, y + 1)
        if knight_piece and knight_piece.color != color and knight_piece.name == "Knight":
                return True
        knight_piece = self.find_piece(x + 2, y - 1)
        if knight_piece and knight_piece.color != color and knight_piece.name == "Knight":
                return True
        knight_piece = self.find_piece(x - 2, y + 1)
        if knight_piece and knight_piece.color != color and knight_piece.name == "Knight":
                return True
        knight_piece = self.find_piece(x - 2, y - 1)
        if knight_piece and knight_piece.color != color and knight_piece.name == "Knight":
                return True
        knight_piece = self.find_piece(x + 1, y + 2)
        if knight_piece and knight_piece.color != color and knight_piece.name == "Knight":
                return True
        knight_piece = self.find_piece(x + 1, y - 2)
        if knight_piece and knight_piece.color != color and knight_piece.name == "Knight":
                return True
        knight_piece = self.find_piece(x - 1, y + 2)
        if knight_piece and knight_piece.color != color and knight_piece.name == "Knight":
                return True
        knight_piece = self.find_piece(x - 1, y - 2)
        if knight_piece and knight_piece.color != color and knight_piece.name == "Knight":
                return True
        return False

    def _submit_move(self, move: dict, color: Color) -> str:
        '''
        Return: "illegal_move", "not_ur_turn", "king_in_check", "success"
        '''
        curr_board = self.pieces
        selection_obj = self.find_piece(move["start_x"], move["start_y"])

        if selection_obj == None:
            return "illegal_move"

        if selection_obj.color != color:
            return "not_ur_turn"

        if not selection_obj.check_if_legal(move["end_x"], move["end_y"], self):
            return "illegal_move"
        
        selection_obj.move(move["end_x"], move["end_y"])
        last_board = curr_board
        curr_board = self.pieces
        for pieces in curr_board:
            if pieces.name == "King" and pieces.color == color:
                ur_king_obj= pieces
        
        if self.checkmate(ur_king_obj.x, ur_king_obj.y, ur_king_obj.color):
            self.pieces = last_board
            print("INFO: Reverting Move")
            return "king_in_check"
        
        return "success"

    def make_move_if_valid(self, move: dict, color: Color) -> str:
        '''
        Returns whether or not the move was valid
        '''
        result = self._submit_move(move, color)
        # TODO: remember to update the self.state in the case of checkmate etc.
        if result == "success":
            match self.active_color:
                case Color.WHITE: self.active_color = Color.BLACK
                case Color.BLACK: self.active_color = Color.WHITE
            match self.state:
                case GameState.WHITE_TURN: self.state = GameState.BLACK_TURN
                case GameState.BLACK_TURN: self.state = GameState.WHITE_TURN
                case _: print(f"What to do in this case? _submit_move returned \"succes\" {self.state=}")

        return result

if __name__ == "__main__":
    terminal_board = [[" " for _ in range(8)] for _ in range(8)]
    game = Game()
    while True:
        game._update_board(terminal_board)
        game._print_board(terminal_board)
