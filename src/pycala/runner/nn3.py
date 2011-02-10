# Not very cool, but disables a warning caused by the MySQLdb module.
import warnings
warnings.filterwarnings("ignore")

import sys

class Unbuffered:
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)
    
sys.stdout=Unbuffered(sys.stdout)

from pycala import engine
from pycala.engine import board
from pycala.engine import players
from pycala.players import basic
from pycala.players.nn.engine import NeuralNetworkBoth
from pycala.players.nn.player import NeuralNetPlayer
from pycala.players.nn.models import Neuron, Log


from pycala.players.control import GROUP

def main():
    nn = NeuralNetworkBoth()
    
    nn.train(GROUP, repeat=1)
    
    del nn

if __name__ == '__main__':
    
    #import cProfile
    #from guppy import hpy
    
    for i in xrange(1):
        main()
        #cProfile.run( 'main()', filename="engine.profile" )
        
        #hp=hpy()
        #r = hp.heap()
        #print r[0].__class__
        #print dir(r[0])
        #print r[:5]
        
