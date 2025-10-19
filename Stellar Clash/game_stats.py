from json import load

class GameStats:
    """Track statistics for Stellar Clash"""
    
    def __init__(self, sc_game):
        """Initialize statistics"""
        
        self.settings = sc_game.settings
        # High score should never be reset
        try:
            with open(r"./Data/Scoreboard.json") as f:
                data = load(f)
                self.high_score = int(data["Highscore"])
        except FileNotFoundError:
            self.high_score = 0
        
        self.reset_stats()
    
    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        
        self.ships_left = self.settings.ship_limit
        self.score = 0