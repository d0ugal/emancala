from pycala.util.tests import PycalaTestCase

from pycala.players import basic

class ConfiguredPlayer(PycalaTestCase):
    
    def test_player_dither(self):
        """ Test player dither, applys dither and checks changes made.
        
        """
        # TODO: Actually test
        player_dict = basic.MiniMaxPlayer.objects.random(settings={'max_depth':4,})
        current_weights = player_dict.weights.copy()
        player_dict.weight_dither(10)
        new_weights = player_dict.weights.copy()
        
        # Check they have at least changed...
        self.assertNotEqual(current_weights, new_weights)