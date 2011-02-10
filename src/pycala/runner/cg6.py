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


from pycala.players import evo
from pycala.players import basic
from pycala.engine.players import ConfiguredPlayer

from pycala.players.control import GROUP

ea_settings = {
    'control_group':GROUP,
    'population_size':10,
    'mm_search_depth':3,
    'mutation_rate':0.5,
    'offspring_count':10,
    'how_many_survive':5, 
    'player_class':basic.MiniMaxPlayerSimple2,
    'initial_pop':None,
    'tournament_size':3,
}

ea = evo.EvolutionaryAlgorithm2(**ea_settings)
ea.verbose = True
ea.run(generations=100)
