import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class to manage our bullets in game"""
    def __init__(self, ai_game):
        super().__init__()
        """creating bullet at ships positions"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #creating a bullet rect at (0,0), settings the correct positioning
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #storing bullets positions as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """moving the bullet up the screen"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """drawing bullets to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)