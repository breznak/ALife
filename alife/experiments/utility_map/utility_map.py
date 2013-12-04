#!/bin/env python2

from alife.worlds.world import World, Point
from alife.agents.UtilityAgent import SimpleAgent
from alife.utils.utils import dumpToArray
import math
import sys
from nupic.encoders.extras.utility import SimpleUtilityEncoder

# common settings:
items=None
target=Point(4,9)

def main(targetX=4, targetY=9, dimX=25, dimY=25):
  global target
  target=Point(int(targetX), int(targetY))
  w = World(int(dimX), int(dimY), items)
  ag = SimpleAgent()
  ag.world=w
  ag.actions['go']=go
  ag.targets=[reachedTarget]
  ag.util = SimpleUtilityEncoder(length=2, minval=0, maxval=max(int(dimX),int(dimY)), scoreMin=0, scoreMax=100, scoreResolution=0.1)
  ag.util.setEvaluationFn(euclDistance)
  ag.start=ag.world._getRandomPos()

  # walk it, baby
  for x in xrange(w.dimX):
    for y in xrange(w.dimY):
      ag.actions['go'](ag, x, y)

  utilityMap = dumpToArray('score', ag.mem)
#  print utilityMap

  _visualize(utilityMap)


#########################################
# defines target:
def reachedTarget(ag, target):
  """are we there yet?"""
  return ag.me['x']==target.x and ar.me['y']==target.y

# defines score:
def euclDistance(listCoords):
  """eval fn for agent is distance to target """
  global target
  x=listCoords[0]
  y=float(listCoords[1])
  tx=target.x
  ty=target.y
  return math.sqrt((tx-x)**2 + (ty-y)**2)

# defines action:
def go(ag, x, y):
  """go to x,y"""
  # check bounds
  if(x<0 or y<0 or x>=ag.world.dimX or y>=ag.world.dimY):
    if(ag.verbose > 2):
      print "Agent ", ag.name, " is crossing the borders! (",x,",",y,")"
    return
  ag.me['x']=x
  ag.me['y']=y
  ag.me['steps']+=1
  ag.mem[x][y]['score'] = ag.util.getScoreIN([x, y])
  ag.mem[x][y]['visited'] = 1

#########################################
# helper functions:
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
  if(len(sys.argv)==3):
    main(sys.argv[1], sys.argv[2])
  elif(len(sys.argv)==5):
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
  else:
    print "Use: \n python /path/to/utility_map.py [targetX targetY [dimX dimY]]"
    main()
