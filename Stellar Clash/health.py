import pygame

class Health:
    """A class for showing player remaining health after any hit"""
    
    def __init__(self, sc_game):
        """Initialize image and number of health"""
        
        self.screen = sc_game.screen
        self.screen_rect = sc_game.screen.get_rect()
        self.settings = sc_game.settings
        
        self.image = pygame.image.load(r"./Images/heart.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        
        self.heart_num = self.settings.ship_limit
        self.my_font = pygame.font.SysFont('impact', 28)
        
        self.rect.bottomleft = self.screen_rect.bottomleft
    
    def blitme(self):
        """Draw the heart at it's current location"""
        
        self.screen.blit(self.image, self.rect)
        self.heart_disp = self.my_font.render(str(self.heart_num), 1, "white")
        self.screen.blit(self.heart_disp, (40, self.settings.screen_height-33))
    
    def update(self):
        """Update the number of heart after any hit"""
        
        self.heart_num -= 1
    
    def reset_health(self):
        self.heart_num = self.settings.ship_limit