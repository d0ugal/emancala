import unittest

from pycala.util.tests import PycalaTestCase
from pycala import engine
from pycala.engine import feature_detection

class DetectorTests(PycalaTestCase):
    
    def setUp(self):
        """
        Set up new board for each test. Fresh piece position and default player turn to A
        """
        super(DetectorTests, self).setUp()
        
        self.feature_detection = feature_detection.Detector(self.board)
        
    def test_scrape(self):
        """ Test the scrape feature detection.
        
        """
        
        # Start board, nobody has more than 24
        value = self.feature_detection.scrape(100.0)
        self.assertEqual(value, 0)
        
        # fake board, nobody has more than 24
        self.board.pits = [0,0,0,0,0,1,23,0,0,0,0,0,1,23]
        value = self.feature_detection.scrape(100.0)
        self.assertEqual(value, 0)
        
        # fake board, both players have 24. draw state.
        self.board.pits = [0,0,0,0,0,0,24,0,0,0,0,0,0,24]
        value = self.feature_detection.scrape(100.0)
        self.assertEqual(value, 0)
        
        # fake board, player A has > 24, player A's turn
        self.board.pits = [0,0,0,0,0,0,25,0,0,0,0,0,0,23]
        value = self.feature_detection.scrape(100.0)
        self.assertEqual(value, 100.0)
        
        # fake board, player A has > 24, player B's turn
        self.board.pits = [0,0,0,0,0,0,25,0,0,0,0,0,0,23]
        self.board.set_turn(engine.PLAYER_B)
        value = self.feature_detection.scrape(100.0)
        self.assertEqual(value, -100.0)
        
        
        # fake board, player B has > 24
        self.board.pits = [0,0,0,0,0,0,23,0,0,0,0,0,0,25]
        self.board.set_turn(engine.PLAYER_A)
        value = self.feature_detection.scrape(100.0)
        self.assertEqual(value, -100.0)
        
        self.setUp()
        self.board.set_turn(engine.PLAYER_B)
        # fake board, player B has > 24
        self.board.pits = [0,0,0,0,0,0,23,0,0,0,0,0,0,25]
        value = self.feature_detection.scrape(100.0)
        self.assertEqual(value, 100.0)
        
    def test_store(self):
        """ Test the store weighting by following through part of a game
        and comparing the store results to those expected.
        
        Comments with A and B show what players turn it is at that 
        point, this is important to consider since results are negated
        depending on the player.
        
        """
        # A
        value = self.feature_detection.store(0.5)
        self.assertEqual(value, 0)
        self.board.move([2,4,], commit=True)
        
        # B
        value = self.feature_detection.store(1)
        self.assertEqual(value, -2)
        self.board.move([8,7,], commit=True)
        
        # A
        value = self.feature_detection.store(0.5)
        self.assertEqual(value, 0.5)
        self.board.move([0,], commit=True)
        
        # B
        value = self.feature_detection.store(1)
        self.assertEqual(value, -3)
        self.board.move([12,], commit=True)
        
        # A
        value = self.feature_detection.store(0.5)
        self.assertEqual(value, 1)
        self.board.move([2,], commit=True)
        
        # B
        value = self.feature_detection.store(1)
        self.assertEqual(value, -2)
        self.board.move([9,], commit=True)
        
        # A
        value = self.feature_detection.store(0.25)
        self.assertEqual(value, 0.25)
        self.board.move([4,1], commit=True)
        
        # B
        value = self.feature_detection.store(1)
        self.assertEqual(value, -3)
        self.board.move([8,], commit=True)
        
        # A
        value = self.feature_detection.store(0.25)
        self.assertEqual(value, -1.75)
    
    def test_score(self):
        """ Test the 'score' feature detection. 'score' can be sumarised
        as sum(a_pits + a_home) - sum(b_pits - b_home) - for player a.
        swapped for player b.
        
        """
        value = self.feature_detection.score(1.0)
        self.assertEqual(value, 0)
        
        self.board.move(5, commit=True)
        self.board.move(7, commit=True)
        self.board.move(4, commit=True)
        
        value = self.feature_detection.score(1.0)
        self.assertEqual(value, 10.0)
    
    def test_stance(self):
        """ Test the stance feature detection.
        
        """
        
        # A
        value = self.feature_detection.stance(1.0)
        self.assertEqual(value, 0)
        self.board.move(5, commit=True)
        
        # B
        value = self.feature_detection.stance(1.0)
        self.assertEqual(value, 7)
        
        # A
        self.board.pits = [2,8,6,0,6,1,8,1,1,0,1,2,8,4]
        self.board.set_turn(engine.PLAYER_A)
        value = self.feature_detection.stance(1.0)
        self.assertEqual(value, 0)
        
        # A
        self.board.pits = [2,8,6,0,6,1,8,1,1,2,1,0,8,4]
        self.board.set_turn(engine.PLAYER_A)
        value = self.feature_detection.stance(1.0)
        self.assertEqual(value, -4.0)
        
        # B
        self.board.set_turn(engine.PLAYER_B)
        value = self.feature_detection.stance(1.0)
        self.assertEqual(value, 4.0)
        
    def test_pits(self):
        """ Test the individual pit weighting method.
        
        """
        
        # TODO: This could do with more example scenarios
        
        weights = [1.0,1.0,1.0,1.0,1.0,1.0,]
        
        value = self.feature_detection.pits(weights)
        self.assertEqual(value, 0)