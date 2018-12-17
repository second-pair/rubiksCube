#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  Trying my best to abstract all the Pyglet nonsense to its own file

#  I've cannibalised this file to get started:
#https://github.com/adamlwgriffiths/Pyglet/blob/master/examples/graphics.py

import pyglet
from pyglet .gl import *
from primitives import *



##  Main Code

#  Initialise the window
window = pyglet .window .Window ()

#  Really this is an Init thing, despite being on_resize
#  Seems to sort the depth problem
@window.event
def on_resize (width, height):
	#  Override the default on_resize handler to create a 3D projection
	glViewport (0, 0, width, height)
	glMatrixMode (GL_PROJECTION)
	glLoadIdentity ()
	gluPerspective (90., width / float (height), .1, 1000.)
	glMatrixMode (GL_MODELVIEW)
	return pyglet .event .EVENT_HANDLED

#  Update our viewport's rotation
def update (dt):
	global rx, ry, rz
	rx += dt * 50
	ry += dt * 40
	rz += dt * 15
	rx %= 360
	ry %= 360
	rz %= 360

#  Refresh and render the view
@window .event
def on_draw ():
#	window .clear ()
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0, 0, -100)
	glRotatef (rz, 0, 0, 1)
	glRotatef (ry, 0, 1, 0)
	glRotatef (rx, 1, 0, 0)
	cubesBatch .draw ()

#  One-time GL setup
def setup ():
	glClearColor (40.0 / 255, 43.0 / 255, 53.0 / 255, 0)
	glColor3f (25.0 /255, 196.0 / 255, 241.0 / 255)
	glEnable (GL_DEPTH_TEST)
#	glEnable (GL_CULL_FACE)
	pyglet .clock .schedule (update)

#  Nearly there...
setup ()
rx = ry = rz = 0