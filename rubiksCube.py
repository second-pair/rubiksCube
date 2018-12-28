#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  For now, this is a programme that will end up solving Rubik's Cubes of arbitrary size.
#  I intend that the programme will display a cube being solved and output a list of moves.
#  I'll also need to implement a shuffling algorithm.

#  Dependencies:
#  pyglet (pip-able)

#  I've cannibalised this file to get started:
#https://github.com/adamlwgriffiths/Pyglet/blob/master/examples/graphics.py



#  Includes
import pyglet
from pyglet .gl import *
from pygletHandler import *
from preferences import *
from cubeMaths import *



##  Main Code
pygletSetup ()
#theRubiksCubeVisual .init (userCubeSize, userCubeLength, 0, 0, 0)
#theRubiksCubeVisual .printCubeCount ()
#theRubiksCubeVisual .rotateAFace (1, 'cw')

theRubiksCubeMatrix .init (userCubeSize)
for i in range (6):
    print ("Face %d:" % i)
    print (theRubiksCubeMatrix .getFace (i))
    print ("\n")

#  Setup complete!
pyglet .app .run ()
