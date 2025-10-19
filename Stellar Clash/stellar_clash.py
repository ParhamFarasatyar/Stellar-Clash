import pygame
from pygame import mixer
import sys
from settings import Settings
from ship import Ship
from bullets import Bullets
from stars import Stars
from aliens import Aliens
from time import sleep
from game_stats import GameStats
from health import Health
from button import Button
from scoreboard import Scoreboard
from json import dump

class StellarClash:
    """Overall class to manage game assets an behavior"""
    
    def __init__(self):
        """Initializing the main class"""
        
        pygame.init()
        self.bck_music = mixer.music
        
        # Background music
        self.bck_music.load(r"./Musics/1.MainTheme-320bit(chosic.com).mp3")
        self.bck_music.set_volume(1)        
        
        # Game sounds
        self.end_music = mixer.Sound(r"./Musics/game-over-horns-epic-stock-media-1-00-03.mp3")
        self.end_music.set_volume(1)
        
        self.fire_sound = mixer.Sound(r"./Musics/mixkit-game-gun-shot-1662.mp3")
        self.fire_sound.set_volume(1)
        
        self.ufo_explode_sound = mixer.Sound(r"./Musics/mixkit-arcade-game-explosion-2759.wav")
        self.ufo_explode_sound.set_volume(1)
        
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Stellar Clash")
        self.screen_icon = pygame.image.load(self.settings.screen_icon)
        pygame.display.set_icon(self.screen_icon)
        
        # Create an instance to store the game statistics
        #  and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.health= Health(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        
        self._create_fleet()
        self._create_space()
        
        # Start Stellar Clash in an inactive state
        self.game_active = False
        
        # Make the play button
        self.play_button = Button(self, "Play")
        self.quit_button = Button(self, "Quit")
    
    def run_game(self):
        """Start the mainloop for the game"""
        
        while True:
            
            self._check_event()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
    
            self._update_screen()
            self.clock.tick(120)
        
    def _check_event(self):
        """Respond to keypresses and mouse events"""
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._exit_game()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_event(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_button(mouse_pos)
    
    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""
        
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.stars.draw(self.screen)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.health.blitme()
        
        # Draw the score information
        self.sb.show_score()
        
        if not self.game_active:
            # Draw the play button if the game is inactive
            self.play_button.draw_button()
            self.quit_button.draw_button()
        
        pygame.display.flip()
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        
        self.bullets.update()
        
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.ufo_explode_sound.play()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self._game_difficulty()
    
    def _game_difficulty(self):
        """Make game harder when player kill all aliens"""
        
        if self.settings.alien_speed <= 5:
            self.settings.alien_speed += 0.5
        if self.settings.alien_num <= 100:
            self.settings.alien_num += 10
        if self.settings.fleet_drop_speed <= 20:
            self.settings.fleet_drop_speed += 2
        if self.settings.alien_points < 100:
            self.settings.alien_points += 5
    
    def _check_keydown_event(self, event):
        """Check keypresses event"""
        
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE and self.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self._exit_game()
        elif event.key == pygame.K_p and not self.game_active:
            self._play_game()
    
    def _check_keyup_event(self, event):
        """Checking key releases event"""
        
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it into the bullets group"""
        
        if len(self.bullets) <= self.settings.bullet_allowed:
            new_bullet = Bullets(self)
            self.bullets.add(new_bullet)
            self.fire_sound.play()
    
    def _create_space(self):
        """A helper method for create a group of stars"""
        
        star = Stars(self)
        
        for i in range(30):
            self._create_star()
    
    def _create_star(self):
        """A helper method for create a star"""
        
        new_star = Stars(self)
        self.stars.add(new_star)
    
    def _create_fleet(self):
        """Create the fleet of aliens"""
        
        alien = Aliens(self)
        
        for i in range(self.settings.alien_num):
            self._create_alien()
    
    def _create_alien(self):
        """Create an alien and place it in the fleet"""
        
        new_alien = Aliens(self)
        self.aliens.add(new_alien)
    
    def _update_aliens(self):
        """Check if the fleet is at an edge, then update position"""
        
        self._check_fleet_edges()
        self.aliens.update()
        
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens reached an edge"""
        
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            
            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            self.health.update()
            
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            
            # Pause
            sleep(0.5)
        else:
            self.play_button = Button(self, "Replay")
            self.end_music.play()
            self.game_active = False
            self.bck_music.pause()
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same if the ship got hit
                self._ship_hit()
                break
    
    def _check_button(self, mouse_pos):
        """Start a newgame when the player clicks Play"""
        
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        quit_button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if play_button_clicked and not self.game_active:
            self._play_game()
        if quit_button_clicked and not self.game_active:
            self._exit_game()
    
    def _play_game(self):
        """A helper method for play the game"""
        
        # Reset the game statistics
        self.stats.reset_stats()
        self.sb.prep_score()
        self.settings.alien_speed = 0.5
        self.settings.fleet_drop_speed = 8
        self.settings.alien_num = 60
        self.settings.alien_points = 50
        self.health.reset_health()
        self.game_active = True
        self.bck_music.play(loops= -1)
        
        # Get rid of any remaining any bullets and aliens
        self.bullets.empty()
        self.aliens.empty()
        
        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()
        
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
    
    def _exit_game(self):
        """A helper method for exit from the game"""
        
        
        with open(r"./Data/Scoreboard.json", "w") as f:
            dump({"Highscore" : str(self.stats.high_score)}, f)
        sys.exit()


if __name__ == "__main__":
    # Make a game instance and run the game
    sc = StellarClash()
    sc.run_game()