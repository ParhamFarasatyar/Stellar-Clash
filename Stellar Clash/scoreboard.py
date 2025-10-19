import pygame.font

class Scoreboard:
    """A class to report scoring information"""
    
    def __init__(self, sc_game):
        """Initialize scorekeeping attributes"""
        
        self.screen = sc_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sc_game.settings
        self.stats = sc_game.stats
        
        # Font settings for scoring information
        self.txt_color = (252, 252, 3)
        self.txt_font = pygame.font.SysFont("impact", 22)
        
        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
    
    def prep_score(self):
        """Turn the score into a rendered image"""
        
        score_str = str(self.stats.score)
        self.score_image = self.txt_font.render(score_str, True, self.txt_color)
        
        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
        """Turn the highscore into a rendered image"""
        
        score_str = str(self.stats.high_score)
        self.high_score_image = self.txt_font.render(f"HighScore: {score_str}", True, self.txt_color)
        
        # Display the highscore at the mid top if the screen
        self.highscore_rect = self.high_score_image.get_rect()
        self.highscore_rect.left = self.screen_rect.left + 20
        self.highscore_rect.top = 20
    
    def check_high_score(self):
        """Check to see if there is a new highscore"""
        
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    
    def show_score(self):
        """Draw score to the screen"""
        
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.highscore_rect)