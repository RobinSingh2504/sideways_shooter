import pygame

from hsettings import settings

class Hship:

    def __init__(self, ai_game):

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load("image/ship.bmp")
        self.rot = pygame.transform.rotate(self.image, 270)
        self.rect = self.rot.get_rect()

        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

        self.moving_top= False
        self.moving_down = False

    def update(self):
        if self.moving_top and self.rect.top > 0:
            self.y -= self.settings.ship_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y +=  self.settings.ship_speed

        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.rot, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)