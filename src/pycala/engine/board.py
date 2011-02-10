import sys

from pycala.util.exceptions import InvalidMoveError, TurnNotFinishedError
from pycala import engine

class MancalaBoard(object):
    """ Board class representing the Mancala boards current state and 
    enforcing all of the game users. A number of useful functions are 
    also included to make writing players easier. Where they can 
    request a list of all the valid moves etc.
    
    """
    
    def __init__(self, state=None, stones=4):
        """Either copies a MancalaBoard or creates a fresh instance
        
        Keyword arguments:
        state -- optional, instance of MancalaBoard to be copied
                 or nothing to make a fresh new instance.
	stones -- The number of stones or seeds to start the board with
		ignored if a state is passed in.
        
        """
        if state is not None:
            # copy state, pits and player_turn
            self.game_state = state.game_state
            self.game_result = state.game_result
            self.pits = state.pits[:]
            self.players_turn = state.players_turn
            self.move_sequence = state.move_sequence[:]
            self.game_history = state.game_history[:]
            self.stones = state.stones
        else:
            self.initial_board(stones)
            self.game_state = engine.GAME_RUNNING
            self.game_result = engine.GAME_UNKNOWN
            self.set_turn(engine.PLAYER_A) #default to player A
            self.move_sequence = []
            self.game_history = []
            self.stones = stones
    
    def initial_board(self,stones):
        """ Sets the initial game board. 4 stones in each pit except 
        home pits have 0
        
        """
        self.pits = [stones for x in range(0,14)] # Place 4 pieces in all pits
        self.pits[engine.HOME_A] = 0   # Empty A's home pit
        self.pits[engine.HOME_B] = 0   # Empty B's home pit
    
    def set_turn(self, player):
        """ Sets the players turn based on the passed in player """
        self.players_turn = player
        self.move_sequence = []
    
    def end(self):
        """ End the game and display results """
        a, b = self.scores()
        
        self.game_state = engine.GAME_FINISHED
        
        if a > b:
            self.game_result = engine.GAME_WON_A
        elif b > a:
            self.game_result = engine.GAME_WON_B
        else:
            self.game_result = engine.GAME_DRAW
    
    def display_score(self):
        return "Player A: %s    Player B: %s" % self.scores()
    
    def winner(self):
        """  Returns winner or raises an exception stating the game 
        isn't finished.
        
        """
        if self.game_state == engine.GAME_WON_A:
            return engine.PLAYER_A
        elif self.game_state == engine.GAME_WON_B:
            return engine.PLAYER_B
        else:
            raise Exception, "Game isn't finished!"
    
    def whos_turn(self):
        """ Returns the player to play next """
        return self.players_turn
    
    def is_legal_move(self, pit_id):
        """ Steps through a number of game rules to check that the 
        requested move is legal raises InvalidMoveError exception if 
        there is a problem, otherwise returns True
        
        """
        
        # Check the pit actually exists
        if pit_id > (len(self.pits)-1) or pit_id < 0:
            raise InvalidMoveError, "Pit %s doesn't exist" % (pit_id)
        
        # Check we are not trying to move from the home pit
        if pit_id == engine.HOME_A or pit_id == engine.HOME_B:
            raise InvalidMoveError, "Can't move stones from home pit - %s" % (pit_id)
        
        # Check the pit we are trying to move from has stones
        if self.pits[pit_id] <= 0:
            raise InvalidMoveError, "Pit has no stones to move - %s" % (pit_id)
        
        # Check the pit belongs to the player
        if not self.pit_belongs_to(pit_id, self.whos_turn()):
            raise InvalidMoveError, "Pit doesn't belong to player - pit:%s player:%s" % (pit_id, self.whos_turn())
        
        # Assume everything is OK, all tests passed
        return True
    
    def get_legal_moves(self):
        """ Returns a list of the pits with 1 or more stones in them 
        that also belong to the player. Or in other words, the legal 
        moves available.
        
        """
        
        legal_moves = []
        if self.whos_turn() is engine.PLAYER_A:
            possible_moves = engine.PITS_A[:]
        else:
            possible_moves = engine.PITS_B[:]
        
        for i in possible_moves:
            if self.pits[i] > 0:
                legal_moves.append(i)
                
        return legal_moves
    
    def get_possible_turns(self):
        """ Each turn can be comprised of more than one move. If a 
        player ends in their home pit they get another turn. This method
        follows through and generator for all the possible moves.
        
        """
        
        def follow_moves(current_board):
            """ Recursive function. Finds all the legal moves and if its
            still the current players turn continue to follow until its
            the end of their turn.
            
            """
            
            boards_list = []
            
            for move in current_board.get_legal_moves():
                turn = [move,]
                # get after-move board
                new_board = current_board.move(move, override_checks=True)
                
                if new_board.whos_turn() == current_board.whos_turn():
                    # still same players turn so check all the moves
                    # get the sub turns
                    subturns = list(follow_moves(new_board))
                    
                    # if we have no moves after landing in the home then
                    # we are done. this happens for example on the last
                    # turn.
                    if len(subturns) == 0:
                        yield turn
                    
                    # loop through possible moves
                    for subturn in subturns:
                        yield turn + subturn
                    
                        
                else:
                    # other players turn so end of turn, save board
                    boards_list.append(new_board)
                    yield turn
                

        result = list(follow_moves(self))
        return result
        
    def scores(self):
        """ Adds up the current game and returns them as a tuple 
        (A_SCORE, B_SCORE).
        
        """
        return sum(self.pits[0:7]), sum(self.pits[7:14]),
    
    def opposite_pit(self, pit_id):
        """ Simple function to calculate the opposite side of the board.
        Useful if the board representation is changed.
        
        """
        
        if pit_id == 6:
            return 13
        if pit_id == 13:
            return 6
        return 12 - pit_id
    
    def move_end(self, pit_id):
        """ Calculate what pit a particular move will end in """
        self.is_legal_move(pit_id)  # Check its legal
        stones = self.pits[pit_id]  # How many stones do we have to move?
        while stones > 0:
            pit_id += 1     # Move to next pit
            if pit_id > 13: # Check we are not at the end
                pit_id = 0
            stones -= 1 
        return pit_id
    
    def pit_belongs_to(self, pit_id, player):
        """ returns True if the given pit belongs to the given player. 
        Otherwise False is returned. 'Belong to' basically means on that
        players side of the board.
        
        """
        
        # Check the pit belongs to the player
        if player is engine.PLAYER_A:
            if pit_id < 0 or pit_id > 6:
                return False
        elif player is engine.PLAYER_B:
            if pit_id < 7 or pit_id > 13:
                return False
        
        # Assume all is A-OK
        return True
    
    def move(self, pits, commit=False, override_checks=False):
        """ Makes a move on the board. If commit is set to False a copy
        of the board is returned rather than modifying the current
        board. If commit is set to True, the current board is updated
        and an exception is raised if a complete turn isn't made. i.e.
        if the player makes a move that ends in their home pit they get
        another move, thus not finishing the turn and an exception is
        raised.
        
        """
        
        if commit:
            working_board = self
        else:
            working_board = MancalaBoard(self)
        
        starting_turn = self.whos_turn()
        
        current_turn = starting_turn
        
        if pits.__class__ == list:
            
            for pit in pits:
                
                if current_turn != starting_turn and not override_checks:
                    raise TurnNotFinishedError, "Sequence has to many moves - no longer players turn"
                
                working_board = working_board._move(pit, commit)
                current_turn = working_board.whos_turn()
                
            working_board.move_sequence = pits
            self.game_history.append(MancalaBoard(working_board))
            
            if working_board.whos_turn() == starting_turn and not override_checks and working_board.can_play():
                raise TurnNotFinishedError, "Given moves didn't finish turn"
            
        else:
            
            working_board = working_board._move(pits, commit)
            if working_board.whos_turn() == starting_turn and not override_checks:
                raise TurnNotFinishedError, "Given moves didn't finish turn"
            working_board.move_sequence = [pits,]
            self.game_history.append(MancalaBoard(working_board))
            
        return working_board
    
    def can_play(self):
        player = self.whos_turn()
        if player:
            to_count = engine.PITS_A
        else:
            to_count = engine.PITS_B
            
        return sum(self.pits[min(to_count):max(to_count)]) > 0
        
    def _move(self, pit_id, commit = False):
        """ Performs the move on the board for the given pit.
        If commit is False a copy of the board is made and returned 
        rather than this instance.
        
        """
        
        if commit is False:
            new_board = MancalaBoard(self)
            return new_board.move(pit_id, commit=True, override_checks=True)
        
        if self.game_state == engine.GAME_STARTED:
            raise InvalidMoveError, "Game not started"
        if self.game_state == engine.GAME_FINISHED:
            raise InvalidMoveError, "Game Finished"
        
        self.is_legal_move(pit_id) # Check the move is legal
        
        self.last_move = pit_id
        self.last_move_pit_count = self.pits[pit_id]
        self.last_move_board_state = self.pits[:]
        
        stones = self.pits[pit_id] # 'Pick up' stones
        self.pits[pit_id] = 0
        
        # While we still one or more stones 'in hand' lets move them one by one
        while stones > 0:
            
            pit_id += 1     # move to next pit
            
            # If Player A skip B's home, if A's home skip B's home
            if (self.whos_turn() is engine.PLAYER_A and pit_id is engine.HOME_B) \
                or (self.whos_turn() is engine.PLAYER_B and pit_id is engine.HOME_A):
                pit_id += 1
                
            if pit_id == 14: # check we are not past the end
                pit_id = 0
            elif pit_id > 14:
                raise Exception, "Past the end of the board?"
            
            """
            If the last stone to be placed ends in an empty pit that 
            belongs to the current player. Then they capture that stone 
            and all the stones on the opposite side of the board.
            """
            if stones == 1 and self.pits[pit_id] == 0 \
                    and pit_id != engine.HOME_A and pit_id != engine.HOME_B \
                    and self.pit_belongs_to(pit_id, self.whos_turn()) \
                    and self.pits[self.opposite_pit(pit_id)] > 0:
                
                # pick up opposite pits stones
                hand = self.pits[self.opposite_pit(pit_id)]
                self.pits[self.opposite_pit(pit_id)] = 0
                
                # add the sum of the opposite to players home pit
                # the final stone is also captured
                if self.whos_turn() is engine.PLAYER_A:
                    self.pits[engine.HOME_A] += hand 
                    self.pits[engine.HOME_A] += 1 
                else:
                    self.pits[engine.HOME_B] += hand
                    self.pits[engine.HOME_B] += 1
                
                stones = 0
            else:
                # We have not ended on a special case to drop a stone in the current pit
                self.pits[pit_id] += 1
                stones -= 1
                
        """
        Check to see we have not finished in the players home pit.
        if we have the turn shouldn't be swapped to the other player as
        they are allowed to play again.
        """
        if (self.whos_turn() is engine.PLAYER_A and pit_id is not engine.HOME_A) \
            or (self.whos_turn() is engine.PLAYER_B and pit_id is not engine.HOME_B):
            self.set_turn(not self.whos_turn())
        
        """
        Check for an end game clause where one of the players can no 
        longer make a move. i.e. they have no stones left.
        
        TODO: This needs to take into account that the next players move
        *may* send stones to their side of the board and thus they 
        could still play.
              -- Actually, I think this is right.
        """
        if sum(self.pits[0:6]) <= 0 or sum(self.pits[7:13]) <=0:
            self.end()
        
        # So there is a common interface between copying a board and 
        # commiting the move to this board
        return self
        
        """
        No board evaluation function was provided so use a very basic eval
        """
        a,b = self.scores()
        value = a - b
        if self.whos_turn() is engine.PLAYER_A:
            return value
        else:
            return -value
        
    def __str__(self):
        """ String replresentation of the board designd to be seen on 
        the command line.
        
        Code is pretty hacky/messy but its useful to have an easy way of
        representing the mancala game board.
        
        """
        
        i = self.pits
        return """
                    PLAYER B (FALSE)
.----------------------------------------------.
| .----. .--. .--. .--. .--. .--. .--. .----.  |
| |    | |%02s| |%02s| |%02s| |%02s| |%02s| |%02s| |    |  |
| | %02s | '--' '--' '--' '--' '--' '--' | %02s |  |
| |    | .--. .--. .--. .--. .--. .--. |    |  |
| |    | |%02s| |%02s| |%02s| |%02s| |%02s| |%02s| |    |  |
| '----' '--' '--' '--' '--' '--' '--' '----'  |
'----------------------------------------------'
                    PLAYER A (TRUE)
        """ % (i[12], i[11], i[10], i[9], i[8], i[7], i[13], i[6], i[0], i[1], i[2], i[3], i[4], i[5])

class MancalaGame(object):
    
    def __init__(self, p_a, p_b, board=None, verbose=False):
        """ Confusing lines to read...
        Creates a new instance of the class chosen for player_a and 
        player_b while passing in either PLAYER_A or PLAYER_B so the 
        class knows what player it is.
        
        """
        self.conf_player_a = p_a
        self.conf_player_b = p_b
        self.player_a = p_a.create(engine.PLAYER_A)
        self.player_b = p_b.create(engine.PLAYER_B)
        self.verbose = verbose
        
        # if we are passed in a board, use it. Otherwise, make a new one.
        if board is not None:
            self.board = board
        else:
            self.board = MancalaBoard()
    
    def run_game(self):
        """ Runs through the game for the two given players. If verbose 
        is set to False then the moves are printed out on the screen.
        
        """
        while self.board.game_state == engine.GAME_RUNNING:
            
            #try:
                
            if self.board.whos_turn() is engine.PLAYER_A:
                player_to_go = self.player_a
            else:
                player_to_go = self.player_b
            
            move = player_to_go.get_move(self.board)
            if self.verbose:
                print "%s moves: %s" % (player_to_go.name, move)
            self.board.move(move, commit=True)
                        
            #except InvalidMoveError, ime:
            #    print ime

class BoardSerializer(object):
    """ Board seralizing class. Used to encode and decode the board
    into various different formats.
    
    """
    
    
    def _reverse(self, pits):
        """ Reverse the board so player B's pits become player A's and
        vice versa. Since its a zerosum game with a symmetrical board
        this allows us to half the states we need to record.
        
        """
        return pits[7:14] + pits[0:7]
    
    def _int_to_bin(self, int):
        """ Convert an integer into a binary string
        i.e. 10 = 00001010
        
        """
        return "".join([str((int >> y) & 1) for y in range(8-1, -1, -1)])
    
    def _bin_to_int(self, binary):
        """ Convert a binary string into an integer
        i.e. 00001010 = 10
        
        """
        return int(binary, 2)
    
    def as_binary(self, board):
        """ Convert a board state (the pits) into a binary string
        
        """
        pits = board.pits[:]
        
        #if board.whos_turn() == engine.PLAYER_B:
        #    pits = self._reverse(pits)
        
        return "".join([self._int_to_bin(i) for i in pits])
    
    def from_binary(self, binary):
        """ Create a board based on a binary representation of its state
        
        """
        def _actual_from_binary(binary):
            step = 0
            
            while step < len(binary):
                yield self._bin_to_int(binary[step:step+8])
                step += 8
        
        new_board = MancalaBoard()
        new_board.pits = list(_actual_from_binary(binary))[:]
        
        return new_board
