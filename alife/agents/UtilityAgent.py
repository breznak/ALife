from alife.agents.agent import Agent

from nupic.encoders.utility import SimpleUtilityEncoder as UtilEnc

from collections import OrderedDict as dict

class SimpleAgent(Agent):
  """ agent that evaluates utility of the states"""
  
  def __init__(self):
    a=dict()
    a['go']=go
    t=[]
    super(SimpleAgent, self).__init__(a, t, name='Visualizer')
    self.me['x']=0
    self.me['y']=0
    self.me['steps']=0
    self.util = None

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
    self.world[x][y]['score'] = util.getScoreIN([x y])

  ### target(s):
  # define in example code