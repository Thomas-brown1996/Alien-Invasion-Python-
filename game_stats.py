class GameStats:
    """track player score"""

    def __init__(self, ai_game):
        """initialise statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        #start game in an inactive state
        self.game_active = False

        #gamestats should never be reset
        self.high_score = 0




    def reset_stats(self):
        """initialise changable statistics"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1