import os
from move import Move
class Pieces:
    def __init__(self, name, colour, value, texture=None, texture_rect=None):
        self.name = name
        self.colour = colour
        value_sign = 1 if colour == "black" else -1
        self.value = value_sign * value
        self.moves = []
        self.last_moved_state = None
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

        
    def set_texture(self, size=80):
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.colour}_{self.name}.png'
        )

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []
    

#set the directions by colour
#then create pieces
class pawn(Pieces):
    def __init__(self, colour):
        self.dir = -1 if colour == "white" else 1
        self.en_passant = False
        super().__init__("pawn", colour, 1.0)


   
class rook(Pieces):
    def __init__(self, colour):
        super().__init__("rook", colour, 5.0)

class knight(Pieces):
    def __init__(self, colour):
        super().__init__("knight", colour, 3.0)

class bishop(Pieces):
    def __init__(self, colour):
        super().__init__("bishop", colour, 3.001)

class queen(Pieces):
    def __init__(self, colour):
        super().__init__("queen", colour, 9.001)

class king(Pieces):
    def __init__(self, colour):
    
        self.left_rook = None
        self.right_rook = None
        super().__init__("king", colour, 0)