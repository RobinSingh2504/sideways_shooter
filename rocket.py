import pygame

from pygame.sprite import Sprite

class Rocket(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.rocket_color

        self.rect = pygame.Rect(0,0, self.settings.rocket_width, self.settings.rocket_height)
        self.rect.midright = ai_game.ship.rect.midright

        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.rocket_speed
        self.rect.x = self.x

    def draw_rocket(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
