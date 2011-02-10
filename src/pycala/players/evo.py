import random
import time
import os

from pycala import engine
from pycala.engine import board
from pycala.engine import players
from pycala.engine import tournament

from pycala.players import basic
from pycala.util.exceptions import ImproperlyConfiguredError

class EvolutionaryAlgorithm(object):
    
    def __init__(self, population_size=20, mm_search_depth=4, 
                 mutation_rate=0.01, offspring_count=10, how_many_survive=10,
                 player_class=basic.MiniMaxPlayer,initial_pop=None,tournament_size=6,):
        self.population = []
        self.population_fitness = []
        self.MAX_POPULATION = population_size
        self.search_depth = mm_search_depth
        self.mutation_rate = mutation_rate
        self.generations = 0
        self.best = None
        self.settings = {}
        self.tournament_size = tournament_size
        
        self.player_class = player_class
        
        self.initial_pop = initial_pop
        self.offspring_count = offspring_count 
        self.how_many_survive = how_many_survive
        
        self.verbose = False
                
    def run(self, generations=0, seconds=0):
        """ Allows for 3 different methods of running the EA. By number
        of generations, seconds or until ctrl+c is pressed (a 
        KeyboardInterrupt exception).
        
        Passing in generations or seconds will start those modes other
        wise it will default to running until told to stop.
        
        """
        
        print "\n\nStarting EA"
        print "PID: %s" % os.getpid()
        if self.verbose: print "init_pop"
        self
        self.init_pop()
        
        sorted_pop = []
        
        try:
            
            if generations > 0:
                while self.generations < generations:
                    sorted_pop = self._run()
                    
            elif seconds > 0:
                start = time.time()
                while time.time() - start > seconds:
                    sorted_pop = self._run()
            
            else:
            
                sorted_pop = self._run()
                
        except KeyboardInterrupt, e:
            pass
        
        for cro in sorted_pop:
            print "NAME:", cro.name, 
            print "\tAGE: %03s" % cro.generations_survived, 
            print "\tWIN: %03s" % len(cro.won),
            print "\tLOOSE: %03s" % len(cro.lost),
            print "\tDRAW: %03s" % len(cro.drawn),
            print "\tDIFF: %04s" % (cro.for_points - cro.away_points),
            print "\tHW: %03s" % cro.home_won,
            print " HL: %03s" % cro.home_lost,
            print " AW: %03s" % cro.away_won,
            print " AL: %03s" % cro.away_lost
            print "\tWEIGHTS: ", cro.weights
            
    
    def _run(self):
        
        def force_breed(parent1, parent2, ea):
            recombination_operators = ['stitch', 'crossover', 'meet']
            mutation_operators = ['shift', 'swap', 'dither']
            children = []
            for recombination_operator in recombination_operators:
                children.append(ea.recombination(parent1, parent2, method=recombination_operator))
            mutants = []
            for child in children:
                for mutation_operator in mutation_operators:
                    mutants.append(ea.mutate(child, method=mutation_operator))
            for mutant in mutants:
                ea.reinsert_child(mutant)
        
        offspring_count = self.offspring_count
        how_many_survive = self.how_many_survive
        
        self.generations += 1
            
        if self.verbose: print "\n\nGeneration", self.generations, "\n"
        
        if len(self.population_fitness) > 0:
            if self.verbose: print "Plucking the 'best' parents and force breeding... ",
            parent1 = self.population_fitness[0]
            parent2 = self.population_fitness[1]
            force_breed(parent1, parent2, self)
            if self.verbose: print "ok\n"
        
        for i in xrange(offspring_count):
        
            if self.verbose:
                print "%02s" % i,
                print "Selection... ",
            parent1, parent2 = self.selection(tournament_count=self.tournament_size)
            
            if self.verbose: print "Recombination... ",
            child = self.recombination(parent1, parent2, 'stitch')
            
            if self.verbose: print "Mutation... ",
            mutant = self.mutate(child, method='shift', percentage=10,)
            
            if self.verbose: print "Re-insertion... ",
            self.reinsert_child(mutant, method="additional")
            
            if self.verbose: print "ok"
        
        if self.verbose: print "\nFitness Calculation ... "
        sorted_population = self.fitness()
        if self.verbose: print "ok"
        
        self.best = sorted_population[0]
        
        if self.verbose: print "Generation Top Players! ..."
        for cro in sorted_population[:20]:
            print "NAME:", cro.name, 
            print "\tAGE:", cro.generations_survived, 
            print "\tWIN:", len(cro.won),
            print "\tLOOSE:", len(cro.lost),
            print "\tDRAW:", len(cro.drawn),
            print "\tDIFF:", cro.for_points - cro.away_points,
            print "\tHW: %03s" % cro.home_won,
            print " HL: %03s" % cro.home_lost,
            print " AW: %03s" % cro.away_won,
            print " AL: %03s" % cro.away_lost
            print "WEIGHTS: ", cro.weights
        
        if self.verbose: 
            print "\n\nCurrent Best ...\n"
            print "NAME:", self.best.name, 
            print "\tAGE:", self.best.generations_survived,
            print "\tWIN:", len(self.best.won),
            print "\tLOOSE:", len(self.best.lost),
            print "\tDRAW:", len(self.best.drawn),
            print "\tDIFF:", self.best.for_points - self.best.away_points
            print "\tWEIGHTS: ", self.best.weights
            
        if self.verbose: print "Generation progressment ...",
        self.init_pop(initial=sorted_population[:how_many_survive])
        if self.verbose: print "ok\n\n"
        
        return sorted_population
            
    def init_pop(self, initial=None):
        
        if self.generations == 0:
            initial = self.initial_pop
        
        settings={'max_depth':self.search_depth,}
        
        if initial == None:
            initial = []
            
        self.population = initial[:]
        
        for cro in initial:
            cro.generations_survived += 1
        
        count = self.MAX_POPULATION - len(initial)
        for i in xrange(0,count):
            cro = self.player_class.objects.random(settings=settings, name="MM %s %s" % (self.generations, i))
            self.population.append(cro)
        
        return self.population
        
    def selection(self, tournament_count=0):
        
        if tournament_count > self.MAX_POPULATION:
            raise ImproperlyConfiguredError, "Tournament size is bigger than population"
        
        def get_random(count):
            play_off = []
            for i in xrange(0,count):
                selected = random.choice(self.population)
                while selected in play_off:
                    selected = random.choice(self.population)
                play_off.append(selected)
            return play_off
        
        if tournament_count <= 2:
            play_off = get_random(2)
            return play_off[0],play_off[1]
        
        if tournament_count == self.MAX_POPULATION:
            play_off = self.population[:]
        else:
            play_off = get_random(tournament_count)
        
        mt = tournament.MancalaTournament(play_off)
        mt.run()
        
        return mt.score_board()[:2]
        
    def recombination(self, parent1, parent2, method='stitch', parents_can_survive=False):
        
        def stitch(parent1, parent2):
            #  a b c d e f g
            #  A B C D E F G
            # =a B c D e F g 
            weight_keys = parent1.weights.keys()
            length = len(weight_keys)
            childa = engine.players.ConfiguredPlayer(parent1.player_class, settings=parent1.settings, skip_validation=True,)
            childb = engine.players.ConfiguredPlayer(parent1.player_class, settings=parent2.settings, skip_validation=True,)
            
            for i in xrange(0, length):
                weight_name = weight_keys[i]
                p1_weight = parent1.weights[weight_name]
                p2_weight = parent2.weights[weight_name]
                if bool(i%2):
                    childa.weights[weight_name] = p1_weight
                    childb.weights[weight_name] = p2_weight
                else:
                    childa.weights[weight_name] = p2_weight
                    childb.weights[weight_name] = p1_weight
            
            play_off = [childa, childb,]
            if parents_can_survive:
                play_off = [childa, childb, parent1, parent2,]
            
            
            mt = tournament.MancalaTournament(play_off)
            return mt.winner()
            
        def crossover(parent1, parent2):
            #  a b c d e f g
            #  A B C D E F G
            # =a b c D E F G 
            weight_keys = parent1.weights.keys()
            length = len(weight_keys)
            
            childa = engine.players.ConfiguredPlayer(parent1.player_class, settings=parent1.settings, skip_validation=True,)
            childb = engine.players.ConfiguredPlayer(parent1.player_class, settings=parent2.settings, skip_validation=True,)
            
            for i in xrange(0, length):
                weight_name = weight_keys[i]
                p1_weight = parent1.weights[weight_name]
                p2_weight = parent2.weights[weight_name]
                if i <= (length/2):
                    childa.weights[weight_name] = p1_weight
                    childb.weights[weight_name] = p2_weight
                else:
                    childa.weights[weight_name] = p2_weight
                    childb.weights[weight_name] = p1_weight
            
            play_off = [childa, childb,]
            if parents_can_survive:
                play_off = [childa, childb, parent1, parent2,]
                
            mt = tournament.MancalaTournament(play_off)
            mt.run()
            return mt.winner()
        
        def meet(parent1, parent2):
            #  8 6 2 4 8 0 9
            #  2 6 6 4 0 4 7
            # =6 6 4 4 4 2 8 
            weight_keys = parent1.weights.keys()
            length = len(weight_keys)
            child = engine.players.ConfiguredPlayer(parent1.player_class, settings=parent1.settings, skip_validation=True,)
            
            for i in xrange(0, length):
                weight_name = weight_keys[i]
                p1_weight = parent1.weights[weight_name]
                p2_weight = parent2.weights[weight_name]
                if not weight_name.endswith('_multi'):
                    meet_val = (p1_weight + p2_weight)/2
                    child.weights[weight_name] = meet_val
                else:
                    new_multi = []
                    
                    for j in xrange(0, len(p1_weight) ):
                        new_multi.append( (p1_weight[j] + p2_weight[j])/2 )
                        
                    child.weights[weight_name] = new_multi
            
            if parents_can_survive:
                play_off = [child, parent1,parent2,]
                mt = tournament.MancalaTournament(play_off)
                mt.run()
                return mt.winner()
            else:
                return child
        
        recombination_methods = {'stitch':stitch,  'meet':meet, 'crossover':crossover,}
        
        child = recombination_methods[method](parent1, parent2)
        child.name = "CC %s %s" % (self.generations, len(self.population))
        return child
        
    def mutate(self, child, method='shift', percentage=1,):
        
        child = child.copy()
        
        def shift(child):
            weights = list(child.weights)
            for weight in weights:    
                if random.random() < self.mutation_rate:
                    if not weight.endswith('_multi'):
                        dither_val = (1.0*child.weights[weight]/100)*percentage
                        change = random.uniform(-dither_val,dither_val)
                        child.weights[weight] += change
                    else:
                        new_multi = []
                        for sub_weight in child.weights[weight]:
                            dither_val = (1.0*sub_weight/100)*percentage
                            change = random.uniform(-dither_val,dither_val)
                            new_multi.append(sub_weight+change)
                        child.weights[weight] = new_multi
            return child
        
        def swap(child):
            if random.random() < self.mutation_rate:
                
                # For simplicity sake, we cannot swap multi-weight weights.
                # Basically, as there is only certain places they will
                # fit in. 
                weights = filter(lambda i:not i.endswith('_multi'), child.weights.keys())
                
                # Check we have enough to swap
                if len(weights) < 2:
                    raise Exception, "Cannot Swap weights if there are less than two"
                
                # Randomly select two weights and make sure they are different
                w1 = w2 = random.choice(weights)
                while w1 == w2:
                    w2 = random.choice(weights)
                
                # swap!
                tmp = child.weights[w1]
                child.weights[w1] = child.weights[w2]
                child.weights[w2] = tmp
            return child
        
        def dither(child):
            if random.random() < self.mutation_rate:
                child.weight_dither(percentage=percentage)
            return child
        
        mutation_methods = {'shift':shift, 'swap':swap, 'dither':dither, }
        
        return mutation_methods[method](child)
    
    def reinsert_child(self, child, method="additional"):
        
        def random_insert(child):
            place = random.randint(0, self.MAX_POPULATION-1)
            self.population[place] = child
        
        def additional(child):
            self.population.append(child)
        
        reinsertation_methods = {'random':random_insert, 'additional':additional, }
        
        return reinsertation_methods[method](child)
    
    def fitness(self):
        
        for cro in self.population:
            cro.won = []
            cro.lost = []
            cro.drawn = []
        
        print "Population is: %s " % len(self.population)
        
        mt = tournament.MancalaTournament(self.population)
        mt.run()
        sb =  mt.score_board(method='difference', second='football')
        self.population_fitness = sb
        return sb

class ControlGroup(EvolutionaryAlgorithm):
    
    def __init__(self, control_group, *args, **kwargs):
        
        self.control_group = control_group
        
        super(ControlGroup, self).__init__(*args, **kwargs)
    
    def _fitness_home(self, cro, cg):
            home = board.MancalaGame(cro, cg)
            home.run_game()
            cro_score, cg_score = home.board.scores()
            cro.for_points += cro_score
            cro.away_points += cg_score
            
            if cro_score > cg_score:
                cro.won.append(cg)
                cro.home_won += 1
            elif cg_score > cro_score:
                cro.lost.append(cg)
                cro.home_lost += 1
            else:
                cro.drawn.append(cg)
    
    def _fitness_away(self, cro, cg):
            away = board.MancalaGame(cg, cro)
            away.run_game()
            cg_score, cro_score = away.board.scores()
            cro.for_points += cro_score
            cro.away_points += cg_score
            
            if cro_score > cg_score:
                cro.won.append(cg)
                cro.away_won += 1
            elif cg_score > cro_score:
                cro.lost.append(cg)
                cro.away_lost += 1
            else:
                cro.drawn.append(cg)
                
    def fitness(self):
        
        c = len(self.population)
        
        print "Population is: %s " % c
        
        for cro in self.population:
            
            cro.won = []
            cro.lost = []
            cro.drawn = []
            cro.for_points = 0
            cro.away_points = 0
            cro.home_won = 0
            cro.home_lost = 0
            cro.away_won = 0
            cro.away_lost = 0
            
            for cg in self.control_group:
                
                self._fitness_home(cro, cg)
                self._fitness_away(cro, cg)

            
            w = len(cro.won)
            d = len(cro.drawn)
            l = len(cro.lost)
            print "%03s: %s \tWon %03s, Drawn %03s, Lost %03s" % (c,cro.name,w,d,l)
            c -= 1
        
        sorted_pop = self.sort_pop_by_fitness(method='difference', second='football')
        
        self.population_fitness = sorted_pop
        return sorted_pop
        
    
    def sort_pop_by_fitness(self, method='difference', second=None):
        
        def score(obj):
            return obj.points(method=method)
        
        def second_sort(obj):
            return obj.points(method=second)
        
        s = sorted(self.population, key=score, reverse=True)
        
        if second:
            return sorted(s, key=second_sort, reverse=True)
        
        return s

class ControlGroupHome(ControlGroup):
    
    def _fitness_away(self, x, y):
        # override away with a blank function as we don't care about it
        pass

class ControlGroupAway(ControlGroup):

    def _fitness_home(self, x, y):
        # override home with a blank function as we don't care about it
        pass
    
class EvolutionaryAlgorithm2(ControlGroup):
    """
    This is here for legacy reasons. Basically acts as a shortcut to the
    control group and thus means the implementations don't need to be 
    changed through the code but the new name that makes more sense can 
    be used.
    
    """