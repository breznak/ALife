import numpy

def dumpToArray(val, dict3d, dimX, dimY):
  """dumps a value from 3D dict to numpy array"""
  ar = numpy.zeros((len(dict3d), len(dict3d[0])))
  for x in xrange(0,dimX):
    for y in xrange(0,dimY):
      ar[x][y]=dict3d[x][y][val]
  return ar

def zeros(listKeys, dict3d, dimX, dimY, zero=0):
  """clears; filles a 3D dictionary;
     params:
       listKeys -- list of keys for inner-most dict ("score","visited",...)
       dict3d -- 3D map, dict, matrix
       zero = the filler value, (default 0)"""
  for x in xrange(0,dimX):
    for y in xrange(0,dimY):
      for key in listKeys:
        dict3d[x][y][key]=zero
  return dict3d
