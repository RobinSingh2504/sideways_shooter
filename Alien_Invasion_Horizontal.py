import  sys

import pygame

from hsettings import settings

from Horizontal_Ship import Hship

from rocket import Rocket

from h_alien import Halien

from time import sleep

from H_gamestats import Gamestats

from button import  Button

from scoreboard import Scoreboard

class h_alienInvasion():


    def __init__(self):
        pygame.init()
        self.settings = settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.ship = Hship(self)
        self.rockets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #Make the play button
        self.play_button = Button(self, "Click to Play")

        #Create an instance to store game statistics and scoreboard
        self.stats = Gamestats(self)
        self.sb = Scoreboard(self)



    def _create_fleet(self):
        """Create a fleet of aliens. """
        halien = Halien(self)
        alien_width, alien_height = halien.rect.size
        available_space_y = self.settings.screen_height - (2 * alien_height)
        number_of_aliens_y = available_space_y // (2 * alien_height)

        ##Determine the number of columns of aliens that would fit on the screen.
        ship_height = self.ship.rect.height
        avalable_space_x = self.settings.screen_width - (10 * alien_width) - (ship_height)
        number_of_columns_x =  avalable_space_x // (2 * alien_width)

        # create the fleet of aliens.
        for row_number in range(number_of_columns_x):
            for alien_number in range(number_of_aliens_y):
                """Create the alien and put in the row."""
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create the fleet of aliens. """
        """Spacing between each alien is equal to one alien width """
        halien = Halien(self)
        alien_width, alien_height = halien.rect.size
        halien.y = alien_height + ( 2 * alien_height * alien_number)
        halien.rect.y = halien.y
        halien.rect.x = self.settings.screen_width - (halien.rect.width + (2 * halien.rect.width * row_number))
        self.aliens.add(halien)

    def _update_aliens(self):
        """Update the positions of aliens in the fleet. """
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for aliens hitting the left of the screen.
        self._check_aliens_left()


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge. """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction. """
        for alien in self.aliens.sprites():
            alien.rect.x -=  self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_rockets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_aliens_left(self):
        """ Check if any aliens have reached the left of the screen. """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.left <=  screen_rect.left:
                #Treat this the same as if the ship got hit.
                self._ship_hit()
                break


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play. """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game settings
            self.settings.initialize_dynamic_settings()
            #Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.aliens.empty()
            self.rockets.empty()
            self._create_fleet()
            self.ship.center_ship()

            #Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):

        if event.key == pygame.K_UP:
            self.ship.moving_top = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_rocket()
        elif event.key == pygame.K_q:

            sys.exit()

    def _ship_hit(self):
        """Respond to the ship being hit by the aline. """
        if self.stats.ships_left > 0:
            #Decrement ships left.
            self.stats.ships_left -= 1

            #get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.rockets.empty()

            #Create a new fleet and center ths ship
            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.ship.moving_top = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_rocket(self):
        if len(self.rockets) < self.settings.rockets_allowed:
            new_rocket = Rocket(self)
            self.rockets.add(new_rocket)

    def _update_rockets(self):
        self.rockets.update()

        for rocket in self.rockets.copy():
            if rocket.rect.right > self.screen.get_rect().width:
                self.rockets.remove(rocket)
        self._check_rocket_alien_collisions()

    def _check_rocket_alien_collisions(self):

        #Check for any rockets that have hit the aliends.
        #If so, get rid of the rockets and the aliens
        collisions = pygame.sprite.groupcollide(self.rockets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.rockets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_screen(self):
        self.screen.fill(self.settings.bgcolor)
        self.ship.blitme()

        for rocket in self.rockets.sprites():
            rocket.draw_rocket()
        self.aliens.draw(self.screen)

        #Draw the score information.
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ =='__main__':
    ai = h_alienInvasion()
    ai.run_game()