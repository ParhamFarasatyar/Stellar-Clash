import pygame
from pygame.sprite import Sprite
from random import choice, randint

class Aliens(Sprite):
    """A class to represent a single alien in the fleet"""
    
    def __init__(self, sc_game):
        """Initialize the alien and set its starting position"""
        
        super().__init__()
        
        self.screen = sc_game.screen
        self.settings = sc_game.settings
        
        # Load the aliens image and set it's rect attribute
        alien_colors = ["blue", "brown", "green", "orange", "red"]
        choiced_color = str(choice(alien_colors))
        self.image = pygame.image.load(f"./images/{choiced_color.title()}UFO.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        
        # Start the each new alien near the top left of the screen
        self.rect.x = randint(90, self.settings.screen_width - 90)
        self.rect.y = randint(5, self.settings.screen_height - 300)
        
        # Store the alien's exact horizontal posotion
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return True if alien is at edge of screen"""
        
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        """Move alien to right or left"""
        
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x