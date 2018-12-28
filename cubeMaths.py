#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  This will end up holding the cube matrix and the cube-solving algorithms

#  I've decided to merge the RubiksCubeMatrix and RubiksCubeVisual classes,
#  since they were essentially controlling the same bit of data.
#  This way, they don't have to keep updating each other every time something
#  changes.

from preferences import *
from primitives import *

class RubiksCube:
	def __init__ (self):
		self .renderBatch = pyglet .graphics .Batch ()
		self .sideMatrix = []
		self .visualMatrix = []
		#self .theRubiksCubeVisual = RubiksCubeVisual ()

	def init (self, cubeCount = userCubeSize, cubeLength = userCubeLength, xPos = 0, yPos = 0, zPos = 0):
		self .cubeCount = cubeCount
		self .cubeLength = cubeLength
		self .xPos = xPos - int (cubeLength * cubeCount / 2)
		self .yPos = yPos - int (cubeLength * cubeCount / 2)
		self .zPos = zPos - int (cubeLength * cubeCount / 2)

		self .generateSideMatrix ()
		self .generateVisualCube ()

	#  Maybe we DO want to merge visuals and matrices after all...
	#  We'd maybe end up with the sideMatrix array as an array of faces, but
	#  that wouldn't be as efficient, so maybe stick wtih separate matrics...
	#  Here we go again.
	def generateSideMatrix (self):
		#  Generate each side
		for i in range (6):
			self .sideMatrix .append ([])

			for j in range (self .cubeCount):
				self .sideMatrix [i] .append ([])

				for k in range (self .cubeCount):
					self .sideMatrix [i][j] .append (i)

	def generateVisualCube (self):
		#  Generate the visual cube
		for currSide in range (6):
			self .visualMatrix .append ([])

			for x in range (self .cubeCount):
				self .visualMatrix [currSide] .append ([])

				for y in range (self .cubeCount):
					self .visualMatrix [currSide][x] .append (self .generateAFace (currSide, x, y))

	def generateAFace (self, theFace, xPos, yPos):
		#  Was originally for cubes, will convert to faces
		#  We'll need to use the given RubiksCube X, Y and Z positions to work
		#  out the faces' positions and rotations

		#  Calculate angles and positions
		#for ...
		#  Grab a new cube
		newFace = CubeFace ()
		#newFace .init (xPos, yPos, zPos, xAngle, yAngle, zAngle, cubeLength, startColour)
		newFace .init (xPos * self .cubeLength, yPos * self .cubeLength, theFace * 10, 0, 0, 0, self .cubeLength, theFace)

		#  Add it to the render queue
		self .renderBatch .add (newFace .getVerticesCount (), pyglet .gl .GL_QUADS, None,
			(newFace .getVerticesType (), newFace .getVertices ()),
			(newFace .getColoursType (), newFace .getColours ())
		)
		#  Return it to the caller
		return newFace

	def getTheSides (self):
		return self .sideMatrix

	def getAFace (self, theFace, theXIndex, theYIndex):
		return self .sideMatrix [theFace][theXIndex][theYIndex]

	def printFaceCount (self):
		#  Sum up the number of stored cubes
		theCount = 0
		for level1 in self .sideMatrix:
			for level2 in level1:
				for level3 in level2:
					theCount += 1
		print ("%d faces counted." % theCount)

	def renderTheFaces (self):
		#  Updates the cube's positions via the Pyglet batch
		self .renderBatch .draw ()

	def swapLines (self, line1: tuple, line2: tuple):
		#  Function to rotate a slice of faces
		#  We'll need a different way to select the slice being rotated

		#  Figure out which items actually needto be swapped
		#  Due to how the indexing works, we'll need to account for skipping
		#  across sub-lists

		#  Start swapping
		tempLine = []
		for i in range (self .cubeCount):
			#  Store one face's slice in a temporary variable
			tempLine .append (self .sideMatrix [line1][i])
		#  Like this, but better.
		for i in range (self .cubeCount):
			sideMatrix [line1][i] = sideMatrix [line2][i]
		for i in range (self .cubeCount):
			sideMatrix [line2][i] = sideMatrix [line3][i]
		for i in range (self .cubeCount):
			sideMatrix [line3][i] = sideMatrix [line4][i]
		for i in range (self .cubeCount):
			#  Use the temporary variable to fill in the final face-slice
			sideMatrix [line4][i] = tempLine [i]

theRubiksCube = RubiksCube ()
