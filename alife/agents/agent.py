
from alife.worlds.world import Point, World
import random
from collections import defaultdict

class Agent(object):
  """abstract class for an Agent, the AI"""

  def __init__(self, dictActions, listTargets, world=None, startPos=None, verbose=0, name='Smith'):
    """
    params:
      world -- the environment/world model
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
    self.me = dict() # me['hunger']=16
    self.name = name

  def _randomChoice(listA):
    """choose one thing from list randomly"""
    return listA[random.randint(0,len(listA)-1)]
