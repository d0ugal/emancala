from pycala.util.tests import PycalaTestCase

from pycala import engine
from pycala.engine import tournament
from pycala.players import basic

class RandomPlayer(PycalaTestCase):
    
    def test_random(self):
        """ Create a Random player. Set its turn as the current player 
        and ask for its move. Finally check the move it provided is 
        valid. Do this 10000 times since its sooo quick
        
        """
        for i in xrange(0,1000):
            rand = basic.RandomPlayer(self.board.whos_turn())
            result = rand.get_move(self.board)
            self.board.move(result)

class HumanPlayer(PycalaTestCase):
    # TODO: Human testing? Unsure how to test. Probably not needed.
    pass

class MiniMaxPlayer(PycalaTestCase):
    
    def test_minimax(self):
        """ Create a MiniMax player. Set its turn as the current player 
        and ask for its move. Finally check the move it provided is 
        valid. Repeat for depths one through to five.
        
        """
        
        for i in range(1,6):
            settings = {'max_depth':i,}
            conf_mm = basic.MiniMaxPlayer.objects.random(settings=settings)
            self.board.set_turn(engine.PLAYER_B)
            mm = conf_mm.create(self.board.whos_turn())
            
            result = mm.get_move(self.board)
            
            
            self.board.move(pits=result,)
            
            self.assertEqual(mm.nodes_at_depth[0], 1)
            self.assertEqual(mm.nodes_at_depth[1], 10)
            
            # bunch of recorded node counts from a starting board
            # position. Checked for regression.
            if i >= 2:
                self.assertEqual(mm.nodes_at_depth[2], 116)
            if i >= 3:
                self.assertEqual(mm.nodes_at_depth[3], 1022)
            if i >= 4:
                self.assertEqual(mm.nodes_at_depth[4], 9682)
            if i >= 5:
                self.assertEqual(mm.nodes_at_depth[5], 125843)
            if i >= 6:
                self.assertEqual(mm.nodes_at_depth[6], 1090937)
    
    def test_minimax_depth(self):
        """ A tournament of minimax players with the same weights but 
        different depths - should give a fairly good test as to how the 
        depth of the search tree effects the result.
        
        """
        
        number_of_each = 1
        max_depth = 4
        
        PLAYER_LIST = []
        
        random_bases = []
        for x in xrange(0,number_of_each):
            random_bases.append(basic.MiniMaxPlayer.objects.random(name="M2%s" %x, settings={'max_depth':1,}))
            random_bases.append(basic.MiniMaxPlayer.objects.random(name="M2%s" %x, settings={'max_depth':1,}))
        
        for y in xrange(1,max_depth+1):
            for i in xrange(0,number_of_each):
                PLAYER_LIST.append(basic.MiniMaxPlayer.objects.random(name="M%s%s" %(y,i), weights=random_bases[i].weights, settings={'max_depth':y,}))
        
        mt = tournament.MancalaTournament(PLAYER_LIST)
        mt.run()
        sb = mt.score_board()