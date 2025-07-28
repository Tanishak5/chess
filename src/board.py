from const import *
from square import Square

class Board:
    def __init__ (self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for cols in range(COLUMNS)]
        for row in range(ROWS):
            self.pieces = piece
            self._create()
    def _create(self):
       
            for cols in range(COLUMNS):
                self.squares[rows][cols] = Square(row, cols) #labels the swaures on the board with only the row/col attribute in square

    def _add_pieces(self, color):
        pass
