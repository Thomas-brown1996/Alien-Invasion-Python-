import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Managing game behaviour"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

       
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion!")



        #creating an instance to store our game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #make the Play button
        self.play_button = Button(self, "Play")
        
    def run_game(self):
        "main loop"
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            #deleting off-screen bullets
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))
           
            #listen to keyboard and mouse
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
    
    def _check_play_button(self, mouse_pos):
        """start a new game when the player clicks play"""
       
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset the game settings
            self.settings.initialise_dynamic_settings()

            #Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet
            self._create_fleet()
            self.ship.center_ship()

            #hide mr.mouse
            pygame.mouse.set_visible(False)

    def check_keydown_events(self, event):
        """responsing to keydown events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def check_keyup_events(self, event):
        """responsing to keyup events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
                
    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update positions of ze bullets"""
        #get rid disappeared bulelts
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_alien_bullet_collisions()


    def _check_alien_bullet_collisions(self):
        """respond to any collisions"""
        #remove dead aliens
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

         #destroy bullets & create new fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
        
        #increase level
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """update the position of all aliens"""
        self._check_fleet_edges()
        self.aliens.update()
        #look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        
        #check for aliens hitting the bottom
        self._check_aliens_bottom()
    
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #draw the score information
        self.sb.show_score()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()
    
    def _create_fleet(self):
        """create our alien fleet"""
        #finding the number of aliens in a row
        #spacng between aliens is equal to an alien
        #make mr.alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (1 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #working out the number of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #creating our complete fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    def _create_alien(self, alien_number, row_number):
        """creating alien and placing it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        """respond when aliens have reached the edges"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """drop fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *=-1  

    def _ship_hit(self):
        """react to the ship being hit by an Alien"""
        #reduce number of ships
        if self.stats.ships_left > 0:
            #remove our shipies
            self.stats.ships_left -= 1
            self.sb.prep_ships()

        #delete remaining bullets and aliens
            self.aliens.empty()
            self.aliens.empty() 

        #creating a new fleet
            self._create_fleet()
            self.ship.center_ship()

        #short pause
            sleep(1) 

        else:
            self.stats.game_active = False
            pygame.mouse.set_visbile(True)


    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treating this events the same as if an alien hit our ship
                self._ship_hit()
                break


            
            

if __name__ =='__main__':
    ai = AlienInvasion()
    ai.run_game()