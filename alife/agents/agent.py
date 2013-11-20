
from alife.worlds.world import Point, World
import random
from collections import defaultdict
from collections import OrderedDict as dict

class Agent(object):
  """abstract class for an Agent, the AI"""

  def __init__(self, dictActions, listTargets, world=None, startPos=None, verbose=0, name='Smith'):
    """
    params:
      world -- the environment/world model; 
                 shared among (all) agents, don't store any personal things here, writable (so eg eaten food is removed);
      startPos -- starting position within the world
      dictActions -- a dict of all actions agent can carry; 
          each action is a function of 1 argument: agent; which it can modify
      listTargets -- list of functions of 1 argument: agent; 
          don't modify these arguments, return True/False if target is met 
    """
    self.world = world
    self.start = startPos
    self.targets = []
    self.actions = dictActions
    self.targets = listTargets[:]
    # me : inner states
    self.me = dict() # me['hunger']=16
    # mem: 3D map, mem['x']['y']['visited']=1, saves as memory of things in the world, personal things written here
    self.mem = defaultdict(lambda: defaultdict(dict))
    self.name = name

  def _randomChoice(listA):
    """choose one thing from list randomly"""
    return listA[random.randint(0,len(listA)-1)]
