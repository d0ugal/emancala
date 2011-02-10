import unittest

from pycala.engine import board


class PycalaTestCase(unittest.TestCase):
    """
    Simple class that sets up a number of vars that are used in most tests
    """
    
    def setUp(self):
        """
        Set up new board for each test. Fresh piece position and default player turn to A
        """
        self.board = board.MancalaBoard()
        super(PycalaTestCase, self).setUp()