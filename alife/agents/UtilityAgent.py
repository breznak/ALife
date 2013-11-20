from alife.agents.agent import Agent

from collections import OrderedDict as dict

class SimpleAgent(Agent):
  """ agent that evaluates utility of the states"""
  
  def __init__(self):
    a=dict()
    t=[]  # target
    super(SimpleAgent, self).__init__(a, t, listMemFields=["score", "visited"], name='Visualizer')
    self.me['x']=0
    self.me['y']=0
    self.me['steps']=0
    self.util = None # UtilityEncoder
  
