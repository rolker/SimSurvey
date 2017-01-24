#!/usr/bin/env python

import sys
import json

config = '''
{
  "seafloor": {
      "default_depth": -100,
      "features": [
        {"type": "box", "xcenter": 20, "ycenter": 30, "xsize": 5, "ysize": 8, "zsize":2},
        {"type": "box", "xcenter": 420, "ycenter": 350, "xsize": 25, "ysize": 12, "zsize":4.5},
        {"type": "hemisphere", "xcenter": 780, "ycenter": 130, "radius": 7}
      ]
  },
  "surveys": [
    {
      "output": "test.xyz",
      "beam_count": 45,
      "swath_width": 200,
      "xstart": 10,
      "ystart": 0,
      "xfinish": 1000,
      "yfinish": 900
    }
  ] 
      
}
'''

class Seafloor:
  def __init__(self, config):
    self.depth = config['default_depth']
    self.features = []
    
  def depth(self,x,y):
    ret = self.depth
    return ret 
  
class Feature:
  def __init__(self):
    pass
  





if len(sys.argv) > 1:
  config = open(sys.argv[1]).read()
  
configuration = json.loads(config)

seafloor = Seafloor(configuration['seafloor'])

