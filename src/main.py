# sys allows us to exist the game
# const is a class and we import all the attributes
# main is a created object
# the first method called is the init method
# to define a method in init, self.attribute name = attribute name.

import pygame
import sys
import os
import time
from const import *
from game import Game
from square import Square
from move import Move
from config import Config
from button import Button
from theme import Theme
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.ai import AI


class Main:
    def __init__(self): #init defines an object, first method called is init then others
        pygame.init()
        self.next = "white"
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CHESS")
        self.game = Game()
        self.mode = "ai"
        


    def mainloop(self):
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        theme = self.game.config
        ai_player = AI("white", game, board)
        needs_redraw = True


        while True:

            game.show_background(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_hover(screen)
            game.show_pieces(screen)
            

            
            # whilst dragging continuously update the screen so no glitching
            if dragger.dragging:
                dragger.update_blit(screen)        

            if(self.mode == "ai" and self.next == ai_player.colour):
                # ai_player.calculate_all_moves(3, ai_player.colour, screen)
                # return
                # return
                colour = ai_player.colour
                ai_move = ai_player.move_piece()
                if ai_move:
                    
                    ai_piece, move = ai_move
                    board.move(ai_piece, move)
                    board.set_en_passant(ai_piece, move)
                    game.play_sound(move.captured != None)
                    game.show_background(screen)
                    game.show_last_move(screen)
                    game.show_moves(screen)
                    game.show_pieces(screen)
                    self.next = "black" if self.next == "white" else "white"
                    print("done")

                    

            if board.checkmate(self.next):
                    font = pygame.font.SysFont("monospace", 36)
                    black = (0, 0, 0)
                    white = (255, 255, 255)
                    green = (119, 154, 88)
                    blue = (123, 147, 156)


                    back_rect = (100, 200, 600, 300)
                    back_g_rect = (110, 210, 600, 300)
                    pygame.draw.rect(screen, blue, back_g_rect)
                    pygame.draw.rect(screen, white, back_rect)
                    
                    restart = Button(100, 40, green, 250, 425, "restart", white)
                    restart.draw_image(screen)
                    end = Button(100, 40, green, 450, 425, "End", white)
                    end.draw_image(screen)

                    text = font.render("Checkmate! ", True, black)
                    text1 = font.render(f"The Winner is: {board.winner}", True, black)
                    text_rect = text.get_rect(center=(300, 300))  # Optional centering method (not used here)
                    text1_rect = text1.get_rect(center = (400,400))
                    # You define white but don't use it:
                    # Manual placement instead of using text_rect
                    screen.blit(text, text_rect)
                    screen.blit(text1, text1_rect)
                    pygame.display.update()

                    if restart.is_pressed(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_hover(screen)
                        game.show_pieces(screen)
                        self.next = "white" if self.next == "black" else "black"
                    elif end.is_pressed(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                    
             

            for event in pygame.event.get():
                #when clicked down, chose a piece and set the piece to drag
                #calculate the moves for the particular piece
    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE



                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if(piece.colour == self.next):
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)

                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
            
                        
                    
                # when dragging allow the hovered square to change colour
                # update background, then the move, then the pieces
                # blit the screen  
                elif event.type == pygame.MOUSEMOTION:

                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hovered_sqr(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                    
            

                # When clicked down, move the piece
                # Create a move for this piece and if valid, actually move it on the board
                # play the correct sound, depending on if captured or not
                # update background, moves then pieces
                # set the turn to the next player
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:

                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col) 
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):

                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move) 

                            board.set_en_passant(dragger.piece, move) 
                            game.play_sound(captured)
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            self.next = "white" if self.next == "black" else "black"
                            
                    dragger.undrag_piece()
     
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        theme.change_theme()
       
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()        

main = Main()
main.mainloop()