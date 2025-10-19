import pygame

class Ship:
    """A class to manage the ship"""
    
    def __init__(self, sc_game):
        """Initializing the ship and its starting position"""
        
        self.screen = sc_game.screen
        self.screen_rect = sc_game.screen.get_rect()
        self.settings = sc_game.settings
        
        # Load the ship image and get its rect
        self.ship = pygame.image.load("./Images/DurrrSpaceShip.png")
        self.ship = pygame.transform.scale(self.ship, (50, 50))
        self.rect = self.ship.get_rect()
        
        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Movement flag start with a ship thats not moving
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def blitme(self):
        """Draw the ship at its current location"""
        
        self.screen.blit(self.ship, self.rect)
    
    def update(self):
        """Update the ships position based on movement flag"""
        
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.rect.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.ship_speed
    
    def center_ship(self):
        """Center the ship on the screen"""
        
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)