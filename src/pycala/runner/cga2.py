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
    'population_size':5,
    'mm_search_depth':3,
    'mutation_rate':0.9,
    'offspring_count':5,
    'how_many_survive':5, 
    'player_class':basic.MiniMaxPlayerExplorer,
    'initial_pop':None,
    'tournament_size':2,
}

ea = evo.ControlGroupAway(**ea_settings)
ea.verbose = True
ea.run(generations=400)
