class settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bgcolor = (230, 230, 230)

        self.ship_speed = 1.5
        self.ship_limit = 3

        self.rocket_speed = 4
        self.rocket_width = 25
        self.rocket_height = 4
        self.rocket_color = (60,60,60)
        self.rockets_allowed = 4

        #Halien settings
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        #fleet direction of 1 represents down and -1 represents up
        self.fleet_direction = 1

        #How quickly the game speeds up.
        self.speedup_scale = 1.1

        #How quickly the alien point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        #Scoring
        self.alien_points = 50


    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game. """
        self.ship_speed = 3.0
        self.rocket_speed = 6.0
        self.alien_speed = 3.0

        #Fleet direction of 1 represents down and -1 represents up
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings. """
        self.ship_speed *= self.speedup_scale
        self.rocket_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)



