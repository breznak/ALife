
from collections import namedtuple
import random
from collections import defaultdict
from collections import OrderedDict as dict

# represents position in 2D
Point = namedtuple('Point', 'x y')


class World(object):
  """ abstract class for world environoments;
      params:
        dimX, dimY -- dimensions <0, dim)
        listItems -- list of all possible proporties that can be found on a tile; eg: food, fire, coin, enemy,...; stored in 2D map tiles
  """

  def __init__(self, dimX, dimY, listItems=None, name='Oz'): 
    self.dimX=dimX
    self.dimY=dimY
    self.allItems = listItems
    self.tiles = defaultdict(lambda: defaultdict(dict)) # tiles[x][y]['gold']=37
    self.name = name

  def getItems(self, pos):
    """get items on this position"""
    return self.tiles[pos.x][pos.y].values()

  ############################################
  def _getRandomPos(self):
    """return random point within the world"""
    return [ random.randint(0, self.dimX-1), random.randint(0, self.dimY-1) ]

