#!/usr/bin/env python

import sys
import json
import math

config = '''
{
  "seafloor": {
      "default_depth": -100,
      "features": [
        {"type": "box", "xcenter": 20, "ycenter": 30, "xsize": 5, "ysize": 8, "zsize":2},
        {"type": "box", "xcenter": 420, "ycenter": 350, "xsize": 25, "ysize": 12, "zsize":4.5},
        {"type": "hemisphere", "xcenter": 780, "ycenter": 130, "radius": 7},
        {"type": "cone", "xcenter": 200, "ycenter": 500, "radius": 15, "height": 12}
      ]
  },
  "surveys": [
    {
      "output": "test.xyz",
      "beam_count": 75,
      "swath_width": 200,
      "speed": 5,
      "ping_rate": 2,
      "lines":[
        {"xstart": 10, "ystart": 0, "xfinish": 1000, "yfinish": 900},
        {"xstart": 925, "ystart": 1000, "xfinish": 0, "yfinish": 100}
      ]
    },
    {
      "output": "full.xyz",
      "beam_count": 2000,
      "swath_width": 1000,
      "speed": 1,
      "ping_rate": 2,
      "lines":[
        {"xstart": 500, "ystart": 0, "xfinish": 500, "yfinish": 1000}
      ]
    }

  ] 
}
'''

class Seafloor:
  def __init__(self, config):
    self.depth = float(config['default_depth'])
    self.features = []
    for fc in config['features']:
      if fc['type'] == 'box':
        self.features.append(Box(fc))
      if fc['type'] == 'cone':
        self.features.append(Cone(fc))
    
  def depthAt(self,x,y):
    ret = self.depth
    for f in self.features:
      ret = max(ret,f.depthAt(x,y,self.depth))
    return ret 
  
class Feature:
  def __init__(self, config):
    self.xcenter = float(config['xcenter'])
    self.ycenter = float(config['ycenter'])

  def depthAt(self,x,y,default):
    return default 

class Box(Feature):
  def __init__(self,config):
    Feature.__init__(self,config)
    self.xsize = float(config['xsize'])
    self.ysize = float(config['ysize'])
    self.zsize = float(config['zsize'])

  def depthAt(self,x,y,default):
    if x >= self.xcenter-self.xsize/2.0 and x <= self.xcenter+self.xsize/2.0:
      if y >= self.ycenter-self.ysize/2.0 and y <= self.ycenter+self.ysize/2.0:
        return default+self.zsize
    return default
    
class Cone(Feature):
  def __init__(self,config):
    Feature.__init__(self,config)
    self.radius = float(config['radius'])
    self.height = float(config['height'])
    
  def depthAt(self,x,y,default):
    dx = x-self.xcenter
    dy = y-self.ycenter
    distance = math.sqrt(dx*dx+dy*dy)
    if distance <= self.radius:
      return default+self.height*(1.0-distance/self.radius)
    return default

  
class SurveyLine:
  def __init__(self, config):
    self.start = (float(config['xstart']),float(config['ystart']))
    self.finish = (float(config['xfinish']),float(config['yfinish']))

  def run(self,survey):
    meters_per_ping = survey.speed/float(survey.ping_rate)
    dx = self.finish[0]-self.start[0]
    dy = self.finish[1]-self.start[1]
    d = math.sqrt(dx*dx+dy*dy)
    dx /= d
    dy /= d
    ldx = dy
    ldy = -dx
    ping_count = math.ceil(d/meters_per_ping)
    print ping_count,'pings'
    x = self.start[0]
    y = self.start[1]
    ping = 0
    while ping < ping_count:
      d = survey.seafloor.depthAt(x,y)
      print ping,x,y,d
      if survey.beam_count > 1:
        beam = 0
        lx = x-ldx*survey.swath_width/2.0
        ly = y-ldy*survey.swath_width/2.0
        while beam < survey.beam_count:
          d = survey.seafloor.depthAt(lx,ly)
          survey.outputFile.write(str(lx)+','+str(ly)+','+str(d)+'\n')
          lx += ldx*survey.ping_spacing
          ly += ldy*survey.ping_spacing
          beam += 1
      else:
        survey.outputFile.write(str(x)+','+str(y)+','+str(d)+'\n')
      x += dx*meters_per_ping
      y += dy*meters_per_ping
      ping += 1

class Survey:
  def __init__(self, config):
    self.outputFilename = config['output']
    self.speed = float(config['speed'])
    self.ping_rate = float(config['ping_rate'])
    self.beam_count = config['beam_count']
    self.swath_width = float(config['swath_width'])
    if self.beam_count > 1:
      self.ping_spacing = self.swath_width/float(self.beam_count)
    else:
      self.ping_spacing = 0
    self.lines = []
    for l in config['lines']:
      self.lines.append(SurveyLine(l))

  def run(self, seafloor):
    self.seafloor = seafloor
    self.outputFile = open(self.outputFilename,'w')
    for l in self.lines:
      l.run(self)



if len(sys.argv) > 1:
  config = open(sys.argv[1]).read()
  
configuration = json.loads(config)

seafloor = Seafloor(configuration['seafloor'])

for sc in configuration['surveys']:
  print sc['output']
  s = Survey(sc)
  s.run(seafloor)
