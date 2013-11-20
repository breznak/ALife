#!/bin/env python2

from alife.worlds.world import World, Point
from alife.agents.UtilityAgent import SimpleAgent
from alife.utils.utils import dumpToArray
import math
from nupic.encoders.utility import SimpleUtilityEncoder

# common settings:
dimX=25
dimY=25
items=None
target=Point(4,9)


def main():
  w = World(dimX, dimY, items)
  ag = SimpleAgent()
  ag.world=w
  ag.actions['go']=ag.go
  ag.targets=[reachedTarget]
  ag.util = SimpleUtilityEncoder(length=2, minval=0, maxval=max(dimX,dimY)-1, scoreMin=0, scoreMax=100, scoreResolution=0.1)
  ag.util.setEvaluationFn(euclDistance)
  ag.start=ag.world._getRandomPos()

  # walk it, baby
  for x in xrange(dimX):
    for y in xrange(dimY):
      ag.actions['go'](x,y)

  utilityMap = dumpToArray('score', ag.world.tiles)
  print utilityMap

  _visualize(utilityMap)


#########################################
def reachedTarget(ag, target):
  """are we there yet?"""
  return ag.me['x']==target.x and ar.me['y']==target.y

def euclDistance(listCoords):
  """eval fn for agent is distance to target """
  x=listCoords[0]
  y=float(listCoords[1])
  tx=target.x
  ty=target.y
  return math.sqrt((tx-x)**2 + (ty-y)**2)

def _visualize(map):
  try:
#    from alife.simulators.mayavi.plot3D import plot3d
    from mayavi import mlab
  except:
    print "Can't show you nice picture; couldn't import mayavi"
    return
#  plot3d(map)
  mlab.barchart(map, scale_factor=0.6) 
  mlab.show()

  

#########################################
if __name__ == "__main__":
    main()
