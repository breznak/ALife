import numpy

def dumpToArray(val, dict3d):
  """dumps a value from 3D dict to numpy array"""
  ar = numpy.zeros((len(dict3d), len(dict3d[0])))
  for x in dict3d:
    for y in dict3d[x]:
      ar[x][y]=dict3d[x][y][val]
  return ar
