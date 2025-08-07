class Move:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final
        self.captured = None
        self.is_promotion = False
        self.en_passant_target = None
        self.en_passant = False
        self.castling = False
        self.promoted_piece = None
        self.castled_rook = None
        self.prev_piece_moved = False



    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final


