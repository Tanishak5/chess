class Square:
    def __init__(self, row, col, piece=NONE): #not all swuares will have a piece
        self.row = row
        self.cols = col
        self.piece = piece