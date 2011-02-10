import random
from sys import maxint

from pycala import engine
from pycala.engine import board
from pycala.players.base import BasePlayer, BasePlayerManager

from pycala.engine import feature_detection

class HumanPlayer(BasePlayer):
    """ A Mancala player to enable human involvement. This player is 
    designed to be used via the command line. When creating an 
    alternative UI (i.e. web) an alternative player will be needed or 
    this player will need to be expanded to be more flexible.
    
    """
    
    name = "Human Player"
    objects = BasePlayerManager('HumanPlayer')
    
    def _get_move(self, b):
        """ Simple get move function that displays the the board on the 
        command line and the list of legal moves and requests the user 
        inputs one of them.
        
        """
        
        # Take a copy of the board to simulate moves on
        working_board = board.MancalaBoard(state=b)
        
        me = working_board.whos_turn()
        turn = []
        # while its still my turn on the working board collect moves
        while me == working_board.whos_turn():
            if len(turn) == 0:
                print working_board
            
            # let the user know why they are getting to play again
            if len(turn) > 0:
                print "You have another turn!" 
            
            if working_board.whos_turn() == engine.PLAYER_A:
                print "You can do the following moves: %s" % working_board.get_legal_moves()
            else:
                print "You can do the following moves: %s" % working_board.get_legal_moves()[::-1]
            move = int(raw_input("Select a move! "))
            print working_board.move(move, commit=True, override_checks=True)
            turn.append(move)
            
        return turn


class RandomPlayer(BasePlayer):
    """ Simple player that randomly selects a move from all the legals 
    moves. This is good for testing in two cases. It allows fast runs 
    through the board for testing all the game rules and it also 
    provides an entry level standard for AI players. If a player can't 
    been an random player then there isn't going to be much success.
    
    """
    
    name = "Random Player"
    objects = BasePlayerManager('RandomPlayer')
        
    def _get_move(self, board):
        # return a possible turn. These are a set of moves.
        return random.choice(board.get_possible_turns())


class MiniMaxPlayer(BasePlayer):
    
    name = "MiniMax Player"
    objects = BasePlayerManager('MiniMaxPlayer')
        
    required_weights = ['scrape', 'store', 'score', 'stance', 'pits_multi', ]
    required_settings = ['max_depth', ]
    
    def __init__(self, *args, **kwargs):
        
        super(MiniMaxPlayer, self).__init__(*args, **kwargs)
        
        self.node_count = 0
        self.end_game_count = 0
        
        self.nodes_at_depth = [0 for x in range(0,self.settings['max_depth']+1)]
        
    def _get_move(self, board):
        
        # start off the initial node and pass it into a recursive function
        self.search_tree = self.Node(board, self.board_eval, 0)
        self.nodes_at_depth[0] = 1
        self.node_count = 1
        
        # TODO: this needs to be altered so it returns the full move
        # rather than part of the move in a list.
        return self.find_best(self.search_tree)
    
    def find_best(self, current_node,):
        
        # for all the possible board outcomes loop through and make a 
        # new node in the tree
        for turn_moves in current_node.board.get_possible_turns():
            
            new_board = current_node.board.move(turn_moves)
            # create the new node
            new_node = self.Node(board=new_board, eval_func=self.board_eval, id=self.node_count, parent=current_node)
            
            if new_node.board.whos_turn() == self.player:
                new_node.value = maxint
            else:
                new_node.value = -maxint
                
            self.node_count += 1
            self.nodes_at_depth[new_node.depth] += 1
            
            if new_node.board.game_state == engine.GAME_FINISHED:
                self.end_game_count += 1
                new_node.evaluate(end_game=True)
            elif new_node.depth >= self.settings['max_depth']:
                new_node.evaluate(max_depth=True)
            else:
                self.find_best(new_node)
            
            # we have all the children for this node. the value of this 
            # node is based on that of the child nodes
            # TODO: following bit of code is suspect!
            if new_node.board.whos_turn() != self.player:
                # MAX - its 'my' turn
                for child in new_node.children:
                    if child.value > new_node.value:
                        new_node.value = child.value
            else:
                # MIN - its 'your' turn
                for child in new_node.children:
                    if child.value < new_node.value:
                        new_node.value = child.value
                
        
        # End of the root node, tree should be fully created now.
        if current_node.depth == 0:
            
            best_move = -1
            best_value = -maxint
            possibles = []
            
            for child in current_node.children:
                
                if child.value > best_value:
                    possibles = []
                    best_value = child.value
                    best_move = child.board.move_sequence
                    possibles.append(child.board.move_sequence)
                elif child.value == best_value:
                    possibles.append(child.board.move_sequence)
                    
            return random.choice(possibles)
    
    def board_eval(self, board):
        
        # initialise the value as 0
        value = 0.0
        
        evaluator = feature_detection.Detector(board)
        
        #return evaluator.store(1)
        
        #return evaluator.store(100)
        
        for key, weight in self.weights.items():
            
            if key.endswith('_multi'):
                key = key[:-6]
            f = getattr(evaluator, key)
            value += f(weight)
            #value += getattr(evaluator, key)(weight)
        
        return value
        
    class Node(object):
        
        def __init__(self, board, eval_func, id, parent=None):
            self.id = id
            self._board_eval = eval_func
            self.board = board
            self.parent = parent
            self.children = []
            self.depth = 0
            self.value = 0
            # Tell the parent we are its child! Feels like that 
            # instruction should be the other way somehow :)
            if parent != None:
                self.parent.add_child(self)
                self.depth = parent.depth + 1
        
        def add_child(self, child):
            self.children.append(child)
        
        def has_parent(self):
            return self.parent != None
        
        def evaluate(self, max_depth=False, end_game=True):
            
            self.value = self._board_eval(self.board)
            
            if self.depth%2:
                self.value = -self.value
                
            return self.value
        
        def __str__(self):
            return "ID:%s Depth:%s Children:%s Value:%s Move:%s" % (self.id,self.depth, len(self.children), self.value, self.board.move_sequence)


class MiniMaxPlayerExplorer(MiniMaxPlayer):
    
    name = "MiniMax Player Explorer"
    objects = BasePlayerManager('MiniMaxPlayerExplorer')
        
    required_weights = ['pit0', 'pit1', 'pit2', 'pit3', 'pit4', 'pit5', 'pit6', 
                        'pit7', 'pit8', 'pit9', 'pit10', 'pit11', 'pit12', 'pit13', ]


class MiniMaxPlayerSimple(MiniMaxPlayer):
    
    name = "MiniMax Player Simple"
    objects = BasePlayerManager('MiniMaxPlayerSimple')
        
    required_weights = ['store',]
    
class MiniMaxPlayerSimple2(MiniMaxPlayer):
    
    name = "MiniMax Player Simple 2"
    objects = BasePlayerManager('MiniMaxPlayerSimple2')
        
    required_weights = ['pit0','pit7',]