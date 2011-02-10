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

# Population of 100, minimax search depth of 4 and 50% change of
# mutation. Mutants FTW

#population_size=20, mm_search_depth=4,  mutation_rate=0.01, 
#offspring_count=10, how_many_survive=10, player_class=basic.MiniMaxPlayer,
#initial_pop=1,tournament_size=6,

ea = evo.EvolutionaryAlgorithm(population_size=15, mm_search_depth=3, mutation_rate=0.5)
ea.verbose = True
ea.run(generations=100)