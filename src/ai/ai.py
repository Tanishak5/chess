import sys
import os
import pygame
import time


from board import Board
from game import Game

from square import Square
from piece import *
from const import *
import random
class AI:
    def __init__(self, colour, game, board, depth = 2):
        self.colour = colour
        self.game = game
        self.board = board
        self.depth = depth
        self.best_move = None

    def move_piece(self):

        best_move = None
        best_piece = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for piece, move in self.move_generator(self.colour):
            colour = "black" if self.colour == "white" else "white"
            self.board.move(piece, move)
            score = -self.minimax(self.depth - 1, -beta, -alpha, colour)
            self.board.undo_move(piece, move)

            if score > best_score:
                best_score = score
                best_move = move
                best_piece = piece
                alpha = max(alpha, score)

            if alpha>=beta:
                break

        print(best_score)
        if best_move and best_piece:
            return best_piece, best_move
        return None


    def calculate_num_pieces(self, piece, colour):
        num_pieces = 0
        moves = []
        for row in range(ROWS):
            for cols in range(COLUMNS):
                p = self.board.squares[row][cols].piece
                if isinstance(p, piece) and p.colour == colour:
                    num_pieces += 1
        return num_pieces

   

    def calculate_mobility_score(self, colour):
        possible_moves = 0
        for row in range(ROWS):
            for cols in range(COLUMNS):
                p = self.board.squares[row][cols].piece
                if p and p.colour == colour:
                    moves = []
                    self.board.calc_moves(p, row, cols, True)
                    possible_moves += len(p.moves)

        return possible_moves



    def calculate_material_score(self, colour):
        material_score = 0
        white_pawns = self.calculate_num_pieces(pawn, "white")
        black_pawns = self.calculate_num_pieces(pawn, "black")
        white_rooks = self.calculate_num_pieces(rook, "white")
        black_rooks = self.calculate_num_pieces(rook, "black")
        white_knights = self.calculate_num_pieces(knight, "white")
        black_knights = self.calculate_num_pieces(knight, "black")
        white_bishops = self.calculate_num_pieces(bishop, "white")
        black_bishops = self.calculate_num_pieces(bishop, "black")
        white_queen = self.calculate_num_pieces(queen, "white")
        black_queen = self.calculate_num_pieces(queen, "black")
        temp_pawn = pawn("white")
        temp_rook = rook("white")
        temp_knight = knight("white")
        temp_bishop = bishop("white")
        temp_rook = rook("white")
        temp_queen = queen("white")
        
        material_score = ((white_pawns - black_pawns) * (temp_pawn.value ) +  
                        (white_rooks - black_rooks) * (temp_rook.value) +
                        (white_knights - black_knights) * (temp_knight.value) + 
                        (white_bishops - black_bishops) * (temp_bishop.value) +
                        (white_queen - black_queen) * (temp_queen.value))
        
        multiplier = -1 if colour == "black" else 1
        return material_score * multiplier 
                
    def evaluation(self, colour):
        multiplier = 1 if colour == "white" else -1 # white wants to maximise, black wants to minimise
        material = self.calculate_material_score(colour)
        mobility = self.calculate_mobility_score(colour)
        total = material + mobility * 10 * multiplier
        return total

  
    def minimax(self, depth, alpha, beta, colour):
            if depth == 0:
                return self.evaluation(colour)

            moves = self.move_generator(colour)


            if not moves:
                if self.board.checkmate(colour):
                    return -float('inf')
                else: return 0

            colour = "black" if colour == "white" else "white"
            maxEval = -float('inf')
            for piece, move in moves:
                self.board.move(piece, move)
                evaluation = -self.minimax(depth - 1, -beta, -alpha, colour)
                
                self.board.undo_move(piece, move)
                maxEval = max(maxEval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return maxEval
            
    def calculate_all_moves(self, depth, colour, screen):
        if depth == 0:
            return 1

        total = 0

        colour = "black" if colour == "white" else "white"
        for row in range(ROWS):
            for col in range(COLUMNS):
                p = self.board.squares[row][col].piece
                if p and p.colour == colour:
        
                    self.board.calc_moves(p, row, col, True)
        
                    for move in p.moves:
                        self.board.move(p, move)

                        # self.game.show_background(screen)
                        # self.game.show_last_move(screen)
                        # self.game.show_moves(screen)
                        # self.game.show_hover(screen)
                        # self.game.show_pieces(screen)
                        # pygame.display.flip()   # Update Pygame display
                        # pygame.event.pump()    # Allow window events (not freezing)
                        # time.sleep(0.1)    

                        total += self.calculate_all_moves(depth - 1, colour, screen)
                        print(total)
                        self.board.undo_move(p, move)
                        # self.game.show_background(screen)
                        # self.game.show_last_move(screen)
                        # self.game.show_moves(screen)
                        # self.game.show_hover(screen)
                        # self.game.show_pieces(screen)
                        # pygame.display.flip()   # Update Pygame display
                        # pygame.event.pump()    # Allow window events (not freezing)
                        # time.sleep(0.1)  

        return total


# returns a list of a (piece, move) tuple
    def move_generator(self, colour):
            moves = []
            for row in range(ROWS):
                for cols in range(COLUMNS):
                    p = self.board.squares[row][cols].piece
                    if p and p.colour == colour:
                        self.board.calc_moves(p, row, cols, True)
                        for m in p.moves: 
                            moves.append((p, m))

            return moves

        
        




        
