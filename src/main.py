# sys allows us to exist the game
# const is a class and we import all the attributes
# main is a created object
# the first method called is the init method
# to define a method in init, self.attribute name = attribute name.

import pygame
import sys
from const import *
from game import Game

class Main:
    def __init__(self): #init defines an object, first method called is init then others
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CHESS")
        self.game = Game()


    def mainloop(self):
        game = self.game
        screen = self.screen

        while True:
            game.show_background(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()        

main = Main()
main.mainloop()