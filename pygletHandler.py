#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  Trying my best to abstract all the Pyglet nonsense to its own file

#  I've cannibalised this file to get started:
#https://github.com/adamlwgriffiths/Pyglet/blob/master/examples/graphics.py

from preferences import *
import pyglet
from pyglet .gl import *
from primitives import mainRenderBatch
if showMatricesWindow == 1:
	from cubeMaths import theRubiksCube



#  Initialise the window
window = pyglet .window .Window (userScreenWidth, userScreenHeight, resizable = True)
window .set_location (userScreenHorizontal, userScreenVertical)
window .activate ()
spinTheCube = True

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
	#  Main render update loop
	global rx, ry, rz
	if spinTheCube:
		rx += dt * 11 * userCubeRotateRate
		ry += dt * 15 * userCubeRotateRate
		rz += dt * 5 * userCubeRotateRate
		rx %= 360
		ry %= 360
		rz %= 360

#  Refresh and render the view
@window .event
def on_draw ():

	#window .clear ()
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0, 0, userCameraDistance)
	glRotated (rx, 1, 0, 0)
	glRotatef (ry, 0, 1, 0)
	glRotatef (rz, 0, 0, 1)

	mainRenderBatch .draw ()
	if showMatricesWindow == 1:
		theRubiksCube .matricesViewerUpdate ()

#  Add toggle-to-pause
@window .event
def on_mouse_press (x, y, button, modifiers):
	if button == pyglet .window .mouse .LEFT:
		global spinTheCube
		spinTheCube = not spinTheCube
@window .event
def on_key_press (symbol, modifiers):
	if symbol == pyglet .window .key .SPACE:
		global spinTheCube
		spinTheCube = not spinTheCube
	if symbol == pyglet .window .key .Q:
		exit ()

#  One-time GL setup
def pygletSetup ():

	glClearColor (userBackgroundColour[0] / 255, userBackgroundColour[1] / 255, userBackgroundColour[2] / 255, 0)
	#glColor3f  (25.0 /255, 196.0 / 255, 241.0 / 255)
	glEnable (GL_DEPTH_TEST)

	#pyglet.clock.set_fps_limit(60)
	#pyglet .clock .schedule (update)
	pyglet .clock .schedule_interval (update, 1.0/60.0)

#  Initialise rotation variables
rx = ry = rz = 0
pygletSetup ()
