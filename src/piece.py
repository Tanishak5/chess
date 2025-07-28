class Pieces:
    def __init__(self, name, colour, value, texture=NONE, texture_rect=None):
        pass

#set the directions by colour
#then create pieces
class pawn(Pieces):
    def __init__(self, colour):
        self.dir = -1 if colour == white else 1
        super().__init__("pawn", colour, 1.0)

    def set_texture(self, size=80):
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.colour}_{self.name}.png'
        )

        
class rook(Pieces):
    def __init__(self, colour):
        super().__init__("pawn", colour, 5.0)

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
        super().__init__("king", colour, 1000)