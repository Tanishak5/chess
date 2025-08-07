from const import *
from square import Square
from piece import *
import copy


class Board:
    def __init__ (self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for cols in range(COLUMNS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.winner = None


    def return_king_pos(self, colour):
        king_pos = None
        for row in range(ROWS):
            for cols in range(COLUMNS):
                p = self.squares[row][cols].piece
                if isinstance(p, king) and p.colour == colour:
                    king_pos = (row, cols)
                    break
            if king_pos:
                    break
        
        return king_pos

    def _create(self):
        for row in range(ROWS):
            for cols in range(COLUMNS):
                self.squares[row][cols] = Square(row, cols) #labels the swaures on the board with only the row/col attribute in square

    def _add_pieces(self, colour):
        if colour == "white":
            row_pawn, row_other = (6, 7) # if colour is white pawn row is row 6
        else:
            row_pawn, row_other = (1, 0)

        for cols in range(COLUMNS):
            self.squares[row_pawn][cols] = Square(row_pawn, cols, pawn(colour))  #pawns

            self.squares[row_other][1] = Square(row_other, 1, knight(colour))
            self.squares[row_other][6] = Square(row_other, 6, knight(colour))

            self.squares[row_other][2] = Square(row_other, 2, bishop(colour))
            self.squares[row_other][5] = Square(row_other, 5, bishop(colour))

            self.squares[row_other][0] = Square(row_other, 0, rook(colour))
            self.squares[row_other][7] = Square(row_other, 7, rook(colour))

            self.squares[row_other][4] = Square(row_other, 4, king(colour))
            self.squares[row_other][3] = Square(row_other, 3, queen(colour))
    
    def castling(self, initial, final):
        return abs(initial.cols - final.cols) == 2

    def can_attack(self, r, c, row, cols):
        
        dir_r = row - r
        dir_c = cols - c

        attacker = self.squares[r][c].piece
        if not attacker:
            return False

        # Don't attack your own piece
        target = self.squares[row][cols].piece
        if target and target.colour == attacker.colour:
            return False

        if isinstance(attacker, pawn):
            direction = -1 if attacker.colour == "white" else 1
            return dir_r == direction and abs(dir_c) == 1
        elif isinstance(attacker, knight):
            return (abs(dir_r), abs(dir_c)) in [(2,1), (1,2)]
        elif isinstance(attacker, bishop):
            if abs(dir_r) != abs(dir_c): return False
            steps_r = 1 if dir_r > 0 else -1
            steps_c = 1 if dir_c > 0 else -1
            for i in range(1, abs(dir_r)):
                if self.squares[r + i * steps_r][c + i * steps_c].piece:
                    return False
            return True
        elif isinstance(attacker, rook):
            if dir_r!=0 and dir_c != 0: return False
            if dir_r == 0:
                steps = 1 if dir_c > 0 else -1
                for i in range(c + steps, cols, steps):
                    if self.squares[r][i].piece:
                        return False
            else:
                steps = 1 if dir_r > 0 else - 1
                for i in range(r + steps, row, steps):
                    if self.squares[i][c].piece:
                        return False
            return True
        elif isinstance(attacker, queen):
            if abs(dir_r) == abs(dir_c):
                steps_r = 1 if dir_r > 0 else -1
                steps_c = 1 if dir_c > 0 else -1
                for i in range(1, abs(dir_r)):
                    if self.squares[r + i * steps_r][c + i * steps_c].piece:
                        return False
                return True
                
         
            if dir_r == 0 or dir_c == 0:
                if dir_r == 0:
                    steps = 1 if dir_c > 0 else -1
                    for i in range(c + steps, cols, steps):
                        if self.squares[r][i].piece:
                            return False
                else:
                    steps = 1 if dir_r > 0 else - 1
                    for i in range(r + steps, row, steps):
                        if self.squares[i][c].piece:
                            return False
                return True
            
            else:
                return False
    
    def in_check(self,move, piece):

        initial_piece = self.squares[move.initial.row][move.initial.cols].piece
        final_piece = self.squares[move.final.row][move.final.cols].piece
        captured = move.captured
        

        self.squares[move.final.row][move.final.cols].piece = initial_piece
        self.squares[move.initial.row][move.initial.cols].piece = None

        king_pos = self.return_king_pos(piece.colour)
        row = king_pos[0]
        cols = king_pos[1]

        for r in range(ROWS):
            for c in range(COLUMNS):
                p = self.squares[r][c].piece
                if p and p.colour!=piece.colour:
                    if self.can_attack(r, c, row, cols):
                        self.squares[move.initial.row][move.initial.cols].piece = initial_piece
                        self.squares[move.final.row][move.final.cols].piece = final_piece
                        return True
        self.squares[move.initial.row][move.initial.cols].piece = initial_piece
        self.squares[move.final.row][move.final.cols].piece = final_piece                
        return False

       
        # initial_piece = self.squares[move.initial.row][move.initial.cols].piece
        # final_piece = self.squares[move.final.row][move.final.cols].piece
        # captured = move.captured
        

        # self.squares[move.final.row][move.final.cols].piece = initial_piece
        # self.squares[move.initial.row][move.initial.cols].piece = None
        # king_pos = self.return_king_pos(piece.colour)
        # for row in range(ROWS):
        #     for cols in range(COLUMNS):
        #         p = self.squares[row][cols].piece
        #         if p and p.colour != piece.colour:
        #             p.clear_moves()
        #             self.calc_moves(p, row, cols, False)
        #             for m in p.moves:
        #                 if (m.final.row, m.final.cols) == king_pos:
        #                     self.squares[move.initial.row][move.initial.cols].piece = initial_piece
        #                     self.squares[move.final.row][move.final.cols].piece = final_piece
        #                     return True
        # self.squares[move.initial.row][move.initial.cols].piece = initial_piece
        # self.squares[move.final.row][move.final.cols].piece = final_piece                   
        # return False
             
    def check_promotion(self, piece, move):
        if move.final.row == 0 or move.final.row == 7:
            self.squares[move.final.row][move.final.cols].piece = queen(piece.colour)
            move.is_promotion = True
            move.promoted_piece = self.squares[move.initial.row][move.initial.cols].piece
        else: move.is_promotion = False
    
    def valid_move(self, piece, move):
        return move in piece.moves

    def set_en_passant(self, piece, move):
        if not isinstance(piece, pawn):
            return

        for row in range(ROWS):
            for cols in range(COLUMNS):
                p = self.squares[row][cols].piece
                if isinstance(p, pawn):
                    p.en_passant = False #reset for all pawns
        
        start_row = move.initial.row
        end_row = move.final.row
        if abs(end_row - start_row) == 2:
            piece.en_passant = True

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.cols].is_empty()
        move.captured = self.squares[move.final.row][move.final.cols].piece
        
        move.prev_piece_moved = piece.moved
        #update on board
        self.squares[initial.row][initial.cols].piece = None
        self.squares[final.row][final.cols].piece = piece

        if isinstance(piece, pawn):
            diff = final.cols - initial.cols

            if en_passant_empty and diff!=0:
                move.captured = self.squares[initial.row][initial.cols+diff].piece
                self.squares[initial.row][initial.cols + diff].piece = None
                self.squares[final.row][final.cols].piece = piece
                self.set_en_passant(piece, move)
                
                move.en_passant = True
    
            else:
                self.check_promotion(piece, move)
                move.is_promotion = True

        

        if isinstance(piece, king):
            if self.castling(initial, final):
                move.castling = True
                diff = final.cols - initial.cols
                if diff > 0:
                    rook_final_cols = final.cols - 1
                    rook_initial_cols = 7
                else:
                    rook_final_cols = final.cols + 1
                    rook_initial_cols = 0

                rook = self.squares[initial.row][rook_initial_cols].piece
                move.castled_rook = rook
                self.squares[initial.row][rook_initial_cols].piece = None
                self.squares[initial.row][rook_final_cols].piece = rook
                rook.moved = True

        #update physically
        piece.moved = True
        piece.clear_moves()
    
        
        move.move_prev = self.last_move
        self.last_move = move
  
    def undo_move(self, piece, move):
        initial = move.initial
        final = move.final
        #update on board
      
        self.squares[initial.row][initial.cols].piece = piece
        self.squares[final.row][final.cols].piece = move.captured

        if isinstance(piece, pawn):
            diff = final.cols - initial.cols
            if move.en_passant and diff!=0:
                self.squares[final.row][final.cols].piece = None
                self.squares[initial.row][final.cols].piece = move.en_passant_target
            else:
                if move.is_promotion:
                    self.squares[initial.row][initial.cols].piece = piece
                    self.squares[final.row][final.cols].piece = move.captured
            
        

        if isinstance(piece, king):
            if move.castling:
                diff = final.cols - initial.cols
                if diff < 0:
                    rook_final_cols = 5
                    rook_initial_cols = 7
                else:
                    rook_final_cols = 3
                    rook_initial_cols = 0

                rook = move.castled_rook
                self.squares[initial.row][rook_final_cols].piece = None
                self.squares[initial.row][rook_initial_cols].piece = move.castled_rook
                
        piece.moved = move.prev_piece_moved
        piece.clear_moves()
        self.last_move = None


    def calc_moves(self, piece, row, col, bool=True):

        def pawn_moves():
            if piece.moved == False and piece.colour == "white" and row == 6:
                steps = 2
            elif piece.moved == False and piece.colour == "black" and row == 1:
                steps = 2
            else:
                steps = 1
         

            start = row + piece.dir
            end = row +  (piece.dir * (steps + 1))

            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
    
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        move.captured = self.squares[final.row][final.cols].piece
                
                        
                        if bool:
                            
                            if not self.in_check(move, piece):
                            
                                # append new move
                                piece.add_move(move)
                                
                        else:
                            # append new move
                       
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                # not in range
                else: break



            # only diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.colour):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        move.captured = self.squares[final.row][final.cols].piece
                        
        

                        if bool:
                            if not self.in_check(move, piece):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
          
            # left en passant
            r = 3 if piece.colour == "white" else 4
            fr = 2 if piece.colour == "white" else 5
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col -1].has_rival_piece(piece.colour):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col - 1, p)
                            move = Move(initial, final)
                            move.en_passant = True
                            move.en_passant_target = self.squares[row][col - 1].piece
                            

                            if bool:
                                if not self.in_check(move, piece):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col +1].has_rival_piece(piece.colour):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col + 1, p)
                            move = Move(initial, final)
                            move.en_passant_target = self.squares[row][col + 1].piece
                            move.en_passant = True
                           
                            
                            if bool:
                                if not self.in_check(move, piece):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

        def king_moves():
            possible_moves = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            for move in possible_moves:
                possible_move_row, possible_move_col = move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.colour):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        move.captured = self.squares[final.row][final.cols].piece
                        
                        if bool:
          
                            if not self.in_check(move, piece):
                                piece.add_move(move)
                            else:

                                continue
                        else:
                   
                            piece.add_move(move)

                    

            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                right_rook = self.squares[row][7].piece
 
                if isinstance(left_rook, rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 3:
                                piece.left_rook = left_rook

                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveL = Move(initial, final)
                               
                        

                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                moveK.castling = True
                                moveK.castled_rook = left_rook
                                if bool:
                                    if not self.in_check(moveK, piece) and not self.in_check(moveL, left_rook):
                                        # append new move to rook
                                        left_rook.add_move(moveL) #MOVEL REMOVED ADD
                                        # append new move to king
                                        piece.add_move(moveK)
  
                                       
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveL)
                                    # append new move king
                                    piece.add_move(moveK)
                                

                                
                if isinstance(right_rook, rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 6:
                                piece.right_rook = right_rook

                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                                
                

                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                moveK.castling = True
                                moveK.castled_rook = right_rook
                              
                                if bool:
                                    if not self.in_check(moveK, piece) and not self.in_check(moveR, right_rook):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                       
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)
  
                                   
        def knight_moves():
            possible_moves = [
                (row + 2, col + 1), 
                (row - 2, col - 1),
                (row + 2, col - 1),
                (row -2, col + 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row -1, col + 2),
            ] 

            for move in possible_moves:
                possible_moves_row, possible_moves_cols = move
                if Square.in_range(possible_moves_row, possible_moves_cols):
                    if self.squares[possible_moves_row][possible_moves_cols].is_empty_or_rival(piece.colour):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_moves_row][possible_moves_cols].piece
                        final = Square(possible_moves_row, possible_moves_cols, final_piece)
                        move = Move(initial, final)
                        move.captured = self.squares[final.row][final.cols].piece
                    
                        
                        if bool:
                            if not self.in_check(move, piece):
                                piece.add_move(move)
                            else:
                                continue
                        else:
                                piece.add_move(move) 

        def straightline_moves(increase):

            for incr in increase:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr


                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        move.captured = self.squares[final.row][final.cols].piece
                        

                        if self.squares[possible_move_row][possible_move_col].is_empty(): #if empty conitnue
                            if bool:
                                if not self.in_check(move, piece):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.colour):
                            if bool:
                                if not self.in_check(move, piece):
                                    piece.add_move(move)
                            
                            else:
                                piece.add_move(move) 
                            break


                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.colour):
                           break
                    else:
                        break

                    possible_move_row += row_incr
                    possible_move_col += col_incr

        if isinstance(piece, pawn):
            pawn_moves()
        elif isinstance(piece, knight):
            knight_moves()
        elif isinstance(piece, bishop):
            increase = [( 1, 1),
                        (- 1, 1),
                        (1, -1),
                        (-1, -1)
                ]
            straightline_moves(increase)
        elif isinstance(piece, rook):
                increase = [(0, 1),
                            (0,  -1),
                            ( 1, 0),
                            ( - 1, 0)
                        ]
                straightline_moves(increase)
        elif isinstance(piece, queen):
            increase = [(0,1), #up
                        (0, -1), #down
                        (1, 0),#right
                        (-1,0),#left
                        (1, 1),#ne
                        (-1, -1),#sw
                        (1, -1),#nw
                        (-1, 1)#se
                        ]
            straightline_moves(increase)
        elif isinstance(piece, king): 
            king_moves()  


    def checkmate(self, colour):
        moves = 0
        
   
        for row in range(ROWS):
            for cols in range(COLUMNS):
                p = self.squares[row][cols].piece
                if p and p.colour == colour:
                    p.clear_moves()
                    self.calc_moves(p, row, cols, True)
                    moves += len(p.moves)
        
        if moves == 0 :
            self.winner = "black" if colour == "white" else "white"
            return True
        else:
            return False



