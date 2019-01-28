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

from preferences import *
from primitives import CubeFace

#  Setup Tk, if required
if showMatricesWindow == 1:
	import tkinter as tk
	#  Setup the root window
	root = tk .Tk ()
	root .title ("Matrices Window")
	#  Setup DPI Scaling
	root .tk .call ('tk', 'scaling', (userCubeSize + matricesWindowCorrection / userCubeSize) / (matricesWindowScale * root .winfo_screenheight () / 1080))

sideOpposites = {0: 5, 1: 3, 2: 4, 3: 1, 4: 2, 5: 0}
sideRotations = {0: 0, 1: 3, 2: 0, 3: 1, 4: 0, 5: 0}
#0 bottom
#1 back
#2 right
#3 front
#4 left
#5 top

#  This puppy, well...
#  First value is the face you're looking at
#  Second value pair (first sub-tuple) is a neighbouring face and the closest
#  of its sides, out of x-close, y-close, x-far, y-far
#  Third value pair is the next clockwise face and etc.
#  This garbage make a bit more sense if you stare at the Matrices Viewer
sideNeighbours = {
0: ((1, 2), (4, 0), (3, 0), (2, 0)),
1: ((0, 0), (2, 3), (5, 2), (4, 1)),
2: ((0, 3), (3, 3), (5, 3), (1, 3)),
3: ((0, 2), (4, 3), (5, 0), (2, 1)),
4: ((0, 1), (1, 1), (5, 1), (3, 1)),
5: ((1, 0), (2, 2), (3, 2), (4, 2)),
}



class RubiksCube:
	def __init__ (self):
		#  Maybe these want to be classes one day?
		self .sideMatrix = []
		self .visualMatrix = []
		self .MatricesViewerData = []

	def init (self, cubeCount = userCubeSize, cubeLength = userCubeLength, xPos = 0, yPos = 0, zPos = 0):
		self .cubeCount = cubeCount
		self .cubeLength = cubeLength
		self .cubeSpacingModifier = int (self .cubeLength * userCubeSpacing)

		self .xPos = xPos - int (cubeLength * cubeCount / 2)
		self .yPos = yPos - int (cubeLength * cubeCount / 2)
		self .zPos = zPos - int (cubeLength * cubeCount / 2)

		self .generateSideMatrix ()
		self .generateVisualCube ()
		if showMatricesWindow == 1:
			self .buildMatricesViewer ()


	#  Generates a matrix of matrices of matrices to hold the cube's faces and
	#  face-statuses
	def generateSideMatrix (self):
		#  Generate each side
		for currSide in range (6):
			self .sideMatrix .append ([])

			for j in range (self .cubeCount):
				self .sideMatrix [currSide] .append ([])

				for k in range (self .cubeCount):
					self .sideMatrix [currSide][j] .append (currSide)


	#  Generates a matrix of matrices of matrices to hold the cube's visual info
	def generateVisualCube (self):
		for currSide in range (6):
			self .visualMatrix .append ([])

			for j in range (self .cubeCount):
				self .visualMatrix [currSide] .append ([])

				for k in range (self .cubeCount):
					self .visualMatrix [currSide][j] .append (self .generateAFace (currSide, j, k))

	#  Generates a single visual face, in the correct orientation
	def generateAFace (self, theFace, index1, index2):
		#  Need to tweak orientations & direction of generation

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
			faceYPos = - (self .yPos + index2Scaled + self .cubeLength)
			faceZPos = self .zPos + startScaled
		elif theFace == 2:
			faceXPos = self .xPos + endScaled
			faceYPos = self .yPos + index2Scaled
			faceZPos = - (self .zPos + index1Scaled + self .cubeLength)
		elif theFace == 3:
			faceXPos = self .xPos + index1Scaled
			faceYPos = self .yPos + index2Scaled
			faceZPos = self .zPos + endScaled
		elif theFace == 4:
			faceXPos = self .xPos + startScaled
			faceYPos = self .yPos + index2Scaled
			faceZPos = self .zPos + index1Scaled
		elif theFace == 5:
			faceXPos = self .xPos + index1Scaled
			faceYPos = self .yPos + endScaled
			faceZPos = - (self .zPos + index2Scaled + self .cubeLength)

		#  Initialise the new face with our co-ords and return it to the caller
		newFace .init (faceXPos, faceYPos, faceZPos, self .cubeLength, theFace)
		return newFace


	def buildMatricesViewer (self):
		#  Generate the face labels
		self .bMVGFL (5, 3, self .getASide2D (0))
		self .bMVGFL (7, 3, self .getASide2D (1))
		self .bMVGFL (3, 5, self .getASide2D (2))
		self .bMVGFL (3, 3, self .getASide2D (3))
		self .bMVGFL (3, 1, self .getASide2D (4))
		self .bMVGFL (1, 3, self .getASide2D (5))

		#  Generate vertical spacers
		for i in range (4):
			self .bMVGFL (1, i * 2, " ")
		#  Generate horizontal spacer(s)
		self .bMVGFL (0, 3, " ")

		#  Position the windos
		root .geometry ("+%d+%d" % (root .winfo_screenwidth () - root .winfo_width (), 0))

	def bMVGFL (self, row, column, text):
		#  build Matrix Viewer Generate Face Label
		newLabel = tk .Label (root, text = text)
		newLabel .grid (row = row, column = column)
		self .MatricesViewerData .append (newLabel)

	def MatricesViewerUpdate (self):
		for i in range (6):
			 self .MatricesViewerData [i]['text'] = self .getASide2D (i)
		root .update ()


	#  Returns the cube-side-face-matrix (not the visual one)
	def getTheSides (self):
		return self .sideMatrix

	def getASide (self, theSide):
		return self .sideMatrix [theSide]

	def getASide2D (self, theSide):
		#  Flatten out a side matrix into a text-based 2D representative (or tuple of texts)
		the2DSide = ""
		#  Unwrap each sub-matrix
		#  Note that to get an "as taught in school" grid, we need to mess with
		#  the unwrapping a bit...
		for y in range (self .cubeCount - 1, -1, -1):
			for x in range (self .cubeCount):
				the2DSide += str (self .sideMatrix [theSide][x][y])
			the2DSide += "\n"

		# for sideSlice in self .getASide (theSide):
		# 	#  Unwrap each sub-matrix
		# 	for currValue in sideSlice:
		# 		the2DSide += str (currValue)
		# 	#the2DSide .append (tempSlice)
		return the2DSide

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
	def rotateSlice (self, startSide, destSide, segNumber):
		#  Function to rotate a slice of faces
		#  Need to account for rotating a whole face

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
		#  It might be worth determining an axis of rotation and going
		#  from there?

		sideStrips = []
		for _ in range (4):
			sideStrips .append ([])

		#  Copy initial strip data to sideStrips
		stripSegment = 0
		for aSide in theSides:

			if sideRotations [aSide] == 0:
				for i in range (self .cubeCount):
					sideStrips [stripSegment] .append (self .sideMatrix [aSide][startSideX][i])
			elif sideRotations [aSide] == 1:
				for i in range (self .cubeCount):
					sideStrips [stripSegment] .append (self .sideMatrix [aSide][i][startSideY])
			elif sideRotations [aSide] == 2:
				for i in range (self .cubeCount):
					sideStrips [stripSegment] .append (self .sideMatrix [aSide][self .cubeCount - startSideX - 1][self .cubeCount - i - 1])
			elif sideRotations [aSide] == 3:
				for i in range (self .cubeCount):
					sideStrips [stripSegment] .append (self .sideMatrix [aSide][self .cubeCount - i - 1][self .cubeCount - startSideY - 1])
			stripSegment += 1

		#  Re-organise sideStrips
		sideStrips .append (sideStrips [0])
		sideStrips .pop (0)

		#  Copy the shifted sideStrips back to their faces
		stripSegment = 0
		for aSide in theSides:
			if sideRotations [aSide] == 0:
				for i in range (self .cubeCount):
					self .sideMatrix [aSide][startSideX][i] = sideStrips [stripSegment][i]
					self .visualMatrix [aSide][startSideX][i] .setFaceColour (sideStrips [stripSegment][i])
			elif sideRotations [aSide] == 1:
				for i in range (self .cubeCount):
					self .sideMatrix [aSide][i][startSideY] = sideStrips [stripSegment][i]
					self .visualMatrix [aSide][i][startSideY] .setFaceColour (sideStrips [stripSegment][i])
			elif sideRotations [aSide] == 2:
				for i in range (self .cubeCount):
					self .sideMatrix [aSide][self .cubeCount - startSideX - 1][self .cubeCount - i - 1] = sideStrips [stripSegment][i]
					self .visualMatrix [aSide][self .cubeCount - startSideX - 1][self .cubeCount - i - 1] .setFaceColour (sideStrips [stripSegment][i])
			elif sideRotations [aSide] == 3:
				for i in range (self .cubeCount):
					self .sideMatrix [aSide][self .cubeCount - i - 1][self .cubeCount - startSideY - 1] = sideStrips [stripSegment][i]
					self .visualMatrix [aSide][self .cubeCount - i - 1][self .cubeCount - startSideY - 1] .setFaceColour (sideStrips [stripSegment][i])
			stripSegment += 1

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

	def rotateFace (self, theFace, direction, depth):
		#  Function to rotate a face CW or CCW
		#  Tested somewhat and seems to work :)
		#  Need to add rotating the slice that touches the face

		#  Generate a new matrix to store the new face
		tempSide = []
		for i in range (self .cubeCount):
			tempSide .append ([])
			for j in range (self .cubeCount):
				tempSide[i] .append ([])

		#  Set up the Xs and Ys to count in the right directions
		currX_ = 0
		currY_ = 0
		if direction == 0:
			#  Rotating CW:
			#  x -> -y
			#  y -> x
			newX_ = self .cubeCount - 1
			newY_ = 0
			newXStep = -1
			newYStep = 1
		else:
			#  Rotating CCW:
			#  x -> y
			#  y -> -x
			newX_ = 0
			newY_ = self .cubeCount - 1
			newXStep = 1
			newYStep = -1

		currY = currY_
		newY = newY_
		for _ in range (self .cubeCount):
			#  Step along existing Y
			currX = currX_
			newX = newX_
			for _ in range (self .cubeCount):
				#  Step along existing X

				#  Look up the existing colour
				tempColour = self .sideMatrix [theFace][currX][currY]
				#  Save that colour to the side and visual matrices
				tempSide [newY][newX] = tempColour
				self .visualMatrix [theFace][newY][newX] .setFaceColour (tempColour)

				currX += 1
				newX += newXStep
			currY += 1
			newY += newYStep

		#  Assign the temporary side to the sideMatrix
		self .sideMatrix [theFace] = tempSide

		#  call self .rotateSlice (stuff, use sideSliceMap)



	def oneoff (self):
		for i in range (6):
			self .sideMatrix [i][0][1] = ((i + 1) % 6)
			self .visualMatrix [i][0][1] .setFaceColour ((i + 1) % 6)
		self .rotateSlice (3, 4, 3)



theRubiksCube = RubiksCube ()
