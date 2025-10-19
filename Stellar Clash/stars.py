import pygame
from pygame.sprite import Sprite
from random import randint

class Stars(Sprite):
    """A class to manage stars appeared on screen"""
    
    def __init__(self, sc_game):
        """Initilize the star and set its starting position"""
        
        super().__init__()
        
        self.screen = sc_game.screen
        self.settings = sc_game.settings
        
        # Load the star image and set its rect attribute
        self.image = pygame.image.load(r"./images/star.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        
        # Start each new star in a random position
        self.rect.x = randint(10, self.settings.screen_width)
        self.rect.y = randint(10, self.settings.screen_height)
        
        # Store the star exact horizontal position
        self.x = float(self.rect.x)