#!/usr/bin/env python

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray
import numpy as np

def display():
    global firstTime
    global vertexArray
    if firstTime:
      vertexArray = vbo.VBO(data)
      firstTime = False
      
    # Clear the color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0,0.0,-6.0)
    
    glScalef(scale,scale,scale)
    
    glRotatef(pitch,1.0,0.0,0.0)
    glRotatef(yaw,0.0,0.0,1.0)
    glTranslatef(-centerx,-centery,-centerz)
    
    glEnableClientState(GL_VERTEX_ARRAY)
    vertexArray.bind()
    glVertexPointerf(vertexArray)
    glDrawArrays(GL_POINTS, 0, len(data))
    glDisableClientState(GL_VERTEX_ARRAY)


    glutSwapBuffers()

def reshape(w,h):
  global width
  global height
  width = w
  height = h
  glViewport(0,0,w,h)
  glutPostRedisplay()

def mouse(button, state, x, y):
  global scale
  global startx
  global starty
  global startPitch
  global startYaw
  global rotating
  if ((button == 3) or (button == 4)):
    if (state != GLUT_UP):
      if button == 3:
        scale *= 1.1
      else:
        scale /= 1.1
      glutPostRedisplay()
  if (button == 0):
    if state == GLUT_DOWN:
      startx = x
      starty = y
      startPitch = pitch
      startYaw = yaw
      rotating = True
    else:
      rotating = False


def mouseMotion(x,y):
  global pitch
  global yaw
  if rotating:
    dx = x-startx
    dy = y-starty
    pitch = startPitch + dy
    yaw = startYaw + dx
    glutPostRedisplay()

data = []
scale = 0.01
width = 1
height = 1
centerx = 0.0
centery = 0.0
centerz = 0.0
pitch = 0.0
yaw = 0.0

starty = 0
startPitch = 0
startx = 0
startYaw = 0
rotating = False

firstTime = True
vertexArray = None

minx = None
miny = None
minz = None

for l in open(sys.argv[1]).readlines():
  parts = l.strip().split(',')
  data.append((float(parts[0]),float(parts[1]),float(parts[2])))
  if minx is None:
    minx = data[0][0]
    maxx = minx
    miny = data[0][1]
    maxy = miny
    minz = data[0][2]
    maxz = minz
  minx = min(minx,data[-1][0])
  maxx = max(maxx,data[-1][0])
  miny = min(miny,data[-1][1])
  maxy = max(maxy,data[-1][1])
  minz = min(minz,data[-1][2])
  maxz = max(maxz,data[-1][2])

centerx = minx + (maxx-minx)/2.0
centery = miny + (maxy-miny)/2.0
centerz = minz + (maxz-minz)/2.0

print centerx,centery,centerz

data = np.array(data,dtype='f')

glutInit(sys.argv)

# Create a double-buffer RGBA window.   (Single-buffering is possible.
# So is creating an index-mode window.)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

# Create a window, setting its title
glutCreateWindow('xyzViewer')

# Set the display callback.  You can set other callbacks for keyboard and
# mouse events.
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
glutMotionFunc(mouseMotion)
# Run the GLUT main loop until the user closes the window.
glutMainLoop()
