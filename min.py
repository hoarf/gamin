import numpy as np
from bitstring import BitArray

def OBJETIVO(x,y):
  return Z(x, y) - R(x,y)

def Z(x,y):
  return -x*np.sqrt(abs(x))-y*np.sin(np.sqrt(abs(y)))

def R(x,y):
  return 100*(y-x**2)**2+(1-x)**2

def W3(x,y):
  return OBJETIVO(x,y)

REPR_SIZE = 20
MUTATION_PROBABILITY = 0.01
MIN_X = -2.0
MAX_X = 2.0
POPULATION_SIZE = 4
MAX_ITER = 1000

class Individual(object):
  
  @staticmethod
  def random(eval_fn):
    i = Individual()
    i.genotype = (np.random.choice(2,REPR_SIZE), np.random.choice(2,REPR_SIZE))
    i.eval_fn = eval_fn
    return i

  def __init__(self, *args, **kwargs):
    self.genotype = kwargs.get('genotype', None)
    self.eval_fn = kwargs.get('eval_fn', None)

  def value(self, x_or_y):
    return BitArray(self.genotype[x_or_y]).uint

  def __getitem__(self,key):
    return self.genotype[key]

  def _decimal_value(self, x_or_y):
    return MIN_X+(MAX_X - MIN_X)*(self.value(x_or_y)/(2.0**REPR_SIZE-1.0))
  
  def fenotype(self):
    return self.eval_fn(self._decimal_value(0),self._decimal_value(1))

  def __iter__(self):
    for i in self.genotype:
      yield i

  def __repr__(self):
    return "\nx value: %r\ny value: %r\n" % self.genotype

  def _mutation_mask_generator(self):
    for i in xrange(REPR_SIZE):
      yield np.random.binomial(1,MUTATION_PROBABILITY)

  def _mutate(self, x_or_y):
    mask = list(self._mutation_mask_generator())
    np.bitwise_xor(self.genotype[x_or_y],mask,self.genotype[x_or_y])

  def mutate(self):
    self._mutate(0)
    self._mutate(1)

  def y(self):
    self.genotype[1]

  def x(self):
    self.genotype[0]

class Population(list):

  @staticmethod
  def random(size, eval_fn):
    p = Population()
    for i in xrange(size):
      p.append(Individual.random(eval_fn))
    return p

  def sum(self):
    return sum (i.fenotype() for i in self)

  def select(self):
    #returns a list with probability weighted selected parents 
    return np.random.choice(self,POPULATION_SIZE, p=[i.fenotype()/self.sum() for i in self])
  
  def pairup(self,parents):
    #takes an even number of parents and returns a pair
    for i, p in enumerate(parents[::2]):
      yield (parents[i], parents[i+1])

  def crossover(self,parents):
    #takes a sequence of 2 parents and returns a tuple of two parents crossed over
    crossoverpoint = np.random.randint(1,REPR_SIZE)
    print "cop: %r" % crossoverpoint
    p1g1 = np.hstack([parents[0][0][crossoverpoint:],parents[1][0][:crossoverpoint]])
    p2g1 = np.hstack([parents[1][0][crossoverpoint:],parents[0][0][:crossoverpoint]])
    p1g2 = np.hstack([parents[0][1][crossoverpoint:],parents[1][1][:crossoverpoint]])
    p2g2 = np.hstack([parents[1][1][crossoverpoint:],parents[0][1][:crossoverpoint]])
    
    i1 = Individual(genotype=(p1g1,p1g2),eval_fn=W3)
    i2 = Individual(genotype=(p2g1,p2g2),eval_fn=W3)
    return (i1,i2)

  def best(self):
    return "f(%r,%r) = %r" % (np.amin(self)._decimal_value(0),np.amin(self)._decimal_value(1),np.amin(self).fenotype())

class Envirioment(object):

  def __init__(self):
    self.nextgen = Population.random(POPULATION_SIZE,W3)
    self.gencount = 0
    self.best = float("inf")
  
  def __repr__(self):
    return "gen: %r\ngencount: %r\nbest: %r\n" % (self.nextgen, self.gencount, self.best)

  def step(self, gen):
    newgen = Population()
    selected_parents = gen.select()
    pairs = gen.pairup(selected_parents)
    for pair in pairs:
      co_pairs = gen.crossover(pair)
      for parent in co_pairs:
        parent.mutate()
        newgen.append(parent)
    self.gencount += 1
    self.best = self.nextgen.best()
    return newgen

  def finish(self):
    while self.gencount < MAX_ITER:
      self.nextgen = self.step(self.nextgen)
      print "%r\n" % self
   
  def next(self):
    self.step(self.nextgen)
    print self