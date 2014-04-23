import numpy as np
from bitstring import BitArray

def Z(x,y):
  return (-x*np.sin(np.sqrt(abs(x))))-(y*np.sin(np.sqrt(abs(y))))

def R(x,y):
  return (100*(y-x**2)**2)+((1-x)**2)

def W3(x,y):
  return -(R(x, y) - Z(x,y)) + 4000

def W32(x,y):
  return (R(x, y) - Z(x,y))

REPRESENTATION_SIZE = 20
MUTATION_PROBABILITY = 0.01
MIN_AXIS = -2.0
MAX_AXIS = 2.0
POPULATION_SIZE = 8
MAX_ITER = 100
X_CHROMOSSOME = 0
Y_CHROMOSSOME = 1
BINOMIAL_TRY_COUNT = 1
INTEGER_INTERVAL_SIZE = 2
MIN_CUT_POINT = 1

class Individual(object):

  # magic methods to get the ball rolling

  def __init__(self, *args, **kwargs):
    self.genotype = kwargs.get('genotype', None)
    self.eval_fn = kwargs.get('eval_fn', None)

  def __repr__(self):
    return "\nx value: %r (%r)\ny value: %r (%r) f=(%r)" % (self.genotype[X_CHROMOSSOME],self.value(X_CHROMOSSOME), self.genotype[Y_CHROMOSSOME], self.value(Y_CHROMOSSOME), self.fenotype2(W32 ))

  def __getitem__(self,key):
    return self.genotype[key]

  def __iter__(self):
    for i in self.genotype:
      yield i

  # end magic methods

  # private - not supposed to be exposed

  def _value_uint(self, x_or_y):
    return BitArray(self.genotype[x_or_y]).uint

  def _mutation_mask_generator(self):
    for i in xrange(REPRESENTATION_SIZE):
      yield np.random.binomial(BINOMIAL_TRY_COUNT,MUTATION_PROBABILITY)

  def _mutate(self, x_or_y):
    mask = list(self._mutation_mask_generator())
    np.bitwise_xor(self.genotype[x_or_y],mask,self.genotype[x_or_y])

  # end private
  
  @staticmethod
  def random(eval_fn):
    i = Individual()
    i.genotype = (np.random.choice(INTEGER_INTERVAL_SIZE,REPRESENTATION_SIZE), np.random.choice(INTEGER_INTERVAL_SIZE,REPRESENTATION_SIZE))
    i.eval_fn = eval_fn
    return i

  def value(self, x_or_y):
    return MIN_AXIS+(MAX_AXIS - MIN_AXIS)*(self._value_uint(x_or_y)/(2.0**REPRESENTATION_SIZE-1.0))
  
  def fenotype(self):
    return  self.eval_fn(self.value(X_CHROMOSSOME),self.value(Y_CHROMOSSOME)) 

  def fenotype2(self,eval_fn):
    return  eval_fn(self.value(X_CHROMOSSOME),self.value(Y_CHROMOSSOME)) 

  def mutate(self):
    self._mutate(X_CHROMOSSOME)
    self._mutate(Y_CHROMOSSOME)

class Population(list):

  @staticmethod
  def random(size, eval_fn):
    p = Population()
    p.eval_fn = eval_fn
    for i in xrange(size):
      p.append(Individual.random(eval_fn))
    return p

  def fitness(self):
    # defines the fitness of our population
    return sum (i.fenotype() for i in self)

  def select(self):
    # returns a list with probability weighted selected parents 
    return np.random.choice(self,POPULATION_SIZE, p=[i.fenotype()/self.fitness() for i in self])
  
  def pairup(self,parents):
    # takes an even number of parents and returns iterator of pair of parents
    for i, p in enumerate(parents[::2]):
      yield (parents[i], parents[i+1])

  @staticmethod
  def _swap(parents, chromossome):
    crossoverpoint = np.random.randint(1,REPRESENTATION_SIZE)
    parent0 = parents[0]
    parent1 = parents[1]

    parent_0_chromossome = np.hstack([parent0[chromossome][:crossoverpoint], parent1[chromossome][crossoverpoint:]])
    parent_1_chromossome = np.hstack([parent1[chromossome][:crossoverpoint], parent0[chromossome][crossoverpoint:]])
    return ( parent_0_chromossome , parent_1_chromossome )

  @staticmethod
  def crossover(parents):
    # takes a sequence of 2 indviduals and returns a tuple of two parents crossed over
    x_chromossome_i1, x_chromossome_i2 = Population._swap(parents, X_CHROMOSSOME)        
    y_chromossome_i1, y_chromossome_i2 = Population._swap(parents, Y_CHROMOSSOME)        

    i1 = Individual(genotype=(x_chromossome_i1,y_chromossome_i1),eval_fn=W3)
    i2 = Individual(genotype=(x_chromossome_i2,y_chromossome_i2),eval_fn=W3)
    return (i1,i2)

  def best(self):
    bi = self.best_individual()
    return "f(%r,%r) = %r" % (bi.value(X_CHROMOSSOME),bi.value(Y_CHROMOSSOME),bi.fenotype())

  def best_individual(self):
    return np.amax(self)

class Enviroment(object):

  def __init__(self):
    self.nextgen = Population.random(POPULATION_SIZE,W3)
    self.gencount = 0
    self.best_so_far = Individual.random(W3)

  def __repr__(self):
    return "gen: %r\ngencount: %r\nbest: %r\nfenotypes: %r\ngenfitness: %r\nprobability_selection:%r\nsample_selection: %r\nbest so far: %r\n" % (self.nextgen, self.gencount, self.best(), [i.fenotype() for i in self.nextgen], self.nextgen.fitness(), [i.fenotype()/self.nextgen.fitness() for i in self.nextgen],[i.fenotype() for i in self.nextgen.select()],self.best_so_far)

  def best(self):
    return self.nextgen.best()

  def step(self):
    newgen = Population()
    selected_parents = self.nextgen.select()
    pairs = self.nextgen.pairup(selected_parents)
    for pair in pairs:
      co_pairs = Population.crossover(pair)
      for parent in co_pairs:
        parent.mutate()
        newgen.append(parent)
    self.gencount += 1
    self.nextgen = newgen
    if self.nextgen.best_individual().fenotype() > self.best_so_far.fenotype():
      print "========= hooray!! ========"
      self.best_so_far = self.nextgen.best_individual()
    print self

  def go_to_last_generation(self):
    while self.gencount < MAX_ITER:
      self.step()

  def next(self):
    self.step()