import unittest

from pycala import engine

from pycala.engine import board
from pycala.engine import tournament
from pycala.engine.players import ConfiguredPlayer

from pycala.players import basic

from pycala.util.tests import PycalaTestCase


class TournamentTests(PycalaTestCase):
    
    def test_score_board(self):
        """ Run through an example tournament and check the score board 
        creation is working properly.
        
        """
        
        PLAYER_LIST = []
        
        for i in range(0,5):
            cp = ConfiguredPlayer(basic.RandomPlayer, name="R%s" %i,)
            PLAYER_LIST.append(cp,)
        
        mt = tournament.MancalaTournament(PLAYER_LIST)
        mt.run()
        # TODO: Think of a test to validate the score_board result. 
        #    Always different so its hard... The only test could really 
        #    check the order but thats more testing the python sort 
        # built in than anything else...
        sb = mt.score_board()
        
    def test_mixed_short_tournament(self):
        """ Run through a tournament with 3 totally different minimax 
        players and 3 random players.
        
        """
        
        PLAYER_LIST = []
        
        for i in range(3):
            cp = ConfiguredPlayer(basic.RandomPlayer, name="R%s" %i,)
            PLAYER_LIST.append(cp,)
        
        for i in range (1,3):
            mm = basic.MiniMaxPlayer.objects.random(name="M%s"%i, settings={'max_depth':i,})
            PLAYER_LIST.append(mm)
        
        mt = engine.tournament.MancalaTournament(PLAYER_LIST)
        mt.run()
        sb = mt.score_board()
