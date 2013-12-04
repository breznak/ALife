#!/bin/env python2

from alife.worlds.world import World, Point
from alife.agents.UtilityAgent import SimpleAgent
from alife.utils.utils import dumpToArray, zeros
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

def main(targetX=4, targetY=9, dimX=250, dimY=250):
  global target
  global agent
  target=Point(int(targetX), int(targetY))
  if not(target.x< dimX and target.y < dimY):
    raise Exception("Target coords unreachable!")

  w = WorldWithResources(int(dimX), int(dimY), count=[2], types=['food']) # world with some food
  ag = SimpleAgent(actions={'go' : go}, targets=[reachedTarget], world=w)
  ag.verbose = 2
  ag.util = SimpleUtilityEncoder(length=2, minval=0, maxval=max(int(dimX),int(dimY)), scoreMin=0, scoreMax=100, scoreResolution=0.1)
  ag.util.setEvaluationFn(euclDistance)
  ag.start=ag.world._getRandomPos()
  ag.me['hunger']=0 # not hungry
  ag.mem = zeros(['score'],ag.mem,ag.world.dimX, ag.world.dimY, zero=-1)
  ag.mem = zeros(['hunger'],ag.mem,ag.world.dimX, ag.world.dimY, zero=-1)
  ag.mem = zeros(['target'],ag.mem,ag.world.dimX, ag.world.dimY, zero=-1)
  agent = ag

  # walk it, baby
  NUM_WALKS=1
  NUM_STARTS=1
  for _ in xrange(0, NUM_STARTS):
   ag.me['x'],ag.me['y'] = ag.world._getRandomPos()
   print "Starting from:", ag.me['x'], ag.me['y']

   for _ in xrange(0,NUM_WALKS):
     while not reachedTarget(ag, target):
      x = ag.me['x']
      y = ag.me['y']
      moves = [-1,0,1] # for move left-right, front-back
      dx = moves[numpy.random.randint(0,len(moves),1)[0]]
      dy = moves[numpy.random.randint(0,len(moves),1)[0]]
      if dx == 0 and dy == 0: # would stand still
        continue
      ag.actions['go'](ag, x+dx, y+dy)

  utilityMap = dumpToArray('score', ag.mem, ag.world.dimX, ag.world.dimY)
#  print utilityMap


  targetMap = dumpToArray('target', ag.mem, ag.world.dimX, ag.world.dimY)
  _visualize(targetMap)

  hungerMap = dumpToArray('hunger', ag.mem, ag.world.dimX, ag.world.dimY)
  _visualize(hungerMap)
  _visualize(utilityMap)



#########################################
# defines target:
def reachedTarget(ag, target):
  """are we there yet?"""
  if ag.verbose > 2:
    print ag.me['x'], target.x, ag.me['y'], target.y
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

  if reachedTarget(agent, target):
    return -10 # make target visible

  dst_target =  math.sqrt((tx-x)**2 + (ty-y)**2)
  (_,dst_food) = _toNearestFood(x,y)

  w=agent.world.tiles
  if(w[x][y]['food']==1):
    #print "Found some tasty food!"
    agent.me['hunger']=0

  hunger = agent.me['hunger']

  if agent.mem[x][y]['target'] == -1:
    agent.mem[x][y]['target'] = dst_target
  else:
    agent.mem[x][y]['target'] = min(dst_target,agent.mem[x][y]['target'])

  if agent.mem[x][y]['hunger'] == -1:
    agent.mem[x][y]['hunger']= dst_food
  else:
    agent.mem[x][y]['hunger'] = min(agent.mem[x][y]['hunger'], dst_food)

  return agent.mem[x][y]['target'] +((agent.me['hunger']/_hungerMax)* agent.mem[x][y]['hunger'])
#  return (1- agent.me['hunger']/_hungerMax)*dst_target + (agent.me['hunger']/_hungerMax)*dst_food # there's + bcs we're finding a min (target dist = 0)
#  return dst_target + dst_food
#  return agent.mem[x][y]['hunger'] + agent.mem[x][y]['target']
  if hunger > _hungerMax*0.8:  # hunger >80% --> eat!
    return agent.mem[x][y]['hunger']
  elif hunger < _hungerMax*0.33: # hunger < 33% --> pursuit life-goals
    return agent.mem[x][y]['target']
  else:
    return agent.mem[x][y]['target'] +(_hungerMax- agent.mem[x][y]['hunger'])


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
  if ag.mem[x][y]['score'] in [-1]: #default
    ag.mem[x][y]['score'] = ag.util.getScoreIN([x, y])
  else:
    ag.mem[x][y]['score'] = ag.util.getScoreIN([x, y]) #min(ag.mem[x][y]['score'],ag.util.getScoreIN([x, y])) 
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
  mlab.figure()
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
