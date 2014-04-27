""" 
About 
=====

Hey, this is a program to calculate the minimum of any given real
function(well, there's a catch =|) through a GA (Genetic Algorithm) approach.

License 
=======

https://www.tldrlegal.com/l/gpl2

You may copy, distribute and modify the software as long as you track 
changes/dates of in source files and keep all modifications under GPL. 
You can distribute your application using a GPL library commercially, 
but you must also disclose the source code.

Prerequisites
=============

I recommend using *ipython* as your console, and start it with the --pylab
command line argument. But if you don't like it, all that is required in order 
to run this is *numpy* and *BitStream*. They are fairly well known libraries 
and you probably already have them.

Usage 
=====

First, you should probably instantiate a new Environment(). It starts with a
predefined target function that you can just run to get the feeling of how 
things work.

    Example:

    e = Environment()

    e.fast_foward()

Details 
=======

I tried to keep the code clean and simple with a lot of one-liners so it
wouldn't be so daunting to read like other similar codes. The basic idea
is this:

    1.  First create a random population. 

    2.  Select another population of the same size but through a roulette 
        method. 

        2.1 The roulette method tries to compute something I called 
            *population fitness* which is just the sum of the fitness of the 
            entire population. Then the probability of selecting any 
            individual in the roulette is given by it's fitness divided by the
            population fitness. If the target function is such that it's 
            maximum value is higher than 4000 you should set the environment 
            normalizing factor that is used to get over the problem of 
            calculating proportions between positive and negative numbers 

    3.  Couple all selected parents. Unfortunately this requires that your 
        population number is even.

    4.  Crossover the selected pairs. 

    5.  For each individual produced so far, try to mutate it. 

    6. This new batch will be your population for the next iteration.

TL;DR 
=====

* Population size must be an even number. It won't work if your function have
* A higher value than 4000 in the specified range, unless you set the upperbound 
  parameter when creating the Environment.

Author 
======

github.com/hoarf 
matehackers.org

"""

import numpy as np
from bitstring import BitArray
from functools import total_ordering

X_CHROMOSOME = 0
Y_CHROMOSOME = 1
BINOMIAL_TRY_COUNT = 1
INTEGER_INTERVAL_SIZE = 2
MIN_CUT_POINT = 1

@total_ordering
class Individual(object):
    """ Represents an individual in a gene pool """

    @staticmethod
    def random(options):
        """ Returns a random individual """
        i = Individual(options)
        x_chromosome = np.random.choice(INTEGER_INTERVAL_SIZE,options.representation_size) 
        y_chromosome = np.random.choice(INTEGER_INTERVAL_SIZE,options.representation_size) 
        i.genotype = (x_chromosome, y_chromosome)
        return i

    def __init__(self, options, *args, **kwargs):
        """ genotype: is a sequence of numpy arrays
            options: options for molding this class behavior
        """
        self.genotype = kwargs.get('genotype', None)
        self.representation_size = options.representation_size
        self.mutation_rate = options.mutation_rate
        self.upperbound = options.upperbound
        self.eval_fn = options.eval_fn
        self.min_axis = options.min_axis
        self.max_axis = options.max_axis
        self.options = options

    def __repr__(self):
        return "\nx value: %r (%r)\ny value: %r (%r) f=(%r)" % ( 
           self.genotype[X_CHROMOSOME],
           self.value(X_CHROMOSOME),
           self.genotype[Y_CHROMOSOME],
           self.value(Y_CHROMOSOME),
           self.phenotype_minimized
        )

    def __add__(self, other):
        """ Together with __radd__ allows the sum of two individuals """
        return self.phenotype + other

    def __radd__(self, other):
        """ Together with __add__ allows the sum of two individuals """
        return other + self.phenotype

    def __div__(self, other):
        """ Together with __rdiv__ allows the division of two individuals """
        return self.phenotype/other

    def __rdiv__(self, other):
        """ Together with __div__ allows the division of two individuals """
        return other/self.phenotype

    def __getitem__(self,key):
        """ Allows to index an individual.
            Example: parent[1] 
        """
        return self.genotype[key]

    def __eq__(self, other):
        """ Allows to compare individuals.
            Example: i == i (i is an Individual())
        """
        return self.phenotype == other.phenotype

    def __lt__(self, other):
        """ Required to make a total_ordering relationship between 
            individuals 
        """
        return self.phenotype < other.phenotype     
    
    @property  
    def phenotype(self):
        """ Represents this guy fitness using the maximizing function """
        return self.eval_fn(self.value(X_CHROMOSOME),self.value(Y_CHROMOSOME)) 

    @property
    def phenotype_minimized(self):
        """ Represents this guy fitness using the minimizing function. 
            Because the roulette is used as selection method, a special care
            is needed to prevent negative numbers to spoil the sum of 
            generation fitness.
            The special treatment consist in inverting the target function on 
            the y axis and then adding an specific constant value to the
            target function in order to make all functions points positive in 
            the given interval.
        """
        return -self.eval_fn(
            self.value(X_CHROMOSOME),self.value(Y_CHROMOSOME))+self.upperbound

    def _value_uint(self, gene):
        """ gene: either X_CHROMOSOME or Y_CHROMOSOME
            Converts a BitArray representation into an unsigned integer. 

            Example: _value_uint('110') = 6
        """
        return BitArray(self.genotype[gene]).uint

    def _generate_mutation_mask(self):
        """ Generates a bit mask with a MUTATION_RATE of having 1's 
            values at any given position
            
            Example: [0 0 0 0 0 0 1 0 0]
        """
        return [np.random.binomial(BINOMIAL_TRY_COUNT,self.mutation_rate) 
                  for i in xrange(self.representation_size)]

    def _mutate(self, gene):
        """ Applies the logical_xor operation between the mutation mask and
            the gene
        """
        mask = self._generate_mutation_mask()
        np.logical_xor(self.genotype[gene], mask, self.genotype[gene])

    def value(self, gene):
        """ Returns the 'value' of the gene, or it's value as an unsigned 
            integer
        """
        return self.min_axis+(
            self.max_axis-self.min_axis)*(self._value_uint(gene)/(
                2.0**self.representation_size-1.0))

    def mutate(self):
        """ Tries to apply the mutation to every chromosome this individual has
            Note that the chromosome may not change though. In fact, it 
            probably won't.
        """
        for chromosome, elem in enumerate(self.genotype):
            self._mutate(chromosome) 

class Population(list):
    """ Represents a group or sequence of individuals """

    @staticmethod
    def _swap(parents, chromosome):
        """ Given two chromosomes, tries to swap them in a point chosen 
            randomly between the second position and the second last position
            Example:

                [0 1 | 0 0 1 0]
                [1 1 | 1 1 1 0]
                ---------------
                [1 1 | 0 0 1 0]
                [0 1 | 1 1 1 0]
        """
        parent0 = parents[0]
        parent1 = parents[1]

        # this could have been taken from either parent
        representation_size = parent0.representation_size         
        crossoverpoint = np.random.randint(1,representation_size-1)
        
        parent_0_chromosome = np.hstack([
            parent0[chromosome][:crossoverpoint], 
            parent1[chromosome][crossoverpoint:]
        ])
        
        parent_1_chromosome = np.hstack([
            parent1[chromosome][:crossoverpoint],
            parent0[chromosome][crossoverpoint:]
        ])
        
        return ( parent_0_chromosome , parent_1_chromosome )

    @staticmethod
    def crossover(parents):
        """ Swap portions of chromosomes between two individuals """
        x_chromosome_i1, x_chromosome_i2 = Population._swap(parents,X_CHROMOSOME)        
        y_chromosome_i1, y_chromosome_i2 = Population._swap(parents,Y_CHROMOSOME)        

        options = parents[0].options

        i1 = Individual(options,genotype=(x_chromosome_i1,y_chromosome_i1))
        i2 = Individual(options,genotype=(x_chromosome_i2,y_chromosome_i2))
        return (i1,i2)

    @staticmethod
    def random(options):
        """ Returns a random population of the given size """
        p = Population()
        for i in xrange(options.population_size):
          p.append(Individual.random(options))
        return p

    @property
    def fitness(self):
        """ Represents the cumulative amount of fitness across all individuals 
        """
        return sum(self)

    @property
    def size(self):
        return len(self)

    def select(self):
        """ Returns a list with probability weighted selected parents """
        return np.random.choice(self, self.size, p=[i/self.fitness for i in self])
  
    def pairup(self,parents):
        """ Takes an even number of parents and returns iterator of pair of
            parents. If an odd number of parents is submitted, then the last
            parent is ignored 
        """
        return [(parents[i], parents[i+1]) for i, p in enumerate(parents[::2])]

    @property
    def best(self):
        """ The best individual is the one with the highest fitness """
        return np.amax(self)

class Environment(object):
    """ Represents all the external and algorithmical constraints """

    @staticmethod
    def update_options_with_kwargs(options, kwargs):
       for key in kwargs:
            if key in options:
                options[key] = kwargs[key]

    def __init__(self, *args, **kwargs):
        options = Options()
        Environment.update_options_with_kwargs(
            options, kwargs)
        print "%r" % options              
        self.current_gen = Population.random(options)
        self.gen_count = 0
        self.max_iter = options.max_iter
        self.best_so_far = Individual.random(options)

    def __repr__(self):
      return """gen: %r\ngen_count: %r\nbest: %r\nphenotypes: %r\ngenfitness:
            %r\nprobability_selection:%r\nsample_selection: %r\nbest so far: 
            %r\n""" % (
                self.current_gen,
                self.gen_count,
                self.best,
                [i.phenotype for i in self.current_gen],
                self.current_gen.fitness,
                [i.phenotype/self.current_gen.fitness 
                    for i in self.current_gen], 
                [i.phenotype for i in self.current_gen.select()],
                self.best_so_far
        )

    @property
    def best(self):
        """ Returns the best individual of the current generation """
        return self.current_gen.best

    def step(self):
        """ The algorithm itself 

            1.  Create a empty new Population 

            2.  Select the best parents of our current generation

            3.  Then we iterate over the pairs we formed

            4.  Next we cross the selected pairs over 

            5.  For each individual produced so far, try to mutate it with the 
                given probability

            6.  Append those individuals to the new Population

            7.  If we got anything bather than we previously had, save that
        """
        new_gen = Population()
        selected_parents = self.current_gen.select()
        pairs = self.current_gen.pairup(selected_parents)
        for pair in pairs:
            co_pairs = Population.crossover(pair)
            for parent in co_pairs:
                parent.mutate()
                new_gen.append(parent)
        self.gen_count += 1
        self.current_gen = new_gen
        if self.current_gen.best > self.best_so_far:
            self.best_so_far = self.current_gen.best
        print self

    def fast_foward(self):
        """ Proceeds with the whole thing until the max_iterations is hit """
        while self.gen_count < self.max_iter:
            self.step()

    def next(self):
        """ Advance one generation """
        self.step()

class Options(object):
    """ Captures all the algorithm options """

    REPRESENTATION_SIZE = 20
    MUTATION_RATE = 0.01
    MIN_AXIS = -2.0
    MAX_AXIS = 2.0
    POPULATION_SIZE = 8
    UPPERBOUND = 4000
    MAX_ITER = 100

    @staticmethod
    def Z(x,y):
        return -x*np.sin(np.sqrt(abs(x)))-y*np.sin(np.sqrt(abs(y)))
    
    @staticmethod
    def R(x,y):
        return 100*(y-x**2)**2+(1-x)**2
    
    def __init__(self, *args, **kwargs):
        self.population_size = kwargs.get('population',self.POPULATION_SIZE) 
        self.eval_fn = kwargs.get('eval_fn',
            lambda x,y: Options.R(x,y)-Options.Z(x, y))
        self.min_axis = kwargs.get('min_axis',self.MIN_AXIS)
        self.max_axis = kwargs.get('max_axis',self.MAX_AXIS)
        self.max_iter = kwargs.get('max_iter',self.MAX_ITER)
        self.mutation_rate = kwargs.get('mutation_rate',self.MUTATION_RATE)
        self.upperbound = kwargs.get('upperbound',self.UPPERBOUND)
        self.representation_size = kwargs.get(
            'representation_size',self.REPRESENTATION_SIZE
        )
