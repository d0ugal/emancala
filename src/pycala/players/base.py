"""
Base player classes and player managers.

This very loosely follows the style of Django's models where you have a 
model for an instance and a manager for dealing with a set or multiple 
instances.

"""
import random
from warnings import warn

from pycala import engine
from pycala.util.exceptions import ImproperlyConfiguredError
from pycala.engine import players

class BasePlayerManager(object):
    
    def __init__(self, class_name):
        """Player class is initially stored as a string. This is because
        otherwise python looks for the class object before we have 
        finished defining it.
        
        """
        
        self._player_class = class_name
    
    @property
    def player_class(self):
        """ Check to see if the player class is being stored as a 
        string, if it is check the global namespace for the class and 
        grab the class object. After doing this save it over the string 
        so its ready for next time.
        
        """
        
        if self._player_class.__class__ == str:
            # load up the basic player module
            module = __import__('pycala.players.basic', fromlist=[self._player_class])
            # get the class from the module
            player_class = getattr(module, self._player_class)
            # store it
            self._player_class = player_class
        return self._player_class
    
    @player_class.setter
    def player_class(self, value):
        """ Nothing clever needs to be added in the setter as the getter
        does all the checking
        
        """
        
        self._player_class = value
    
    @player_class.deleter
    def player_class(self):
        """ Basic delete of the stored class """
        
        del self._player_class
    
    def _random_float(self, upper, lower):
        """ Create a random float between two upper and lower values. if
        upper and lower are just 1.0 and 0.0 then just return the result 
        of pythons random function rather than trying to do something 
        clever.
        
        Needs to be depreciated. random.triangular does the same job.
        
        """
        # TODO: depreciate method.
        return random.triangular(upper, lower)
    
    def random(self, name=None, lower=-1.0, upper=1.0, weights={}, settings={}):
        """ Create a randomly configured player. Weights and settings 
        are randomly generated between the lower and upper limits, 
        defaulted at 0.0 and 1.0. Optionally a weights and settings dict 
        can be passed in for any weights/settings that you want to fix. 
        In this instance only the other weights will be added randomly 
        to this dict. 
        
        """
        
        weights = weights.copy()
        settings = settings.copy()
        
        # copy over the list of requires weights
        required_weights = self.player_class.required_weights[:]
        # and settings
        required_settings = self.player_class.required_settings[:]
        
        # loop through required weights and create random weight for any
        # that have not been passed into this function.
        for rq_weight in required_weights:
            if not weights.has_key(rq_weight):
                if rq_weight.endswith('_multi'):
                    weights[rq_weight] = [self._random_float(upper, lower) for x in range(0,6)]
                else:
                    weights[rq_weight] = self._random_float(upper, lower)
        
        # See above, do the same for settings
        #for rq_setting in required_settings:
        #    if not settings.has_key(rq_setting):
        #       settings[rq_setting] = random.randrange()
        
        # Create an instance of the player simple to check that it passes
        # the configuration test. 
        player_obj = self.player_class(True, weights=weights, settings=settings, name=name)
        player_obj.check_setup()
        # Then discard it
        del player_obj
        
        # Create a configured player object that is ready to be placed in a game.
        return players.ConfiguredPlayer(
            self.player_class,
            name = name or "Randomly Generated %s" % self.player_class.name,
            settings=settings, weights=weights,
        )
         
class BasePlayer(object):
    
    name = "Base Mancala Player"
    required_weights = []
    required_settings = []
    
    objects = BasePlayerManager('BasePlayer')
    
    @property
    def weights(self):
        """ return weights dict """
        return self._weights
    
    @weights.setter
    def weights(self, dict):
        """ update weights with the added dict, never remove weights """
        self._weights.update(dict)
        
    @weights.deleter
    def weights(self):
        """ basic delete of the weights """
        del self._weights
    
    @property
    def settings(self):
        return self._settings
    
    @settings.setter
    def settings(self, dict):
        self._settings.update(dict)
        
    @settings.deleter
    def settings(self):
        del self._settings
    
    def __init__(self, player_side, settings={}, weights={}, name=None):
        """ Only required parameter is the player. If the player is A or
        B, this is used when making a moving so the algorithm knows what
        side of the board its interested in.
        
        Optional settings and weights if the player needs them and name 
        to make it easily identifiable.
        
        """
        # initialise the setting and weight dicts
        self._weights = {}
        self._settings = {}
        
        
        self.settings = settings.copy()
        self.weights = weights.copy()
        if name:
            self.name = name
        
        # set the player so we know what side of the board we are looking at
        self.player = player_side
        self.check_setup()
        
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.__str__()
    
    def check_setup(self):
        """ Checks that the player has all the required weights set.
        
        Also outputs a warning if any weights  are set that are 
        'not required' - basically weights are required or not used, so 
        if its not required its set by mistake.
        
        """
        
        def checker(set_values, required_values, verb):
            """ Checker to compare the set values vs the required 
            values. Process is the same for the settings and the 
            weights. Doesn't return anything but raises 
            ImproperlyConfiguredError if there is a problem.
            
            """
            # loop through all the set_values and make sure they are 
            # recognised. removing each weight as we go so we can 
            #identify what are missing.
            for key, value in set_values.items():
                if key not in required_values:
                    warn("Unrecognised %s '%s' in player '%s'" % (verb, key, self.name))
                else:
                    del set_values[key]
                    required_values.remove(key)
            
            # the remaining copy of required_weights contains the missing weights
            if len(required_values) > 0:
                raise ImproperlyConfiguredError, "Player '%s' is missing the following required %ss %s" % \
                    (self.name, verb, ", ".join(required_values))
        
        # Take a copy of the weights and required weights for us to work with
        copy_weights = self.weights.copy()
        copy_required_weights = self.required_weights[:]
        checker(copy_weights, copy_required_weights, 'weight')

        copy_settings = self.settings.copy()
        copy_required_settings = self.required_settings[:]
        checker(copy_settings, copy_required_settings, 'setting')
        
        return True
    
    def get_move(self, board):
        """
        Method for handling the calling of the players _get_move.
        """
        # First, check we have a valid player (again)
        self.check_setup()
        # Call _get_move ...
        return self._get_move(board)
    
    def _get_move(self, board):
        """ In essence this is a bit like an abstract method. The 
        players must overwrite this. It's a bit more flexible as it can 
        be replaced by any callable object. ImproperlyConfiguredError is
        raised if its not overwritten
        
        """
        raise ImproperlyConfiguredError, "Player doesn't have a _get_move method or base player is being called"
