import pygame 

class button():
    def __init__(self, x, y, image, single_click):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click 

    def draw(self, suface):
        action = False
         #finds the mouse pos 
        pos = pygame.mouse.get_pos() 

        #check if the mouse is on the button and if pressed 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.cliked = True
                if self.single_click:
                    self.clicked = True
            elif pygame.mouse.get_pressed()[0] == 0: #resets 
                self.clicked = False
        #show button on screen 
        suface.blit(self.image, self.rect)

        return action


