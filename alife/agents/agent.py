
from alife.worlds.world import Point, World
import random
from collections import defaultdict

class Agent(object):
  """abstract class for an Agent, the AI"""

  def __init__(self, world, startPos, listActions, listTargets, verbose=0):
    """
    params:
      world -- the environment/world model
      startPos -- starting position within the world
      listActions -- list of all actions agent can carry; 
          each action is a function of 1 argument: agent; which it can modify
      listTargets -- list of functions of 1 argument: agent; 
          don't modify these arguments, return True/False if target is met 
    """
    self.world = world
    self.start = startPos
    self.targets = []
    self.actions = listActions[:]
    self.targets = listTargets[:]
    self.me = defaultdict(dict)

  def _randomChoice(listA):
    """choose one thing from list randomly"""
    return listA[random.randint(0,len(listA)-1)]
