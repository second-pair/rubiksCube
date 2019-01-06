#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  This holds the cube matrix, the matrix of cube-graphics and the cube-solving
#  algorithms.
#  For the purposes of this project:
#    A face refers to a single side of a single cube in a Rubik's Cube - IE
#    a sticker.
#    A side refers to a collection of such faces, all facing the same way.
#  The idea is that the actual faces will remain the same and each time we
#  swap faces around, we do the equivalent of peeling off the stickers and
#  placing them back where we want them.

#  Need to account for rotating a whole face

from preferences import *
from primitives import CubeFace

sideOpposites = {0: 5, 1: 3, 2: 4, 3: 1, 4: 2, 5: 0}
sideRotations = {0: 0, 1: 3, 2: 0, 3: 1, 4: 0, 5: 0}
#0 bottom
#1 back
#2 right
#3 front
#4 left
#5 top



class RubiksCube:
	def __init__ (self):
		self .sideMatrix = []
		self .visualMatrix = []

	def init (self, cubeCount = userCubeSize, cubeLength = userCubeLength, xPos = 0, yPos = 0, zPos = 0):
		self .cubeCount = cubeCount
		self .cubeLength = cubeLength
		self .cubeSpacingModifier = int (self .cubeLength * userCubeSpacing)

		self .xPos = xPos - int (cubeLength * cubeCount / 2)
		self .yPos = yPos - int (cubeLength * cubeCount / 2)
		self .zPos = zPos - int (cubeLength * cubeCount / 2)

		self .generateSideMatrix ()
		self .generateVisualCube ()

	#  Generates a matrix of matrices of matrices to hold the cube's faces and
	#  face-statuses
	def generateSideMatrix (self):
		#  Generate each side
		for i in range (6):
			self .sideMatrix .append ([])

			for j in range (self .cubeCount):
				self .sideMatrix [i] .append ([])

				for k in range (self .cubeCount):
					self .sideMatrix [i][j] .append (i)

	#  Generates a matrix of matrices of matrices to hold the cube's visual info
	def generateVisualCube (self):
		for currSide in range (6):
			self .visualMatrix .append ([])

			for x in range (self .cubeCount):
				self .visualMatrix [currSide] .append ([])

				for y in range (self .cubeCount):
					self .visualMatrix [currSide][x] .append (self .generateAFace (currSide, x, y))

	#  Generates a single visual face, in the correct orientation
	def generateAFace (self, theFace, index1, index2):
		#  Grab relevant variables
		startIndex = self .cubeCount // 2
		index1Scaled = index1 * self .cubeSpacingModifier
		index2Scaled = index2 * self .cubeSpacingModifier
		startScaled = 0 * self .cubeSpacingModifier
		endScaled = (self .cubeCount - 1) * self .cubeSpacingModifier

		#  Grab a new cube
		newFace = CubeFace ()

		#  Calculate co-ordinates
		if theFace == 0:
			faceXPos = self .xPos + index1Scaled
			faceYPos = self .yPos + startScaled
			faceZPos = self .zPos + index2Scaled
		elif theFace == 1:
			faceXPos = self .xPos + index1Scaled
			faceYPos = self .yPos + index2Scaled
			faceZPos = self .zPos + startScaled
		elif theFace == 2:
			faceXPos = self .xPos + endScaled
			faceYPos = self .yPos + index1Scaled
			faceZPos = self .zPos + index2Scaled
		elif theFace == 3:
			faceXPos = self .xPos + index1Scaled
			faceYPos = self .yPos + index2Scaled
			faceZPos = self .zPos + endScaled
		elif theFace == 4:
			faceXPos = self .xPos + startScaled
			faceYPos = self .yPos + index1Scaled
			faceZPos = self .zPos + index2Scaled
		elif theFace == 5:
			faceXPos = self .xPos + index1Scaled
			faceYPos = self .yPos + endScaled
			faceZPos = self .zPos + index2Scaled

		#  Initialise the new face with our co-ords and return it to the caller
		newFace .init (faceXPos, faceYPos, faceZPos, self .cubeLength, theFace)
		return newFace

	#  Returns the cube-side-face-matrix (not the visual one)
	def getTheSides (self):
		return self .sideMatrix

	#  Returns a specific face from that matrix
	def getAFace (self, theFace, theXIndex, theYIndex):
		return self .sideMatrix [theFace][theXIndex][theYIndex]

	#  Returns the number of faces currentlly stored in the cube-matrix
	def getFaceCount (self):
		#  Sum up the number of stored cubes by unwrapping the sideMatrix list
		theCount = 0
		for level1 in self .sideMatrix:
			for level2 in level1:
				for level3 in level2:
					theCount += 1
		return theCount

	#  I'm doing you next, I promise!
	def rotateSlice (self, startSide, destSide, startSideX, startSideY):
		#  Function to rotate a slice of faces

		#  How the indexing works:
		#  To keep things simple, I'm having the indexing work by selecting
		#  the face we're intending to move, then specifying a destination
		#  side that we want it to end up at.

		#  Determine the order of face-swapping
		#  This is pretty simple, as we always want to select the faces in
		#  rotating order as we go round the cube.  IE:
		#  The first and second faces are provided to us,
		#  The third face is opposite the first,
		#  The fourth face is opposite the second.
		theSides = (startSide, destSide, sideOpposites [startSide], sideOpposites [destSide])

		#  Figure out which items actually need to be swapped
		#  Due to how the indexing works, we'll need to account for skipping
		#  across sub-lists

		for aSide in theSides:
			if sideRotations [aSide] == 0:
				for i in range (self .cubeCount):
					self .visualMatrix [aSide][startSideX][i] .setFaceColour (7 + i)
			elif sideRotations [aSide] == 1:
				for i in range (self .cubeCount):
					self .visualMatrix [aSide][i][startSideY] .setFaceColour (7 + i)
			elif sideRotations [aSide] == 2:
				for i in range (self .cubeCount):
					self .visualMatrix [aSide][startSideX][i] .setFaceColour (7 + i)
			elif sideRotations [aSide] == 3:
				for i in range (self .cubeCount):
					self .visualMatrix [aSide][i][startSideY] .setFaceColour (7 + i)

		'''
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
		'''

	def oneoff (self):
		for i in range (1, 5):
			self .visualMatrix [i][0][0] .setFaceColour (6)
		self .rotateSlice (1, 2, 4, 4)
		#for i in range (6):
		#	self .visualMatrix [i][0][2] .setFaceColour (6)
		#	self .visualMatrix [i][2][0] .setFaceColour (7)




theRubiksCube = RubiksCube ()
