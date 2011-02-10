import random
from sys import maxint

from pycala import engine
from pycala.engine import board
from pycala.players.base import BasePlayer, BasePlayerManager
from pycala.players.nn.models import Neuron

from pycala.engine import feature_detection

class NeuralNetPlayer(BasePlayer):
    """ 
    
    """
    
    name = "Neural Net Player"
    
    def __init__(self, *args, **kwargs):
        
        self.deviate_rate = -1
        
        super(NeuralNetPlayer, self).__init__(*args, **kwargs)
    
    def _get_move(self, working_board):
        
        #return random.choice(working_board.get_possible_turns())
        
        # get all the possible moves
        possible = working_board.get_possible_turns()
        # get all child boards for the possible moves
        child_boards = [working_board.move(p) for p in possible]
        
        # for each of the child boards turn into the binary
        # representation for searching the net.
        serializer = board.BoardSerializer()
        binary_boards = [serializer.as_binary(c) for c in child_boards]
        
        # search for neurons with an exact match
        # TODO: add methods for finding similar neurons
        neurons = [Neuron.objects.get_or_create(binary=b)[0] for b in binary_boards]
        #neurons = Neuron.objects.filter(binary__in=binary_boards)
        neurons = list(neurons)
        # if the random value is less than the deviate_rate then don't
        # select the best, just move on and we'll random select from them all
        if self.deviate_rate < random.random():
            
            # find the highest scoring neuron
            max = -maxint
            for neuron in neurons:
                if neuron.probability > max:
                    max = neuron.probability
            
            # filter the neurons to keep only the top scorers
            neurons = filter(lambda n: n.probability >= max, neurons)
                    
        if False:
            max = -maxint
            for neuron in neurons:
                if neuron.percent_won() > max:
                    max = neuron.percent_won()
            
            # filter the neurons to keep only the top scorers
            neurons = filter(lambda n: n.percent_won() >= max, neurons)
        
        # select randomly from the best, this may often be 1.
        chosen = random.choice(neurons)
        
        # convert binary representation back into the list 
        # representation of pits
        tmp_board = serializer.from_binary(chosen.binary)
        
        # find the child board that matches these pits and return the 
        # last move it made.
        for child_board in child_boards:
            if child_board.pits == tmp_board.pits:
                return child_board.move_sequence