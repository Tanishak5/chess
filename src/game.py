#surgace refers to the pygame screen
import pygame
from const import *
# loop in all the rows of all the columns - double floor, draw a dark/light square.

class Game:
    def __init__(self):
        pass
    def show_background(self, surface):
        for row in range(ROWS):
            for cols in range(COLUMNS):
                if ((row + cols) % 2) == 0:
                    colour = (234, 235, 200)
                else:
                    colour = (119, 154, 88)
                rect = (cols * SQSIZE, row *SQSIZE, SQSIZE, SQSIZE) #y pos start, x post start, size, size 
                pygame.draw.rect(surface, colour, rect)     