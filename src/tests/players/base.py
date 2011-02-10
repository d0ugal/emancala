import unittest

from pycala.players import base
from pycala.players import basic

from pycala.util import exceptions

class PlayerManager(unittest.TestCase):

    def test_random_minimax(self):
        """ Test the random MiniMax creation to make sure that the 
        randoms can be overwritten and the random values are also 
        different for each player.
        
        """
        
        lower = 0.0
        upper = 1.0
        weights = {'scrape':0.5,}
        weights2 = {'scrape':1.0,}
        settings = {'max_depth':4,}
        
        player_dict = basic.MiniMaxPlayer.objects.random(lower=lower, upper=upper, weights=weights, settings=settings)
        player_dict2 = basic.MiniMaxPlayer.objects.random(lower=lower, upper=upper, weights=weights2, settings=settings)
        
        self.assertEqual(player_dict.settings['max_depth'], 4)
        self.assertEqual(len(player_dict.weights['pits_multi']), 6)
        self.assertEqual(player_dict.weights['scrape'], 0.5)
        self.assertEqual(player_dict2.weights['scrape'], 1.0)
        
        # Check the weights are different, we know at least one will be
        # as we set 'scrape' for both of them.
        self.assertNotEqual(player_dict.weights, player_dict2.weights)