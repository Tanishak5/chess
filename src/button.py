import pygame


class Button:
    def __init__(self, width, height, background_colour, xpos, ypos, text, text_colour):
        self.width = width
        self.height = height
        self.background_colour = background_colour
        self.xpos = xpos
        self.ypos = ypos
        self.text = text
        self.text_colour = text_colour
        self.middle_rect = pygame.Rect(xpos - 3, ypos - 3, width + 6, height + 6)
        self.back_rect = pygame.Rect(xpos - 6, ypos - 6, width + 12, height + 15)
        self.rect = pygame.Rect(xpos, ypos, width, height)

    def draw_image(self, screen):
        font = pygame.font.SysFont("monospace", 16)
        dark = (51, 153, 102)
        white = (255, 255, 255)
        pygame.draw.rect(screen, dark , self.back_rect)
        pygame.draw.rect(screen, white, self.middle_rect)
        pygame.draw.rect(screen, self.background_colour, self.rect)
        
        text = font.render(self.text, True, self.text_colour)
        text_rect = text.get_rect(center = (self.xpos + (self.width // 2) , self.ypos  + (self.height // 2)))
        screen.blit(text, text_rect)

    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)



    
