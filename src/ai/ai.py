import sys
import os
import pygame
import time
import math

from board import Board
from game import Game

from square import Square
from piece import *
from const import *
import random

class AI:
    def __init__(self, colour, game, board, depth = 5):
        self.colour = colour
        self.game = game
        self.board = board
        self.depth = depth
        self.best_move = None
        self.prune = 0
        self.node_searched = 0

    def move_piece(self):

        best_move = None
        best_piece = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        moves = self.move_generator(self.colour)
        moves.sort(key=lambda pm: self.move_order_key(pm[0], pm[1]))

        for piece, move in moves:
            colour = "black" if self.colour == "white" else "white"
            self.board.move(piece, move)
            mobility = len(moves) * self.mobility_value_per_piece(piece)
            score = -self.minimax(self.depth - 1, -beta, -alpha, colour, move,piece, mobility)
            self.board.undo_move(piece, move)

            if score > best_score:
                best_score = score
                best_move = move
                best_piece = piece
                alpha = max(alpha, score)

            if alpha>=beta:
                break


        if best_move and best_piece:
            return best_piece, best_move
        return None
          
    def evaluation(self, colour, move, piece, mobility):
        multiplier = 1 if self.colour == "white" else -1 # white wants to maximise, black wants to minimise
        material = self.calculate_material_score(colour)

        pst_score = self.pst_score(piece, move) * 5
        attacker_total = self.count_attackers(move, piece)
        penalty = 20 * (attacker_total / piece.value) if attacker_total > 0 else 0

        capture_bonus = self.mvv_lva(piece, move.captured) * 300 if move.captured else 0

        promotion_bonus = 900 if move.is_promotion else 0

        total = 10 * material * multiplier + capture_bonus * multiplier + pst_score * multiplier * 5 + penalty * multiplier + promotion_bonus + multiplier * mobility * 30

  

        return total

    def minimax(self, depth, alpha, beta, colour, move = None, piece = None, mobility = None):
        self.node_searched += 1
        if depth == 0:
            return self.evaluation(colour, move, piece, mobility)

        moves = self.move_generator(colour)
        moves.sort(key=lambda pm: self.move_order_key(pm[0], pm[1]))

        if not moves:
            if self.board.checkmate(colour):
                return -float('inf')
            else: return 0

        colour = "black" if colour == "white" else "white"
        maxEval = -float('inf')
        for piece, move in moves:
            self.board.move(piece, move)
            mobility = len(moves) * self.mobility_value_per_piece(piece)
            evaluation = -self.minimax(depth - 1, -beta, -alpha, colour, move, piece, mobility)
            self.board.undo_move(piece, move)
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if alpha >= beta:
                self.prune += 1
                # print("pruned", alpha)
                break
        return maxEval
  
    def pst_score(self, piece, move):
        row = move.final.row
        cols = move.final.cols
        row = row if piece.colour == "white" else 7 - row
        multiplier = 1 if piece.colour == "white" else -1


        if isinstance(piece, pawn): pst_score = PAWN_PST[row][cols] 
        elif isinstance(piece, rook): pst_score = ROOK_PST[row][cols]
        elif isinstance(piece, knight): pst_score = KNIGHT_PST[row][cols]
        elif isinstance(piece, bishop) : pst_score = BISHOP_PST[row][cols]
        elif isinstance(piece, queen): pst_score = QUEEN_PST[row][cols]
        elif isinstance(piece, king): pst_score = KING_PST[row][cols]
        return pst_score * multiplier
  

    def mobility_value_per_piece(self, piece):
        if isinstance(piece, queen):
            return 1
        elif isinstance(piece, rook):
            return 2
        elif isinstance(piece, knight):
            return 4
        elif isinstance(piece, bishop):
            return 4
        elif isinstance(piece, pawn):
            return 1
        else:
            return 0

    def calculate_material_score(self, colour):
        material_score = 0
        white_pawns = black_pawns = 0
        white_rooks = black_rooks = 0 
        white_knights = black_knights = 0
        white_bishops = black_bishops = 0
        white_queen = black_queen = 0
        white_king = black_king = 0

        for row in range(ROWS):
            for cols in range(COLUMNS):
                p = self.board.squares[row][cols].piece
                if isinstance(p, pawn) and p.colour == "white":
                    white_pawns += 1
                elif isinstance(p, pawn) and p.colour == "black":
                    black_pawns += 1
                if isinstance(p, rook) and p.colour == "white":
                    white_rooks += 1
                elif isinstance(p, rook) and p.colour == "black":
                    black_rooks += 1
                if isinstance(p, knight) and p.colour == "white":
                    white_knights += 1
                elif isinstance(p, knight) and p.colour == "black":
                    black_knights += 1
                if isinstance(p, bishop) and p.colour == "white":
                    white_bishops += 1
                elif isinstance(p, bishop) and p.colour == "black":
                    black_bishops += 1
                if isinstance(p, queen) and p.colour == "white":
                    white_queen += 1
                elif isinstance(p, queen) and p.colour == "black":
                    black_queen += 1
                if isinstance(p, king) and p.colour == "white":
                    white_king += 1
                elif isinstance(p, king) and p.colour == "black":
                    black_king += 1
                
        temp_pawn = pawn("white")
        temp_rook = rook("white")
        temp_knight = knight("white")
        temp_bishop = bishop("white")
        temp_queen = queen("white")
        
        material_score = ((white_pawns - black_pawns) * (temp_pawn.value ) +  
                        (white_rooks - black_rooks) * (temp_rook.value) +
                        (white_knights - black_knights) * (temp_knight.value) + 
                        (white_bishops - black_bishops) * (temp_bishop.value) +
                        (white_queen - black_queen) * (temp_queen.value))
        
        return material_score  
# returns a list of a (piece, move) tuple
    def move_generator(self, colour):
        moves = []
        moves_sorted = []
        for row in range(ROWS):
            for cols in range(COLUMNS):
                p = self.board.squares[row][cols].piece
                if p and p.colour == colour:
                    p.clear_moves()
                    self.board.calc_moves(p, row, cols, True)
                    for m in p.moves: 
                        moves.append((p, m))

        # moves.sort(key=lambda x: x[0], reverse=True)
        # print(moves)
        return moves     
    
    def calculate_all_moves(self, depth, colour, screen):
        if depth == 0:
            return 1

        total = 0

   
        for row in range(ROWS):
            for col in range(COLUMNS):
                p = self.board.squares[row][col].piece
                if p and p.colour == colour:
                    p.clear_moves()
                    self.board.calc_moves(p, row, col, True)
                    for move in p.moves:
                        self.board.move(p, move)
                        # print(p, move.initial.row, move.initial.cols, move.final.row, move.final.cols)
                        # self.game.show_background(screen)
                        # self.game.show_last_move(screen)
                        # self.game.show_moves(screen)
                        # self.game.show_hover(screen)
                        # self.game.show_pieces(screen)
                        # pygame.display.flip()   # Update Pygame display
                        # pygame.event.pump()    # Allow window events (not freezing)
                        # time.sleep(0.1)    
                        # print(colour)
                        total += self.calculate_all_moves(depth - 1, "black" if colour == "white" else "white",screen)

                        print(f"Before undo: {p} at ({move.final.row},{move.final.cols})")
                        self.board.undo_move(p, move)
                        print(f"After undo: {p} at ({move.initial.row},{move.initial.cols})")
                        # self.game.show_background(screen)
                        # self.game.show_last_move(screen)
                        # self.game.show_moves(screen)
                        # self.game.show_hover(screen)
                        # self.game.show_pieces(screen)
                        # pygame.display.flip()   # Update Pygame display
                        # pygame.event.pump()    # Allow window events (not freezing)
                        # time.sleep(0.1) 

             

        return total

    # def can_attack(self, r, c, row, cols):
        
    #     dir_r = row - r
    #     dir_c = cols - c

    #     attacker = self.board.squares[r][c].piece
    #     if not attacker:
    #         return False

    #     # Don't attack your own piece
    #     target = self.board.squares[row][cols].piece
    #     if target and target.colour == attacker.colour:
    #         return False

    #     if isinstance(attacker, pawn):
    #         direction = -1 if attacker.colour == "white" else 1
    #         return dir_r == direction and abs(dir_c) == 1
    #     elif isinstance(attacker, knight):
    #         return (abs(dir_r), abs(dir_c)) in [(2,1), (1,2)]
    #     elif isinstance(attacker, bishop):
    #         if abs(dir_r) != abs(dir_c): return False
    #         steps_r = 1 if dir_r > 0 else -1
    #         steps_c = 1 if dir_c > 0 else -1
    #         for i in range(1, abs(dir_r)):
    #             if self.board.squares[r + i * steps_r][c + i * steps_c].piece:
    #                 return False
    #         return True
    #     elif isinstance(attacker, rook):
    #         if dir_r!=0 and dir_c != 0: return False
    #         if dir_r == 0:
    #             steps = 1 if dir_c > 0 else -1
    #             for i in range(c + steps, cols, steps):
    #                 if self.board.squares[r][i].piece:
    #                     return False
    #         else:
    #             steps = 1 if dir_r > 0 else - 1
    #             for i in range(r + steps, row, steps):
    #                 if self.board.squares[i][c].piece:
    #                     return False
    #         return True
    #     elif isinstance(attacker, queen):
    #         if abs(dir_r) == abs(dir_c):
    #             steps_r = 1 if dir_r > 0 else -1
    #             steps_c = 1 if dir_c > 0 else -1
    #             for i in range(1, abs(dir_r)):
    #                 if self.board.squares[r + i * steps_r][c + i * steps_c].piece:
    #                     return False
    #             return True
                

         
    #         if dir_r == 0 or dir_c == 0:
    #             if dir_r == 0:
    #                 steps = 1 if dir_c > 0 else -1
    #                 for i in range(c + steps, cols, steps):
    #                     if self.board.squares[r][i].piece:
    #                         return False
    #             else:
    #                 steps = 1 if dir_r > 0 else - 1
    #                 for i in range(r + steps, row, steps):
    #                     if self.board.squares[i][c].piece:
    #                         return False
    #             return True
            
    #         else:
    #             return False
    
    #     elif isinstance(attacker, king):
    #         return max(abs(dir_r), abs(dir_c)) == 1
    #     return False

    def count_attackers(self, move, piece):
        count = 0
        row = move.final.row
        cols = move.final.cols

        for r in range(ROWS):
            for c in range(COLUMNS):
                p = self.board.squares[r][c].piece
                if p and p.colour != piece.colour:
                    if self.board.can_attack(r, c, row, cols):
                        val = p.value  #because my piece values are 100- 900 not 1 - 9
                        count += val
        # print(count)
        return count

    def mvv_lva(self, attacker, captured):
        attacker_rank = attacker.value 
        captured_rank = captured.value
        return (captured_rank * 15) - attacker_rank

    def move_order_key(self, piece, move):
        score = 10000
        captured_score = 0
        promoted_score = 0
        pst_val = self.pst_score(piece, move)
        if move.captured:
            captured_score = 1000 + self.mvv_lva(piece, move.captured) * 100
        if move.is_promotion:
            promoted_score += 9000
        # if self.count_attackers(move, piece) > 0:
        #     score -= self.count_attackers(move, piece) * 0.5
        score = score + pst_val * 20 + captured_score + promoted_score
        return -score

        


        


                    





        
        




        
