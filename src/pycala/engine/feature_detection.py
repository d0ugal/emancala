from pycala import engine

class Detector(object):
    
    def __init__(self, current_board):
        """ Takes in the board to work with. Assumes the current player 
        is result of current_board.whos_turn()
        
        """
        self.current_board = current_board
    
    def scrape(self, weight,):
        """ Detection of a loosing case. Games have x pits and thus if 
        a player captures more than x/2 stones they have won even if the 
        game hasn't technically finished. This function doesn't care how 
        much the player is winning or loosing by but mearley if an 
        end game case has/will be reached.
        
        """
        
        val = 0.0
        
        total = sum(self.current_board.pits)
        need_to_win = total/2
        
        # See if its a winning state for player A
        if self.current_board.pits[engine.HOME_A] >= need_to_win:
            val += weight
        
        # see if its a winning state for player B
        if self.current_board.pits[engine.HOME_B] >= need_to_win:
            val -= weight
        
        # if its player b thats playing negate the result.
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
        
    def store(self, weight,):
        """ Weighting for how many pits are currently in the players
        home pit
        
        """
        val = self.current_board.pits[engine.HOME_A] * weight
        
        val += -(self.current_board.pits[engine.HOME_B] * weight)
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    
    def score(self, weight,):
        """ Weighting for the current 'score' this isn't technically
        the score in Mancala as there isn't a case for the current
        score. However, its based on the rules where the stones 
        on the players side of the board and in their home pit
        'belong' to them
        
        """
        
        a_score, b_score = self.current_board.scores()
        val = a_score * weight
        val += -(b_score * weight)
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
        
    def stance(self, weight,):
        """ Weighting for the stance of the player. Based on the 
        position of the stones of their side of the board. Basically 
        allowing differentiation between the first three pits and the 
        last three pits to focus having the pits at the back or the 
        front.
        
        """
        
        # TODO: Not sure this one seems quite right TBH
        # seems to work!
        a_front_pits = self.current_board.pits[3:6]
        a_back_pits = self.current_board.pits[0:3]
        b_front_pits = self.current_board.pits[7:10]
        b_back_pits = self.current_board.pits[10:13]
        
        a_stance = sum(a_front_pits) - sum(a_back_pits)
        b_stance = sum(b_front_pits) - sum(b_back_pits)
        
        val = a_stance * weight
        val += -(b_stance * weight)
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
        
    def pits(self, weights,):
        """ Weighting for each individual pit. This allows for very 
        flexible feature detection with the EA where it may be able to 
        notice that a specific pit for some reason provides more wins if
        there are n stones in it.
        
        """
        
        if weights.__class__ == float:
            print weights
            raise Exception, "Invalid weights for 'pits': %s" % weights
        
        val = 0
        
        for pit,weight in enumerate(weights):
            if self.current_board.whos_turn() == engine.PLAYER_B:
                val -= self.current_board.pits[pit+7] * weights[pit]
                val += self.current_board.pits[pit] * weights[pit]
            else:
                val -= self.current_board.pits[pit] * weights[pit]
                val += self.current_board.pits[pit+7] * weights[pit]
        
        return val
    
    def pit0(self, weight):
        """ Weighting for the pit 0 """
        
        val = self.current_board.pits[0] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit1(self, weight):
        """ Weighting for the pit 1 """
        
        val = self.current_board.pits[1] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit2(self, weight):
        """ Weighting for the pit 2 """
        
        val = self.current_board.pits[2] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit3(self, weight):
        """ Weighting for the pit 3 """
        
        val = self.current_board.pits[3] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit4(self, weight):
        """ Weighting for the pit 4 """
        
        val = self.current_board.pits[4] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit5(self, weight):
        """ Weighting for the pit 5 """
        
        val = self.current_board.pits[5] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit6(self, weight):
        """ Weighting for the pit 6 """
        
        val = self.current_board.pits[6] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit7(self, weight):
        """ Weighting for the pit 7 """
        
        val = self.current_board.pits[7] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit8(self, weight):
        """ Weighting for the pit 8 """
        
        val = self.current_board.pits[8] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit9(self, weight):
        """ Weighting for the pit 9 """
        
        val = self.current_board.pits[9] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit10(self, weight):
        """ Weighting for the pit 10 """
        
        val = self.current_board.pits[10] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit11(self, weight):
        """ Weighting for the pit 11 """
        
        val = self.current_board.pits[11] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit12(self, weight):
        """ Weighting for the pit 12 """
        
        val = self.current_board.pits[12] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val
    def pit13(self, weight):
        """ Weighting for the pit 13 """
        
        val = self.current_board.pits[13] * weight
        
        if self.current_board.whos_turn() == engine.PLAYER_B:
            return -val
        
        return val