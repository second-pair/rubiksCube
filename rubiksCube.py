#! /usr/bin/python
#  Author:  Blair Edwards 2018
#  For now, this is a programme that will end up solving Rubik's Cubes of arbitrary size.
#  I intend that the programme will display a cube being solved and output a list of moves.
#  I'll also need to implement a shuffling algorithm.

import pyglet

#  Parameters & Globals
#cube size
#face colours
#starting face
#shuffling options
#font

#  Pyglet Init
window = pyglet .window .Window ()

#  Pyglet Render
@window .event
def on_draw ():
	pass
	window .clear ()
#	label .draw ()
#	graphics .Batch ()
	cubesBatch .draw ()

#  For now, we'll just start by rendering some text.
#label = pyglet .text .Label (
#	"Hello, world!",
#	font_name = "Calibri",
#	font_size = 36,
#	x = window .width // 2,
#	y = window .height // 2,
#	anchor_x = "center",
#	anchor_y = "center"
#	)

#  Let's add some cubes (this should become a class later).
#  Well, they're just squares for now.
cubesBatch = pyglet .graphics .Batch ()

cube1 = cubesBatch .add (4, pyglet .gl .GL_QUADS, None, ("v2i", (10, 10, 10, 40, 40, 40, 40, 10)))
cube2 = cubesBatch .add (4, pyglet .gl .GL_QUADS, None, ("v2i", (80, 80, 80, 120, 120, 120, 120, 80)))


#  Setup complete!
pyglet .app .run ()
