#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  For now, this is a programme that will end up solving Rubik's Cubes of arbitrary size.
#  I intend that the programme will display a cube being solved and output a list of moves.
#  I'll also need to implement a shuffling algorithm.

#  I've cannibalised this file to get started:
#https://github.com/adamlwgriffiths/Pyglet/blob/master/examples/graphics.py

import pyglet
from pyglet .gl import *

#  Parameters & Globals
#cube size
#face colours
#starting face
#shuffling options
#font



##  Main Code

#  Initialise the window
window = pyglet .window .Window ()

# One-time GL setup
def setup ():
	glClearColor (1, 1, 1, 1)
	glColor3f (1, 0, 0)
	glEnable (GL_DEPTH_TEST)
	glEnable (GL_CULL_FACE)


#  Really this is an Init thing, despite being on_resize
#  Seems to sort the depth problem
@window.event
def on_resize (width, height):
	# Override the default on_resize handler to create a 3D projection
	glViewport (0, 0, width, height)
	glMatrixMode (GL_PROJECTION)
	glLoadIdentity ()
	gluPerspective (60., width / float (height), .1, 1000.)
	glMatrixMode (GL_MODELVIEW)
	return pyglet .event .EVENT_HANDLED

#  Update our viewport's rotation
def update (dt):
	global rx, ry, rz
	rx += dt * 1
	ry += dt * 80
	rz += dt * 30
	rx %= 360
	ry %= 360
	rz %= 360
pyglet.clock.schedule(update)

#  Refresh and render the view
@window .event
def on_draw ():
	pass
#	window .clear ()
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0, 0, -4)
#	glRotatef (30, 1, 0, 0)
#	glRotatef (30, 0, 1, 0)
#	glRotatef (30, 0, 0, 1)
	glRotatef(rz, 0, 0, 1)
	glRotatef(ry, 0, 1, 0)
	glRotatef(rx, 1, 0, 0)
	cubesBatch .draw ()

setup ()
rx = ry = rz = 0


#  Let's add some cubes (this should become a class later).
cubesBatch = pyglet .graphics .Batch ()

cube1 = cubesBatch .add (24, pyglet .gl .GL_QUADS, None, ("v3i", (
	50, 50, 50,
	50, 80, 50,
	80, 80, 50,
	80, 50, 50,

	50, 50, 50,
	50, 80, 50,
	50, 80, 80,
	50, 50, 80,

	50, 50, 50,
	80, 50, 50,
	80, 50, 80,
	50, 50, 80,

	50, 80, 50,
	50, 80, 80,
	80, 80, 80,
	80, 80, 50,

	80, 50, 50,
	80, 50, 80,
	80, 80, 80,
	80, 80, 50,

	50, 50, 80,
	50, 80, 80,
	80, 80, 80,
	80, 50, 80
	)))



#  Setup complete!
pyglet .app .run ()
