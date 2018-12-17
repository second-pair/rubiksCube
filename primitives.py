#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  Trying my best to abstract all the primitives info to its own file

import pyglet
from pyglet .gl import *
from pygletHandler import *



##  Batches

cubesBatch = pyglet .graphics .Batch ()



##  Primitives

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

cube2 = cubesBatch .add (8, pyglet .gl .GL_QUADS, None, ("v3i", (
	0, 0, 100,
	0, 10, 100,
	10, 10, 100,
	10, 0, 100,
	
	0, 0, 0,
	0, 10, 0,
	10, 10, 0,
	10, 0, 0
	)))
