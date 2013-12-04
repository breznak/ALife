#!/bin/env python2

from alife.worlds.world import World, Point
from alife.agents.UtilityAgent import SimpleAgent
from alife.utils.utils import dumpToArray
import math
import sys
import numpy
from nupic.encoders.extras.utility import SimpleUtilityEncoder

# common settings:
items=None
target=Point(4,9)
agent=None

foods = []
_hungerMax = 40

def main(targetX=4, targetY=9, dimX=25, dimY=25):
  global target
  global agent
  target=Point(int(targetX), int(targetY))
  w = WorldWithResources(int(dimX), int(dimY), count=[10], types=['food']) # world with some food
  ag = SimpleAgent()
  ag.world=w
  ag.actions['go']=go
  ag.targets=[reachedTarget]
  ag.util = SimpleUtilityEncoder(length=2, minval=0, maxval=max(int(dimX),int(dimY)), scoreMin=0, scoreMax=100, scoreResolution=0.1)
  ag.util.setEvaluationFn(euclDistance)
  ag.start=ag.world._getRandomPos()
  ag.me['hunger']=0 # not hungry

  agent = ag

  # walk it, baby
  for x in xrange(w.dimX):
    for y in xrange(w.dimY):
      ag.actions['go'](ag, x, y)

  utilityMap = dumpToArray('score', ag.mem, ag.world.dimX, ag.world.dimY)
#  print utilityMap

  _visualize(utilityMap)


#########################################
# defines target:
def reachedTarget(ag, target):
  """are we there yet?"""
  return ag.me['x']==target.x and ag.me['y']==target.y

# defines score:
def euclDistance(listCoords):
  """eval fn for agent is distance to target """
  global target
  global agent
  x=listCoords[0]
  y=float(listCoords[1])
  tx=target.x
  ty=target.y
  w=agent.world.tiles
  if(w[x][y]['food']==1):
    print "Found some tasty food!"
    agent.me['hunger']=0

  if reachedTarget(agent, target):
    return 0

  dst_target =  math.sqrt((tx-x)**2 + (ty-y)**2)
  (_,dst_food) = _toNearestFood(x,y)

  return (1- agent.me['hunger']/_hungerMax)*dst_target + (agent.me['hunger']/_hungerMax)*dst_food # there's + bcs we're finding a min (target dist = 0)
#  return dst_target + dst_food

def _toNearestFood(x,y):
  global foods
  max_idx = 0
  max_val = 100000
  for i,p in enumerate(foods):
    fx,fy = p
    d = math.sqrt((x-fx)**2 + (y-fy)**2)
    if d < max_val:
      max_idx = i
      max_val = d
  return (max_idx, max_val)

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
  if ag.me['hunger']<=_hungerMax:
    ag.me['hunger']+=1 # walking is tiresome
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
class WorldWithResources(World):
  import numpy

  def __init__(self, dimX, dimY, count=[5], types=['food']):
    """distributes (list) count of (list) types resources randomly; 
    """
    super(WorldWithResources, self).__init__(dimX, dimY, types)
    global foods

    for i,typee in enumerate(types):
      for x in xrange(0,dimX): # zero-out
        for y in xrange(0,dimY):
          self.tiles[x][y][typee]=0

      cnt = count[i]
      for c in xrange(0,cnt):
        rx = numpy.random.randint(0,dimX,1).tolist()[0]
        ry = numpy.random.randint(0,dimY,1).tolist()[0]
        self.tiles[rx][ry][typee] = 1
        foods.append( (rx,ry) )


#########################################
if __name__ == "__main__":
  if(len(sys.argv)==3):
    main(sys.argv[1], sys.argv[2])
  elif(len(sys.argv)==5):
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
  else:
    print "Use: \n python /path/to/utility_map.py [targetX targetY [dimX dimY]]"
    main()
