import pygame.font

class Button:
    """A class for build button for the game"""
    
    def __init__(self, sc_game, msg):
        """Initialize button attributes"""
        
        self.screen = sc_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Set the dimensions and properties of button
        self.width, self.height = 200, 50
        self.btn_color = (3, 143, 5)
        self.txt_color = "white"
        self.txt_font = pygame.font.SysFont("impact", 40)
        
        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if msg == "Play" or msg == "Replay":
            self.rect.center = self.screen_rect.center
        elif msg == "Quit":
            self.rect.center = (600, 420)
        
        # The button message needs to be prepped only once
        self._prep_msg(msg)
    
    def _prep_msg(self, msg):
        """Turn message in to a rendered image and center text on the button"""
        
        self.msg_image = self.txt_font.render(msg, True, self.txt_color,
                                            self.btn_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """Draw a blank button and then draw message"""
        
        self.screen.fill(self.btn_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)