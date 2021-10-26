import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """a class to manage our little shippy"""

    def __init__(self, ai_game):
        """initialize ship and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('/Users/TOM/Desktop/Alien Invasion/ship.bmp')
        self.rect = self.image.get_rect()
        
        
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        #moving flg
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """center ship on screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)