class Settings:
    """class store for all settings"""

    def __init__(self):
        """initialization"""
        #screen settings
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        #ship- settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        #alien settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10

        #fleet directiom -1 equals left, 1 equals right
        self.fleet_direction = 1

        #how quickly the game speeds up
        self.speedup_scale = 1.1

        #how quickly the game speeds up
        self.score_scale = 1.5

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        """initialise dynamic settings"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        self.fleet_direction = 1

        #scoring
        self.alien_points = 50
    
    def increase_speed(self):
        """increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)


     