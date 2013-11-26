from alife.agents.agent import Agent

from nupic.bindings.algorithms import SpatialPooler as SP
from nupic.encoders.utility import SimpleUtilityEncoder as UtilEncoder
from nupic.algorithms.CLAClassifier import CLAClassifier as Clas

import numpy

def evalFn(l):
  return sum(l)

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
    self.enc = UtilEncoder(length=numFields, minval=0, maxval=100, scoreMin=0, scoreMax=100, scoreResolution=0.1)
    self.enc.setEvaluationFn(evalFn)
    # spatial pooler
    self.sp = SP(
        inputDimensions = [self.enc._offset],
        columnDimensions = [1024],
        potentialRadius = 15,
        potentialPct = 0.5,
        globalInhibition = True,
        localAreaDensity = -1.0,
        numActiveColumnsPerInhArea = 5,
        stimulusThreshold=0,
        synPermInactiveDec=0.01,
        synPermActiveInc = 0.1,
        synPermConnected = 0.20,
        minPctOverlapDutyCycle = 0.1,
        minPctActiveDutyCycle = 0.1,
        dutyCyclePeriod = 10,
        maxBoost = 10.0,
        seed = -1,
        spVerbosity = 2,)
    self.cls = Clas() # classifier 


  def testSP(self):
    dataSize = 5
    totalPatterns = 5
    patterns=[]
    for i in xrange(0,totalPatterns):
      patterns.append(numpy.random.randint(0,2,dataSize).tolist()) # generate input patterns

    # SP learn patterns
    for _ in xrange(0,10): #learn-repeate 
     for pattern in patterns:
      ret = numpy.zeros(1024)
      print "input=", pattern
      enc = self.enc.encode(pattern)
      print "encoded=",enc
      self.sp.compute(enc,True, ret)
      nz = numpy.nonzero(ret)[0].tolist()
      print len(nz)
      score = self.enc.getScoreIN(pattern)
      buckets = self.enc.getBucketIndices({'simpleUtility' : pattern,'utility' : score})
      print self.enc.getScalarNames(), buckets
      print self.cls.compute(recordNum=1, patternNZ=nz, classification={'bucketIdx': buckets[0], 'actValue': score }, learn=True, infer=True)

    print "Test"
    for pattern in patterns:
      ret = numpy.zeros(1024)
      enc = self.enc.encode(pattern)
      self.sp.compute(enc,False, ret)
      nz = numpy.nonzero(ret)[0].tolist()
      score = self.enc.getScoreIN(pattern)
      buckets = self.enc.getBucketIndices({'simpleUtility' : pattern,'utility' : score})
      print self.cls.compute(recordNum=1, patternNZ=nz, classification={'bucketIdx': buckets[0], 'actValue': None }, learn=False, infer=True)


if __name__ == "__main__":
  a = SpatialPoolerAgent(5)
  a.testSP()
