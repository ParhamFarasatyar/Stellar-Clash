import pygame

class Settings:
    """A class to store all settings for Stellar Clash"""
    
    def __init__(self):
        """Initialize the game's static settings"""
        
        # Screen settings
        self.bg_color = (0, 11, 88)
        self.screen_width = 1200
        self.screen_height = 700
        self.screen_icon = "./Images/StellarIcon.png"
        
        # Ship settings
        self.ship_speed = 4
        self.ship_limit = 3
        
        # Bullets settings
        self.bullet_speed = 6
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullet_allowed = 3
        
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 8
        self.alien_num = 60
        # Fleet direction of 1 represents right and -1 represents left
        self.fleet_direction = 1
        
        # Scoring settings
        self.alien_points = 50