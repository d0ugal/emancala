""" This contains no logic about how a player plays. It meerly is a wrapper
to contain a player with their name, weights and settings. Allowing for
easy reusable players. Since it generates instances of the player rather
than specifically passing around that player.

"""
import random

class ConfiguredPlayer(object):
    
    def __init__(self, player_class, weights={}, settings={}, name=None, skip_validation=False):
        
        weights = weights.copy()
        settings = settings.copy()
        
        self.player_class = player_class
        self.weights = weights
        self.settings = settings
        self.name = name or player_class.name
        
        self.for_points = 0
        self.away_points = 0
        
        # TODO: Change to won, lost, drawn from wins, looses, draws
        self.won = []
        self.lost = []
        self.drawn = []
        
        self.home_won = 0
        self.home_lost = 0
        self.away_won = 0
        self.away_lost = 0
        
        self.generations_survived = 0
        
        if not skip_validation:
            self.player_class(True, weights=weights, settings=settings)
    
    def __str__(self):
        return "%s %s" % (self.name, self.points())
    
    def __unicode__(self):
        return self.__str__()
    
    def create(self, player_side):
        return self.player_class(player_side=player_side,settings=self.settings, weights=self.weights, name=self.name)
    
    def points(self, method="football"):
        
        def football():
            win = len(self.won)
            draw = len(self.drawn)
            lose = len(self.lost)
            points = (win * 3) + (draw * 1) + (lose * 0)
            return points
        
        def rugby():
            win = len(self.won)
            draw = len(self.drawn)
            lose = len(self.lost)
            points = (win * 2) + (draw * 1) + (lose * 0)
            return points
        
        def wins_only(child):
            return len(self.won)
        
        def aged_football():
            return football() + self.generations_survived
        
        def loss_penalty():
            win = len(self.won)
            draw = len(self.drawn)
            lose = len(self.lost)
            points = (win * 3) + (draw * 1) + (lose * -1)
            return points
        
        def difference():
            return self.for_points - self.away_points
        
        mutation_methods = {'football':football, 'rugby':rugby, 
            'wins_only':wins_only, 'aged_football':aged_football, 
            'loss_penalty':loss_penalty, 'difference':difference,}
        
        return mutation_methods[method]()
    
    def weight_dither(self, percentage=1, include=None, exclude=None):
        """
        Adds a simple way to add dither 
        """
        weights_to_dither = self.weights.copy()
        
        if include is not None:
            for weight in weights_to_dither:
                if weight not in include:
                    weights_to_dither.remove(weight)
        elif exclude is not None:
            for weight in weights_to_dither:
                if weight in exclude:
                    weights_to_dither.remove(weight)
        
        for weight in weights_to_dither:
            # TODO: Add dither to 'multi' weights - at the moment they are skipped
            if weight.endswith('_multi'):
                new_multi = []
                for sub_weight in weights_to_dither[weight]:
                    dither_val = (1.0*sub_weight/100)*percentage
                    change = random.uniform(-dither_val,dither_val)
                    new_multi.append(sub_weight+change)
            else:
                dither_val = (1.0*self.weights[weight]/100)*percentage
                change = random.uniform(-dither_val,dither_val)
                self.weights[weight] += change
        
        return weights_to_dither

    def copy(self):
        new_self = ConfiguredPlayer(self.player_class, weights=self.weights, settings=self.settings, name=self.name, skip_validation=True)
        new_self.won = self.won[:]
        new_self.lost = self.lost[:]
        new_self.drawn = self.drawn[:]
        return new_self
