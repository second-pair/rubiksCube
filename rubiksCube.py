#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  For now, this is a programme that will end up solving Rubik's Cubes of arbitrary size.
#  I intend that the programme will display a cube being solved and output a list of moves.
#  I'll also need to implement a shuffling algorithm.

#  Dependencies:
#  pyglet (pip-able)



#  Includes
import pyglet
from pyglet .gl import *
from pygletHandler import *
from preferences import *
from cubeMaths import *



##  Main Code
pygletSetup ()

#  Generate the cube
theRubiksCube .init (userCubeSize, userCubeLength, 0, 0, 0)
print ("%d faces counted." % theRubiksCube .getFaceCount ())

#  Setup complete!
pyglet .app .run ()
