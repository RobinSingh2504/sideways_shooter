import pygame

from pygame.sprite import Sprite

class Halien(Sprite):
    """ A class to represent a single alien in the fleet. """

    def __init__(self,hai_game):
        """Initialize the alien and set its starting position. """
        super().__init__()
        self.screen = hai_game.screen
        self.settings = hai_game.settings
        self.screen_rect = self.screen.get_rect()

        """Load the alien image and get its rect attribute. """
        self.image = pygame.image.load('image/alien.bmp')
        self.rot = pygame.transform.rotate(self.image, 90)
        self.rect = self.rot.get_rect()

        """Place alien at the top right of the screen. """
        self.rect.x = self.screen_rect.width - (2* self.rect.width)
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Return true if alien has hit the edge of the screen. """
        screen_rect = self.screen.get_rect()

        if self.rect.bottom >= screen_rect.bottom or self.rect.top <=0:
            return True

    def update(self):
        """Move the alien up or down."""
        self.y += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.y = self.y



