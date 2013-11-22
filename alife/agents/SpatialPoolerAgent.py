from alife.agents.agent import Agent

from nupic.bindings.algorithms import SpatialPooler as SP
from nupic.encoders.utility import SimpleUtilityEncoder as UtilEncoder


class SpatialPoolerAgent(Agent):
  """ agent that uses CAM (content-addresable memory; 
      uses SpatialPooler to make abstractions and generalizations of inputs to learn actions. 
      Can be trained in both supervised and unsupervised ways. 
      Uses utility encoder with feedback = 1, to remember 1 step -> start={stateA, actionA} , score(start)==score after applying actionA"""

  
  def __init__(self, numFields):
    a=dict()
    t=[]  # target
    super(SpatialPoolerAgent, self).__init__(a, t, listMemFields=["score", "visited"], name='SPlearner')
    self.me['x']=0
    self.me['y']=0
    self.me['steps']=0
    self.enc = ag.util = SimpleUtilityEncoder(length=numFields, minval=0, maxval=max(int(dimX),int(dimY)), scoreMin=0, scoreMax=100, scoreResolution=0.1)
    # spatial pooler
    self.sp = None # spatial pooler
        SP(
        inputDimensions = [5],
        columnDimensions = [5],
        potentialRadius = 5,
        potentialPct = 0.5,
        globalInhibition = False,
        localAreaDensity = -1.0,
        numActiveColumnsPerInhArea = 3,
        stimulusThreshold=0,
        synPermInactiveDec=0.01,
        synPermActiveInc = 0.1,
        synPermConnected = 0.10,
        minPctOverlapDutyCycle = 0.1,
        minPctActiveDutyCycle = 0.1,
        dutyCyclePeriod = 10,
        maxBoost = 10.0,
        seed = -1,
        spVerbosity = 0,)

