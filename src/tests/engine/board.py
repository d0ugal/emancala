import unittest

from pycala import engine
from pycala.engine import board
from pycala.engine import players

from pycala.players import basic

from pycala.util.exceptions import InvalidMoveError, TurnNotFinishedError
from pycala.util.tests import PycalaTestCase

class MancalaBoardTests(PycalaTestCase):
    
    def test_setup(self):
        """ Checking the initial values are set up correctly """
        
        # Check the board is valid
        self.assertEqual(self.board.pits, engine.VALID_START_BOARD)
        # Check the player is valid
        self.assertEqual(self.board.whos_turn(), engine.PLAYER_A)
    
    def test_valid_move(self):
        """ Testing a valid move being made on a start board """
        
        self.board.move(0, commit=True)
        
        # The board should look like the following list
        new_board = [0,5,5,5,5,4,0,4,4,4,4,4,4,0]
        self.assertEqual(self.board.pits, new_board)
        
        # The player should now have changed to B
        self.assertEqual(self.board.whos_turn(),engine.PLAYER_B)
    
    def test_invalid_move(self):
        """ Testing the process of making invalid moves """
        self.board.set_turn(engine.PLAYER_B)
        
        self.assertRaises(InvalidMoveError, self.board.move, 0, commit=True)
        
        # board should still be in engine.VALID_START_BOARD state
        self.assertEqual(self.board.pits, engine.VALID_START_BOARD)
        
        # The player should not have changed to A since the move was invalid
        self.assertEqual(self.board.whos_turn(),engine.PLAYER_B)
    
    def test_multiple_turns(self):
        """ Test a number of moves in a seqeuence and check the board
        matches up with what is expected after each move.
        
        """
        self.assertEqual(self.board.pits, engine.VALID_START_BOARD)
        self.board.move(5, commit=True)
        self.assertEqual(self.board.pits, [4,4,4,4,4,0,1,5,5,5,4,4,4,0])
        self.board.move(7, commit=True)
        self.assertEqual(self.board.pits, [4,4,4,4,4,0,1,0,6,6,5,5,5,0])
        self.board.move(4, commit=True)
        self.assertEqual(self.board.pits, [4,4,4,4,0,1,2,1,7,6,5,5,5,0])
    
    def test_move_sequence(self):
        """ Since some turns consist of more than one move these are
        now grouped together into one turn rather than being multiple. 
        this tests the repeat moves.
        
        """
        self.setUp()
        self.board.move([2,0], commit=True)
        self.assertEqual(self.board.pits, [0,5,1,6,6,5,1,4,4,4,4,4,4,0])
        
        self.setUp()
        new_board = self.board.move([2,0,], commit=False)
        self.assertEqual(new_board.pits, [0,5,1,6,6,5,1,4,4,4,4,4,4,0])
        
    def test_ending_in_home(self):
        """ Testing a move that ends in the players home. If it does, 
        then the player gets another turn and it shouldn't be swapped to
        the other player
        
        """
        # ends in home, exception is raised because turn isn't finished
        self.assertRaises(TurnNotFinishedError, self.board.move, 2, commit=True)
        
        # The player should not have changed to B since move was invalid
        self.assertEqual(self.board.whos_turn(),engine.PLAYER_A)
        
        # Validate the new board too.
        # The board should look like the following list
        new_board = [4,4,0,5,5,5,1,4,4,4,4,4,4,0]
        self.assertEqual(self.board.pits, new_board)
        
        # reset and start with player_b
        self.setUp()
        self.board.set_turn(engine.PLAYER_B)
        self.assertRaises(TurnNotFinishedError, self.board.move, 9, commit=True)
        new_board = [4,4,4,4,4,4,0,4,4,0,5,5,5,1]
        self.assertEqual(self.board.pits, new_board)
        self.assertEqual(self.board.whos_turn(),engine.PLAYER_B)
        
        # reset
        self.setUp()
        # this time run a turn that has multiple moves but finishes the 
        # turn. so no exception should be raised.
        self.board.move([2,1], commit=True)
        
        # Validate new board...
        new_board = [4,0,1,6,6,6,1,4,4,4,4,4,4,0]
        self.assertEqual(self.board.pits, new_board)
        
    def test_game_copy(self):
        """ Checks the abilit for a board to return a copy of itself or 
        commit a move.
        
        """
        
        # A move without a commit should mean the new board is different
        # from the old board.
        new_board = self.board.move(0)
        self.assertNotEqual(self.board.pits,new_board.pits)
        
        # A move with a commit should mean the boards are the same object
        new_board2 = self.board.move(0, commit=True)
        self.assertEqual(self.board,new_board2)
    
    def test_legal_moves(self):
        """ This test checks that the finding legal moves function works
        on the start move.
        
        """
        lm_a = self.board.get_legal_moves()
        self.assertEqual(lm_a, [0,1,2,3,4,5])
        
        # For each legal move, try it out without a commit.
        for pit in lm_a:
            # assume if there are no errors its ok.
            # overriding check for finishing turn
            self.board.move(pit, override_checks=True)
            
        # Swap the player go through the same process.
        self.board.set_turn(engine.PLAYER_B)
        lm_b = self.board.get_legal_moves()
        self.assertEqual(lm_b, [7,8,9,10,11,12])
        
        # For each legal move, try it out without a commit.
        for pit in lm_b:
            # assume if there are no errors its ok.
            # overriding check for finishing turn
            self.board.move(pit, override_checks=True)
    
    def test_get_possible_turns(self):
        """ Get all the possible turns
        
        """
        
        # starting position should have 10 possible moves.
        possible_moves = list(self.board.get_possible_turns())
        self.assertEqual(len(possible_moves), 10)
        
        # Variation on early board
        self.board.pits = [4,4,4,4,0,4,0,4,4,4,4,4,4,0]
        possible_moves = list(self.board.get_possible_turns())
        self.assertEqual(len(possible_moves), 9)
        
        # Variation on early board
        self.board.pits = [4,4,4,4,0,0,0,4,4,4,4,4,4,0]
        possible_moves = list(self.board.get_possible_turns())
        self.assertEqual(len(possible_moves), 11)
        
        # board after a number of moves in.
        self.board.pits = [4,4,0,5,5,0,2,0,1,7,7,6,6,1,]
        possible_moves = list(self.board.get_possible_turns())
        self.assertEqual(len(possible_moves), 4)
        
        # Suddnly a HUGE jump in the possible turns by having just 2
        # more in the first pit.
        self.board.pits = [6,4,4,4,0,0,0,4,4,4,4,4,4,0]
        possible_moves = list(self.board.get_possible_turns())
        self.assertEqual(len(possible_moves), 80)
        
        # Very rare possibility. highest found number of possible turns
        self.board.pits = [6,5,4,3,2,1,0,4,4,4,4,4,4,0]
        possible_moves = list(self.board.get_possible_turns())
        self.assertEqual(len(possible_moves), 912)
        
        
        # identifying a problem where if players only has one piece left
        # and the move ends in the home the possible_turn calculator 
        # looks for a second move but can't find one.
        # example below shows player b with a stone in pit 12 only that
        # they cna move.
        self.board.pits = [0,5,5,0,0,0,18,0,0,0,0,0,1,19,]
        self.board.set_turn(engine.PLAYER_B)
        possible_moves = list(self.board.get_possible_turns())
        self.assertEqual(len(possible_moves), 1)
        self.assertEqual(possible_moves, [[12,],])
        
        # same as the example above but for player A
        self.board.pits = [0,0,0,0,0,1,16,0,0,0,2,0,1,28,]
        self.board.set_turn(engine.PLAYER_A)
        possible_moves = list(self.board.get_possible_turns())
        self.assertEqual(len(possible_moves), 1)
        self.assertEqual(possible_moves, [[5,],])
        
    def test_is_legal_move(self):
        """ Checks to see if the legal move calulations are valid on a 
        new board and on the legal moves of each player
        
        """
        self.board.set_turn(engine.PLAYER_A)
        for i in range(0,6):
            self.board.is_legal_move(i)
        
        self.board.set_turn(engine.PLAYER_B)
        for i in range(7,13):
            self.board.is_legal_move(i)
        
        self.assertRaises(InvalidMoveError, self.board.move, 20)
    
    def test_opposite(self):
        """ Check the calculations of the opposite pit is correct
        
        """
        self.assertEqual(self.board.opposite_pit(0), 12)
        self.assertEqual(self.board.opposite_pit(1), 11)
        self.assertEqual(self.board.opposite_pit(2), 10)
        self.assertEqual(self.board.opposite_pit(3), 9)
        self.assertEqual(self.board.opposite_pit(4), 8)
        self.assertEqual(self.board.opposite_pit(5), 7)
        self.assertEqual(self.board.opposite_pit(6), 13)
        self.assertEqual(self.board.opposite_pit(7), 5)
        self.assertEqual(self.board.opposite_pit(8), 4)
        self.assertEqual(self.board.opposite_pit(9), 3)
        self.assertEqual(self.board.opposite_pit(10), 2)
        self.assertEqual(self.board.opposite_pit(11), 1)
        self.assertEqual(self.board.opposite_pit(12), 0)
        self.assertEqual(self.board.opposite_pit(13), 6)
    
    def test_opposite_capture(self):
        """ Test 'capture' move when the move ends in an empty pit
        
                            PLAYER B (FALSE)
        .----------------------------------------------.
        | .----. .--. .--. .--. .--. .--. .--. .----.  |
        | |    | | 4| | 4| | 4| | 4| | 4| | 4| |    |  |
        | |  0 | '--' '--' '--' '--' '--' '--' |  0 |  |
        | |    | .--. .--. .--. .--. .--. .--. |    |  |
        | |    | | 2| | 1| | 0| | 8| | 1| |10| |    |  |
        | '----' '--' '--' '--' '--' '--' '--' '----'  |
        '----------------------------------------------'
                            PLAYER A (TRUE)
        
        This set-up provides 3 different test cases for an opposide 
        capture all for capturing pit 10. It can be captured by 
        player A moving 0, 1 or 5
        
        """
        
        capture_setup = [2,1,0,8,1,10,0,4,4,4,4,4,4,0]
        
        self.board.pits = capture_setup[:]
        self.board.set_turn(engine.PLAYER_A)
        self.board.move(0, commit=True)     # move 0 for a simple capture
        self.assertEqual(self.board.pits, [0,2,0,8,1,10,5,4,4,4,0,4,4,0])
        
        self.board.pits = capture_setup[:]
        self.board.set_turn(engine.PLAYER_A)
        self.board.move(1, commit=True)     # move 1 for a simple capture
        self.assertEqual(self.board.pits, [2,0,0,8,1,10,5,4,4,4,0,4,4,0])
        
        self.board.pits = capture_setup[:]
        self.board.set_turn(engine.PLAYER_A)
        self.board.move(5, commit=True)     # move 5 for a loop-around capture
        self.assertEqual(self.board.pits, [3,2,0,8,1,0,7,5,5,5,0,5,5,0])
        
        #self.board.pits = []
        #self.board.set_turn(engine.PLAYER_B)
        #self.board.move(pits, commit, override_checks)
    
    def test_score(self):
        """ Test the score calculation - while this is only normally 
        calculated at the end, this example shows it being calculated at
        a midpoint in the game.
        
        """
        # Starting board, both should have the sum of 6 pits x 4 stones = 24
        self.assertEqual(self.board.scores(), (24,24))
        
        """
                            PLAYER B (FALSE)
        .----------------------------------------------.
        | .----. .--. .--. .--. .--. .--. .--. .----.  |
        | |    | | 1| | 0| | 0| | 0| | 0| | 0| |    |  |
        | | 29 | '--' '--' '--' '--' '--' '--' | 18 |  |
        | |    | .--. .--. .--. .--. .--. .--. |    |  |
        | |    | | 0| | 0| | 0| | 0| | 0| | 0| |    |  |
        | '----' '--' '--' '--' '--' '--' '--' '----'  |
        '----------------------------------------------'
                            PLAYER A (TRUE)
        """
        self.board.pits = [0,0,0,0,0,0,18,0,0,0,0,0,1,29]
        self.assertEqual(self.board.scores(), (18,30))
        
        """
                            PLAYER B (FALSE)
        .----------------------------------------------.
        | .----. .--. .--. .--. .--. .--. .--. .----.  |
        | |    | | 0| | 1| | 2| | 0| | 2| | 1| |    |  |
        | | 18 | '--' '--' '--' '--' '--' '--' | 23 |  |
        | |    | .--. .--. .--. .--. .--. .--. |    |  |
        | |    | | 0| | 0| | 0| | 0| | 1| | 0| |    |  |
        | '----' '--' '--' '--' '--' '--' '--' '----'  |
        '----------------------------------------------'
                            PLAYER A (TRUE)
        """
        self.board.pits = [0,0,0,0,1,0,23,1,2,0,2,1,0,18]
        self.assertEqual(self.board.scores(), (24,24))
    
    def test_game_history(self):
        """ Check the stored game history is valid. The game history
        should be be a list containing all the moves made in the game
        in their correct order.
        
        """
        
        self.assertEqual(self.board.game_history, [])
        
        self.board.move([3,], commit=True)
        self.assertEqual(len(self.board.game_history), 1)
        self.assertEqual(self.board.game_history[0].move_sequence, [3,])
        self.board.move([7,], commit=True)
        self.assertEqual(len(self.board.game_history), 2)
        self.assertEqual(self.board.game_history[1].move_sequence, [7,])
        self.board.move([2,1,], commit=True)
        self.assertEqual(len(self.board.game_history), 3)
        self.assertEqual(self.board.game_history[2].move_sequence, [2,1,])
        self.board.move([8,10,], commit=True)
        self.assertEqual(len(self.board.game_history), 4)
        self.assertEqual(self.board.game_history[3].move_sequence, [8,10,])
        self.board.move([1,], commit=True)
        self.assertEqual(len(self.board.game_history), 5)
        self.assertEqual(self.board.game_history[4].move_sequence, [1,])
        self.board.move([9,], commit=True)
        self.assertEqual(len(self.board.game_history), 6)
        self.assertEqual(self.board.game_history[5].move_sequence, [9,])
        self.board.move([5,], commit=True)
        self.assertEqual(len(self.board.game_history), 7)
        self.assertEqual(self.board.game_history[6].move_sequence, [5,])


class MancalaGame(PycalaTestCase):
    
    def setUp(self, *args, **kwargs):
        """ Set up new board for each test. Fresh piece position and 
        default player turn to A
        
        """
        super(MancalaGame, self).setUp(*args, **kwargs)
    
    def test_game(self):
        """ Run through 10,000 test games with random players.
        For testing the game player and also testing game rules. 10,000
        totally games are likely to explore most of the game rules and
        find any flaws.
        
        """
        
        for i in range(10000):
            player_a = players.ConfiguredPlayer(basic.RandomPlayer, name="R A",)
            player_b = players.ConfiguredPlayer(basic.RandomPlayer, name="R B",)
        
            mg = board.MancalaGame(player_a, player_b)
        mg.run_game()
    
    def test_minimax_game(self):
        """ Run through a sample test game with MiniMax players.
        
        """
        settings={'max_depth':2,}
        player_a = basic.MiniMaxPlayer.objects.random(name="MM 1", settings=settings.copy())
        player_b = basic.MiniMaxPlayer.objects.random(name="MM 2", settings=settings.copy())
        player_a = players.ConfiguredPlayer(basic.RandomPlayer, name="R A",)
        player_b = players.ConfiguredPlayer(basic.RandomPlayer, name="R B",)
        mg = board.MancalaGame(player_a, player_b)
        mg.run_game()

class BoardSerializer(PycalaTestCase):
    
    def test_int_to_binary(self):
        """ Integer to binary conversion.
        
        """
        repr = board.BoardSerializer()
        
        self.assertEqual(repr._int_to_bin(0),  '00000000')
        self.assertEqual(repr._int_to_bin(1),  '00000001')
        self.assertEqual(repr._int_to_bin(2),  '00000010')
        self.assertEqual(repr._int_to_bin(3),  '00000011')
        self.assertEqual(repr._int_to_bin(4),  '00000100')
        self.assertEqual(repr._int_to_bin(5),  '00000101')
        self.assertEqual(repr._int_to_bin(6),  '00000110')
        self.assertEqual(repr._int_to_bin(7),  '00000111')
        self.assertEqual(repr._int_to_bin(8),  '00001000')
        self.assertEqual(repr._int_to_bin(9),  '00001001')
        self.assertEqual(repr._int_to_bin(10), '00001010')
        self.assertEqual(repr._int_to_bin(11), '00001011')
        self.assertEqual(repr._int_to_bin(12), '00001100')
        self.assertEqual(repr._int_to_bin(13), '00001101')
        self.assertEqual(repr._int_to_bin(14), '00001110')
    
    def test_board_reverse(self):
        """ Board reversing. Since it doesn't matter what player you are
        the board is effectively symmetrical, so to avoid storing dupes
        the board is reverse for player B
        
        """
        repr = board.BoardSerializer()
        
        self.assertEqual(repr._reverse(self.board.pits), engine.VALID_START_BOARD)
        self.assertEqual(repr._reverse([4,4,4,4,4,4,0,4,4,4,4,4,4,0]), [4,4,4,4,4,4,0,4,4,4,4,4,4,0])
        self.assertEqual(repr._reverse([4,4,4,4,4,5,0,4,4,4,4,4,3,0]), [4,4,4,4,4,3,0,4,4,4,4,4,5,0])
        self.assertEqual(repr._reverse([4,4,4,4,4,6,0,4,4,4,4,4,2,0]), [4,4,4,4,4,2,0,4,4,4,4,4,6,0])
        self.assertEqual(repr._reverse([4,4,4,4,4,7,0,4,4,4,4,4,1,0]), [4,4,4,4,4,1,0,4,4,4,4,4,7,0])
        self.assertEqual(repr._reverse([1,2,3,4,5,6,7,8,9,10,11,12,13,14]), [8,9,10,11,12,13,14,1,2,3,4,5,6,7])
    
    def test_as_binary(self):
        """ Board being serialized to binary.
        
        """
        
        repr = board.BoardSerializer()
        
        self.assertEqual(repr.as_binary(self.board),"0000010000000100000001000000010000000100000001000000000000000100000001000000010000000100000001000000010000000000")
        
    def test_from_binary(self):
        """ Board being serialized from binary.
        
        """
        
        repr = board.BoardSerializer()
        
        r = repr.from_binary('0000010000000100000001000000010000000100000001000000000000000100000001000000010000000100000001000000010000000000')
        
        self.assertEqual(r.pits, engine.VALID_START_BOARD)