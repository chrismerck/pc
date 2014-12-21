# sem.py - Structural Equation Models
#

from random import random
from collections import OrderedDict

class StructuralEquation(object):
  def __init__(self,name,parents,eq):
    self._d = {'name':name, 'parents':parents, 'eq':eq}
  def __getitem__(self,key):
    return self._d[key]

class StructuralEquationModel(object):
  def __init__(self):
    self._vars = OrderedDict()
  def add_var(self,name,parents,eq):
    assert not name in self._vars
    self._vars[name] = StructuralEquation(name,parents,eq)
  def sample(self):
    rv = OrderedDict()
    for name in self._vars:
      se = self._vars[name]
      rv[name] = se['eq'](*map(lambda parent: rv[parent], se['parents']))
    return rv

def test_sem():
  sem = StructuralEquationModel()
  sem.add_var('sprinkler',[],lambda: random()<0.5 )
  sem.add_var('rain',[],lambda: random()<0.2 )
  sem.add_var('lawn',['sprinkler','rain'],
      lambda sprinkler, rain: (random()<0.9) if (rain or sprinkler) else (random()<0.1))
  sem.add_var('carpet',['lawn'],
      lambda lawn: (random()<0.9) if lawn else (random()<0.1))
  print(sem.sample())


if __name__=='__main__':
  test_sem()

# take structural equation (with binary variables), generate samples
# take samples, recover causal graph
