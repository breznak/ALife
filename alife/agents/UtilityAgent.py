from alife.agents.agent import Agent

from collections import OrderedDict as dict

class SimpleAgent(Agent):
  """ agent that evaluates utility of the states"""
  
  def __init__(self):
    a=dict()
    t=[]  # target
    super(SimpleAgent, self).__init__(a, t, name='Visualizer')
    self.me['x']=0
    self.me['y']=0
    self.me['steps']=0
    self.util = None # UtilityEncoder

  ### actions:
  def go(self, x, y):
    """go to x,y"""
    # check bounds
    if(x<0 or y<0 or x>=self.world.dimX or y>=self.world.dimY):
      if(self.verbose > 2):
        print "Agent ", self.name, " is crossing the borders! (",x,",",y,")"
      return
    self.me['x']=x
    self.me['y']=y
    self.me['steps']+=1
    self.world.tiles[x][y]['score'] = self.util.getScoreIN([x, y])

  ### target(s):
  # define in example code
