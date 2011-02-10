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

# Population of 100, minimax search depth of 4 and 50% change of
# mutation. Mutants FTW

#population_size=20, mm_search_depth=4,  mutation_rate=0.01, 
#offspring_count=10, how_many_survive=10, player_class=basic.MiniMaxPlayer,
#initial_pop=1,tournament_size=6,

ea_settings = {
    'population_size':4,
    'mm_search_depth':5,
    'mutation_rate':0.5,
    'offspring_count':5,
    'how_many_survive':1, 
    'player_class':basic.MiniMaxPlayerSimple,
    'initial_pop':None,
    'tournament_size':2,
}

ea = evo.EvolutionaryAlgorithm(**ea_settings)
ea.verbose = True
ea.run(generations=100)