from pycala.util.tests import PycalaTestCase

from pycala.players import evo

class Evolutionary(PycalaTestCase):
    
    def setUp(self):
        super(Evolutionary, self).setUp()
        # effectively make mutation 100% of the time so we can test it
        self.ea = ea = evo.EvolutionaryAlgorithm(population_size=10, mm_search_depth=2, mutation_rate=1,)
    
    def test_popinit(self):
        """ EA population initialisation. Simple check, makes a 
        population and checks the size is right.
        
        """
        
        self.ea.init_pop()
        
        # Check the population is the same as the max_length
        # each chromozone is validated when its created so that
        # should be A-OK
        self.assertEqual(len(self.ea.population), self.ea.MAX_POPULATION)
    
    def test_selection_random(self):
        """ EA Random selection. Randomly selects two parents, makes
        sure they are not the same.
        
        """
        
        self.ea.init_pop()
        
        p1, p2 = self.ea.selection()
        self.assertEqual(p1 in self.ea.population, True)
        self.assertEqual(p2 in self.ea.population, True)
        self.assertNotEqual(p1, p2)
    
    def test_selection_tournament(self):
        """ EA tournament selection. Randomly selects parents and holds
        a playoff to see what parent is the best.
        
        """
        
        self.ea.init_pop()
        
        p3, p4 = self.ea.selection(tournament_count=3)
        self.assertEqual(p3 in self.ea.population, True)
        self.assertEqual(p4 in self.ea.population, True)
        self.assertNotEqual(p3, p4)
        
        p5, p6 = self.ea.selection(tournament_count=4)
        self.assertEqual(p5 in self.ea.population, True)
        self.assertEqual(p6 in self.ea.population, True)
        self.assertNotEqual(p5, p6)
        
    def test_recombnination_stitch(self):
        """ EA Recombination stitch. Test the stitch method of 
        recombination. could be expanded to do a more thorough test.
        
        """
        
        self.ea.init_pop()
        p1, p2 = self.ea.selection()
        
        child1 = self.ea.recombination(p1, p2, method='stitch')
        self.assertNotEqual(child1.weights, p1.weights)
        self.assertNotEqual(child1.weights, p2.weights)
        
    def test_recombnination_crossover(self):
        """ EA Recombination crossover. Test the crossover method of 
        recombination. could be expanded to do a more thorough test.
        
        """
        
        self.ea.init_pop()
        p1, p2 = self.ea.selection()
        
        child2 = self.ea.recombination(p1, p2, method='crossover')
        self.assertNotEqual(child2.weights, p1.weights)
        self.assertNotEqual(child2.weights, p2.weights)
        
    def test_recombnination_meet(self):
        """ EA Recombination meet. Test the meet method of 
        recombination. could be expanded to do a more thorough test.
        
        """
        
        self.ea.init_pop()
        p1, p2 = self.ea.selection()
        
        child3 = self.ea.recombination(p1, p2, method='meet')
        self.assertNotEqual(child3.weights, p1.weights)
        self.assertNotEqual(child3.weights, p2.weights)
    
    def test_mutation_shift(self):
        """ EA Mutation shift. Test the shift method of recombination. 
        could be expanded to do a more thorough test.
        
        """
        
        self.ea.init_pop()
        p1, p2 = self.ea.selection()
        child = self.ea.recombination(p1, p2)
        
        mutant = self.ea.mutate(child, method='shift')
        self.assertNotEqual(child.weights, mutant.weights)
    
    def test_mutation_swap(self):
        """ EA Mutation swap. Test the swap method of recombination. 
        could be expanded to do a more thorough test.
        
        """
        
        self.ea.init_pop()
        p1, p2 = self.ea.selection()
        child = self.ea.recombination(p1, p2)
        
        mutant = self.ea.mutate(child, method='swap')
        self.assertNotEqual(child.weights, mutant.weights)
    
    def test_mutation_dither(self):
        """ EA Mutation dither. Test the dither method of recombination. 
        could be expanded to do a more thorough test.
        
        """
        
        self.ea.init_pop()
        p1, p2 = self.ea.selection()
        child = self.ea.recombination(p1, p2)
        
        mutant = self.ea.mutate(child, method='dither')
        self.assertNotEqual(child.weights, mutant.weights)
    
    def test_reinsert_child(self):
        """ EA reinsertation. Test the reinsertation of a child into
        the EA population.
        
        """
        
        self.ea.init_pop()
        for i in xrange(0,20):
            self.ea.reinsert_child(None)
        
    def test_fitness(self):
        """ EA fitness. Test calculation of fitness.
        
        """
        
        self.ea.init_pop()
        self.ea.fitness()