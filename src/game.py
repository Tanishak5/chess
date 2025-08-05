#surgace refers to the pygame screen
import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
# loop in all the rows of all the columns - double floor, draw a dark/light square.

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.hovered_sqr = None

    def show_background(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for cols in range(COLUMNS):
                if ((row + cols) % 2) == 0:
                    colour = theme.bg.light
                else:
                    colour = theme.bg.dark
                rect = (cols * SQSIZE, row *SQSIZE, SQSIZE, SQSIZE) #y pos start, x post start, size, size 
                pygame.draw.rect(surface, colour, rect)    

    def show_pieces(self, surface):
        for row in range(ROWS):
            for cols in range(COLUMNS):
                if self.board.squares[row][cols].has_piece(): #check if piece on square
                    piece = self.board.squares[row][cols].piece #then get the piece
    
                    if piece is not self.dragger.piece:

                        img = pygame.image.load(
                            piece.texture) #get the image of the piece
                        img_center = cols * SQSIZE +  SQSIZE // 2, row * SQSIZE + SQSIZE // 2 #find the center of the piece
                        piece.texture_rect = img.get_rect(center = img_center) # set the texture of the piece to the img
                        surface.blit(img, piece.texture_rect) # render the image


    def show_hover(self, surface):
        if self.hovered_sqr:
            colour = (180, 180, 180)
            rect = (self.hovered_sqr.cols *SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, colour, rect)
    
    def set_hovered_sqr(self, row, col):

        self.hovered_sqr = self.board.squares[row][col]


    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                colour = theme.moves.light if (move.final.row + move.final.cols) %2 == 0 else theme.moves.dark
                rect = (move.final.cols * SQSIZE, move.final.row *SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, colour, rect)
    
    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                colour = theme.trace.light if (pos.row + pos.cols) % 2 == 0 else theme.trace.dark
                rect = (pos.cols * SQSIZE, pos.row *SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, colour, rect)

    def reset(self):
        self.__init__()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    
            