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
from time import sleep
import threading
import random

#  Setup Tk, if required
if showMatricesWindow == 1:
	import tkinter as tk
	#  Setup the root window
	root = tk .Tk ()
	root .title ("Matrices Window")
	#  Setup DPI Scaling
	root .tk .call ('tk', 'scaling', (userCubeSize + matricesWindowCorrection / userCubeSize) / (matricesWindowScale * root .winfo_screenheight () / 1080))

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
#  0 -> bottom
#  1 -> back
#  2 -> right
#  3 -> front
#  4 -> left
#  5 -> top



class RubiksCube:
	def __init__ (self):
		#  Maybe these want to be classes one day?
		self .sideMatrix = []
		self .visualMatrix = []
		self .matricesViewerData = []

	def init (self, cubeCount = userCubeSize, cubeLength = userCubeLength, xPos = 0, yPos = 0, zPos = 0, updatePeriod = userMovePeriod):
		funcRef = "RubiksCube .init"
		#  Manual init function

		self .cubeCount = cubeCount
		self .cubeLength = cubeLength
		self .cubeSpacingModifier = int (self .cubeLength * userCubeSpacing)

		self .xPos = xPos - int (cubeLength * cubeCount / 2)
		self .yPos = yPos - int (cubeLength * cubeCount / 2)
		self .zPos = zPos - int (cubeLength * cubeCount / 2)

		self .updatePeriod = updatePeriod

		self .generateSideMatrix ()
		self .generateVisualCube ()
		if showMatricesWindow == 1:
			self .buildMatricesViewer ()

		log (funcRef, "Generated %d faces." % theRubiksCube .getFaceCount ())
		return


	##  Matrix Viewer

	def buildMatricesViewer (self):
		funcRef = "RubiksCube .buildMatricesViewer"
		#  Function to build the matrix viewing window

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

		#  Position the window
		root .geometry ("+%d+%d" % (root .winfo_screenwidth () - root .winfo_width (), 0))

		return

	def bMVGFL (self, row, column, text):
		funcRef = "RubiksCube .bMVGFL"
		#  build Matrix Viewer Generate Face Label

		newLabel = tk .Label (root, text = text)
		newLabel .grid (row = row, column = column)
		self .matricesViewerData .append (newLabel)
		return

	def matricesViewerUpdate (self):
		funcRef = "RubiksCube .matricesViewerUpdate"
		for i in range (6):
			 self .matricesViewerData [i]['text'] = self .getASide2D (i)
		root .update ()
		return


	##  Overall Cube Generation

	def generateSideMatrix (self):
		funcRef = "RubiksCube .generateSideMatrix"
		#  Generates a matrix of matrices of matrices to hold the cube's faces and
		#  face-statuses

		#  Generate each side
		for currSide in range (6):
			self .sideMatrix .append ([])

			for j in range (self .cubeCount):
				self .sideMatrix [currSide] .append ([])

				for k in range (self .cubeCount):
					self .sideMatrix [currSide][j] .append (currSide)


	def generateVisualCube (self):
		funcRef = "RubiksCube .generateVisualCube"
		#  Generates a matrix of matrices of matrices to hold the cube's visual info

		for currSide in range (6):
			self .visualMatrix .append ([])

			for j in range (self .cubeCount):
				self .visualMatrix [currSide] .append ([])

				for k in range (self .cubeCount):
					self .visualMatrix [currSide][j] .append (self .generateAFace (currSide, j, k))


	#  Returns the cube-side-face-matrix (not the visual one)
	def getTheSides (self):
		funcRef = "RubiksCube .getTheSides"
		return self .sideMatrix

	def getASide (self, theSide):
		funcRef = "RubiksCube .getASide"
		return self .sideMatrix [theSide]

	def getASide2D (self, theSide):
		funcRef = "RubiksCube .getASide2D"
		#  Flatten out a side matrix into a text-based 2D representative (or tuple of texts)
		the2DSide = ""
		#  Unwrap each sub-matrix
		#  Note that to get an "as taught in school" grid, we need to mess with
		#  the unwrapping a bit...
		for y in range (self .cubeCount - 1, -1, -1):
			for x in range (self .cubeCount):
				the2DSide += str (self .sideMatrix [theSide][x][y])
			the2DSide += "\n"
		return the2DSide


	##  Face Functions

	def generateAFace (self, theFace, index1, index2):
		funcRef = "RubiksCube .generateAFace"
		#  Generates a single visual face, in the correct orientation

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

	#  Returns a specific face from that matrix
	def getAFace (self, theFace, theXIndex, theYIndex):
		funcRef = "RubiksCube .getAFace"
		return self .sideMatrix [theFace][theXIndex][theYIndex]

	#  Returns the number of faces currentlly stored in the cube-matrix
	def getFaceCount (self):
		funcRef = "RubiksCube .getFaceCount"
		#  Sum up the number of stored cubes by unwrapping the sideMatrix list
		theCount = 0
		for level1 in self .sideMatrix:
			for level2 in level1:
				for level3 in level2:
					theCount += 1
		return theCount


	##  Rotation Functions

	def rotateAFace (self, theFace, direction, segDepth):
		funcRef = "RubiksCube .rotateAFace"
		#  Function to rotate a face CW or CCW
		#  Need to ensure we don't rotate the whole cube
		#  Either that, or also rotate the back face, but why bother?

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

		#  Handle the segments
		#  Iterate through each layer
		for currDepth in range (segDepth + 1):
			self .rotateASegment (theFace, direction, currDepth)

		#  Log the rotation and foxtrott oscar
		self .recordMove (theFace, direction, segDepth)
		return

	def rotateASegment (self, theFace, direction, currDepth):
		funcRef = "RubiksCube .rotateASegment"
		#  Function to rotate a single segment, either clockwise or anti-clockwise.
		#  This is the sort of thing a compiled language would be great for.

		#  Firstly, store the first segment, so it can be overwritten
		tempSegment = self .getSingleSegment (sideNeighbours [theFace][0][0], sideNeighbours [theFace][0][1], currDepth)

		#  Determine direction of rotation / copy
		if direction == 0:
			#  Next, copy each segment round one direction
			self .setSingleSegment (sideNeighbours [theFace][0][0], sideNeighbours [theFace][0][1], currDepth,
				self .getSingleSegment (sideNeighbours [theFace][3][0], sideNeighbours [theFace][3][1], currDepth))

			self .setSingleSegment (sideNeighbours [theFace][3][0], sideNeighbours [theFace][3][1], currDepth,
				self .getSingleSegment (sideNeighbours [theFace][2][0], sideNeighbours [theFace][2][1], currDepth))

			self .setSingleSegment (sideNeighbours [theFace][2][0], sideNeighbours [theFace][2][1], currDepth,
				self .getSingleSegment (sideNeighbours [theFace][1][0], sideNeighbours [theFace][1][1], currDepth))

			#  Lastly, copy the stored segment to the last position
			self .setSingleSegment (sideNeighbours [theFace][1][0], sideNeighbours [theFace][1][1], currDepth, tempSegment)

		elif direction == 1:
			self .setSingleSegment (sideNeighbours [theFace][0][0], sideNeighbours [theFace][0][1], currDepth,
				self .getSingleSegment (sideNeighbours [theFace][1][0], sideNeighbours [theFace][1][1], currDepth))

			self .setSingleSegment (sideNeighbours [theFace][1][0], sideNeighbours [theFace][1][1], currDepth,
				self .getSingleSegment (sideNeighbours [theFace][2][0], sideNeighbours [theFace][2][1], currDepth))

			self .setSingleSegment (sideNeighbours [theFace][2][0], sideNeighbours [theFace][2][1], currDepth,
				self .getSingleSegment (sideNeighbours [theFace][3][0], sideNeighbours [theFace][3][1], currDepth))

			self .setSingleSegment (sideNeighbours [theFace][3][0], sideNeighbours [theFace][3][1], currDepth, tempSegment)
		return

	def getSingleSegment (self, face, extremity, depthNear):
		funcRef = "RubiksCube .getSingleSegment"
		#  Gets a single segment from a face, given the face and which side to get it from
		depthFar = self .cubeCount - depthNear - 1
		theSegment = []
		if extremity == 0:
			for i in range (self .cubeCount):
				theSegment .append (self .sideMatrix [face][i][depthNear])
		elif extremity == 1:
			for i in range (self .cubeCount):
				theSegment .append (self .sideMatrix [face][depthNear][i])
		elif extremity == 2:
			for i in range (self .cubeCount):
				theSegment .append (self .sideMatrix [face][i][depthFar])
		elif extremity == 3:
			for i in range (self .cubeCount):
				theSegment .append (self .sideMatrix [face][depthFar][i])
		return theSegment

	def setSingleSegment (self, face, extremity, depthNear, theSegment):
		funcRef = "RubiksCube .setSingleSegment"
		#  Writes a single segment to a face, given the position of said segment

		if extremity > 3:
			die (funcRef, "`extremity` out of range.")
		if face > 6:
			die (funcRef, "`face` out of range.")
		if depthNear >= self .cubeCount:
			die (funcRef, "`depthNear` out of range.")

		depthFar = self .cubeCount - depthNear - 1
		if extremity == 0:
			for i in range (self .cubeCount):
				self .sideMatrix [face][i][depthNear] = theSegment [i]
				self .visualMatrix [face][i][depthNear] .setFaceColour (theSegment [i])
		elif extremity == 1:
			for i in range (self .cubeCount):
				self .sideMatrix [face][depthNear][i] = theSegment [i]
				self .visualMatrix [face][depthNear][i] .setFaceColour (theSegment [i])
		elif extremity == 2:
			for i in range (self .cubeCount):
				self .sideMatrix [face][i][depthFar] = theSegment [i]
				self .visualMatrix [face][i][depthFar] .setFaceColour (theSegment [i])
		elif extremity == 3:
			for i in range (self .cubeCount):
				self .sideMatrix [face][depthFar][i] = theSegment [i]
				self .visualMatrix [face][depthFar][i] .setFaceColour (theSegment [i])
		return



	##  Algorithms

	def recordMove (self, theFace, theDirection, theDepth):
		funcRef = "RubiksCube .recordMove"
		#  Records a given move

		if theDirection == 0:
			log (funcRef, "F %d;  CW ;  D %d" % (theFace, theDepth))
		elif theDirection == 1:
			log (funcRef, "F %d;  CCW;  D %d" % (theFace, theDepth))
		else:
			die ("RubiksCube .recordMove", "`theDirection` out of bounds.")

	def shuffle (self):
		funcRef = "RubiksCube .shuffle"
		#  Function to shuffle the cube, for as long as set in preferences.py
		log (funcRef, "Shuffling the cube...")

		#  Set up the random generator
		random .seed ()

		maxDepth = self .cubeCount - 1
		for i in range (cubeShuffleAmount):
		#while True:
			sleep (self .updatePeriod)

			#  Random variables:  Face, Direction, Depth
			self .rotateAFace (random .randrange (6), random .randrange (2), random .randrange (maxDepth))

		log (funcRef, "Shuffling complete!")
		return



theRubiksCube = RubiksCube ()
