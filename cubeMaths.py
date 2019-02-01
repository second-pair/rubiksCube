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
# import inspect
# print(inspect.stack()[1].function)
# print(inspect.stack()[1][3])

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
#  Second value (first sub-tuple pair) is a neighbouring face and the closest
#  of its sides, out of x-close, y-close, x-far, y-far
#  This is in the same order as the x-close etc order
#  Third value pair is the next clockwise face and etc.
#  This garbage make a bit more sense if you stare at the Matrices Viewer
sideNeighbours = {
0: ((1, 2), (4, 0), (3, 0), (2, 0)),
1: ((5, 2), (4, 1), (0, 0), (2, 3)),
2: ((0, 3), (3, 3), (5, 3), (1, 3)),
3: ((0, 2), (4, 3), (5, 0), (2, 1)),
4: ((0, 1), (1, 1), (5, 1), (3, 1)),
5: ((3, 2), (4, 2), (1, 0), (2, 2)),
}
#  Need to make everything work with this later on
sideNeighboursTemp = {
0: {1: 2, 4: 0, 3: 0, 2: 0},
1: {5: 2, 4: 1, 0: 0, 2: 3},
2: {0: 3, 3: 3, 5: 3, 1: 3},
3: {0: 2, 4: 3, 5: 0, 2: 1},
4: {0: 1, 1: 1, 5: 1, 3: 1},
5: {3: 2, 4: 2, 1: 0, 2: 2},
}
#  This one will give you the face that borders a given face
#  First value is the face you're looking at
#  Second value (dictionary) gives the relevant face that borders the
#  keyed neighbour
sideNeighboursReverse = {
0: {1: 2, 4: 0, 3: 0, 2: 0},
1: {5: 2, 4: 1, 0: 0, 2: 3},
2: {0: 3, 3: 3, 5: 3, 1: 3},
3: {0: 2, 4: 3, 5: 0, 2: 1},
4: {0: 1, 1: 1, 5: 1, 3: 1},
5: {3: 2, 4: 2, 1: 0, 2: 2},
}
sideOpposites = {
0: 5,
1: 3,
2: 4,
3: 1,
4: 2,
5: 0,
}
turnDiffs = {
0: (0, 1, 2, -1),
1: (-1, 0, 1, 2),
2: (2, -1, 0, 1),
3: (1, 2, -1, 0),
}
#  0 -> bottom
#  1 -> back
#  2 -> right
#  3 -> front
#  4 -> left
#  5 -> top
#
#  0 -> x-close
#  1 -> y-close
#  2 -> x-far
#  3 -> y-far



class RubiksCube:
	def __init__ (self):
		#  Maybe these want to be classes one day?
		self .sideMatrix = []
		self .visualMatrix = []
		self .matricesViewerData = []

	def init (self, cubeCount = userCubeSize, cubeLength = userCubeLength, xPos = 0, yPos = 0, zPos = 0, updatePeriod = userAlgoMovePeriod):
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

		self .recordMoves = open  ("lastMoves.txt", "w")

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
		#  Generates a matrix of matrices of matrices to hold the cube's faces
		#  and face-statuses

		#  Generate each side
		for currSide in range (6):
			self .sideMatrix .append ([])

			for j in range (self .cubeCount):
				self .sideMatrix [currSide] .append ([])

				for k in range (self .cubeCount):
					self .sideMatrix [currSide][j] .append (currSide)


	def generateVisualCube (self):
		funcRef = "RubiksCube .generateVisualCube"
		#  Generates a matrix of matrices of matrices to hold the cube's
		#  visual info

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
		#  Flatten out a side matrix into a text-based 2D representative
		#  (or tuple of texts)
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

	def rotateASide (self, theSide, direction, segDepth):
		funcRef = "RubiksCube .rotateASide"
		#  Function to rotate a face CW or CCW
		#  Need to ensure we don't rotate beyond half-way, since this'll
		#  break the cube-solving logic (the faces are basically hard-coded).
		if segDepth >= self .cubeCount // 2:
			die (funcRef, "Trying to rotate beyond half-way point (`segDepth` = %d)" % segDepth)

		sleep (self .updatePeriod)

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
				tempColour = self .sideMatrix [theSide][currX][currY]
				#  Save that colour to the side and visual matrices
				tempSide [newY][newX] = tempColour
				self .visualMatrix [theSide][newY][newX] .setFaceColour (tempColour)

				currX += 1
				newX += newXStep
			currY += 1
			newY += newYStep

		#  Assign the temporary side to the sideMatrix
		self .sideMatrix [theSide] = tempSide

		#  Handle the segments
		#  Iterate through each layer
		for currDepth in range (segDepth + 1):
			self .rotateASegment (theSide, direction, currDepth)

		#  Log the rotation and foxtrott oscar
		self .recordMove (theSide, direction, segDepth)
		return

	def rotateASegment (self, theSide, direction, currDepth):
		funcRef = "RubiksCube .rotateASegment"
		#  Function to rotate a single segment, either clockwise or
		#  anti-clockwise.
		#  This is the sort of thing a compiled language would be great for.

		#  Firstly, store the first segment, so it can be overwritten
		tempSegment = self .getSingleSegment (sideNeighbours [theSide][0][0], sideNeighbours [theSide][0][1], currDepth)

		#  Determine direction of rotation / copy
		if direction == 0:
			#  Next, copy each segment round one direction
			self .setSingleSegment (sideNeighbours [theSide][0][0], sideNeighbours [theSide][0][1], currDepth,
				self .getSingleSegment (sideNeighbours [theSide][3][0], sideNeighbours [theSide][3][1], currDepth))

			self .setSingleSegment (sideNeighbours [theSide][3][0], sideNeighbours [theSide][3][1], currDepth,
				self .getSingleSegment (sideNeighbours [theSide][2][0], sideNeighbours [theSide][2][1], currDepth))

			self .setSingleSegment (sideNeighbours [theSide][2][0], sideNeighbours [theSide][2][1], currDepth,
				self .getSingleSegment (sideNeighbours [theSide][1][0], sideNeighbours [theSide][1][1], currDepth))

			#  Lastly, copy the stored segment to the last position
			self .setSingleSegment (sideNeighbours [theSide][1][0], sideNeighbours [theSide][1][1], currDepth, tempSegment)

		elif direction == 1:
			self .setSingleSegment (sideNeighbours [theSide][0][0], sideNeighbours [theSide][0][1], currDepth,
				self .getSingleSegment (sideNeighbours [theSide][1][0], sideNeighbours [theSide][1][1], currDepth))

			self .setSingleSegment (sideNeighbours [theSide][1][0], sideNeighbours [theSide][1][1], currDepth,
				self .getSingleSegment (sideNeighbours [theSide][2][0], sideNeighbours [theSide][2][1], currDepth))

			self .setSingleSegment (sideNeighbours [theSide][2][0], sideNeighbours [theSide][2][1], currDepth,
				self .getSingleSegment (sideNeighbours [theSide][3][0], sideNeighbours [theSide][3][1], currDepth))

			self .setSingleSegment (sideNeighbours [theSide][3][0], sideNeighbours [theSide][3][1], currDepth, tempSegment)
		return

	def getSingleSegment (self, side, extremity, depthNear):
		funcRef = "RubiksCube .getSingleSegment"
		#  Gets a single segment from a side, given the side and which edge to
		#  get it from

		#  Work out which edge of the side we're looking at
		if extremity == 0 or extremity == 1:
			theDepth = depthNear
		else:
			theDepth = self .cubeCount - depthNear - 1

		theSegment = []
		if extremity == 0 or extremity == 2:
			for i in range (self .cubeCount):
				theSegment .append (self .sideMatrix [side][i][theDepth])
		elif extremity == 1 or extremity == 3:
			for i in range (self .cubeCount):
				theSegment .append (self .sideMatrix [side][theDepth][i])
		return theSegment

	def setSingleSegment (self, side, extremity, depthNear, theSegment):
		funcRef = "RubiksCube .setSingleSegment"
		#  Writes a single segment to a side, given the position of
		#  said segment

		# #  Error checking
		# if extremity > 3:
		# 	die (funcRef, "`extremity` out of range.")
		# if side > 6:
		# 	die (funcRef, "`side` out of range.")
		# if depthNear >= self .cubeCount:
		# 	die (funcRef, "`depthNear` out of range.")

		#  Work out which side of the side we're looking at
		if extremity == 0 or extremity == 1:
			theDepth = depthNear
		else:
			theDepth = self .cubeCount - depthNear - 1

		if extremity == 0 or extremity == 2:
			for i in range (self .cubeCount):
				self .sideMatrix [side][i][theDepth] = theSegment [i]
				self .visualMatrix [side][i][theDepth] .setFaceColour (theSegment [i])
		elif extremity == 1 or extremity == 3:
			for i in range (self .cubeCount):
				self .sideMatrix [side][theDepth][i] = theSegment [i]
				self .visualMatrix [side][theDepth][i] .setFaceColour (theSegment [i])
		return

	def extremityToCoords (self, extremity):
		funcRef = "RubiksCube .extremityToCoords"
		#  Converts an extremity reference to an x-y coordinate tuple.
		#  0 -> x-close
		#  1 -> y-close
		#  2 -> x-far
		#  3 -> y-far
		if extremity == 0:
			return (1, 0)
		elif extremity == 1:
			return (0, 1)
		elif extremity == 2:
			return (1, self .cubeCount - 1)
		elif extremity == 3:
			return (self .cubeCount - 1, 1)
		else:
			die (funcRef, "extremity out of range")

	def recordMove (self, theSide, theDirection, theDepth):
		funcRef = "RubiksCube .recordMove"
		#  Records a given move

		self .recordMoves .write ("(%s,%s,%s),\n" % (theSide, theDirection, theDepth))
		if theDirection == 0:
			log (funcRef, "F %d;  CW ;  D %d" % (theSide, theDepth))
		elif theDirection == 1:
			log (funcRef, "F %d;  CCW;  D %d" % (theSide, theDepth))
		else:
			die ("RubiksCube .recordMove", "`theDirection` out of bounds.")

	def replayMoves (self, theMoves):
		for currMove in theMoves:
			self .rotateASide (currMove [0], currMove [1], currMove [2])


	##  Algorithms
	#  We'll need a different algo for 2x2

	def shuffle (self, shuffleAmount = cubeShuffleAmount):
		funcRef = "RubiksCube .shuffle"
		#  Function to shuffle the cube, for as long as set in preferences.py
		log (funcRef, "Shuffling the cube...")

		#  Set up the random generator
		random .seed ()

		maxDepth = self .cubeCount // 2
		for i in range (shuffleAmount):
		#while True:
			#  Random variables:  Face, Direction, Depth
			self .rotateASide (random .randrange (6), random .randrange (2), random .randrange (maxDepth))

		log (funcRef, "Shuffling complete!")
		return

	def algoCornerSwap (self):
		funcRef = "RubiksCube .algoCornerSwap"
		return

	def algoFaceCentre (self):
		funcRef = "RubiksCube .algoFaceCentre"
		return
	def algoFaceEdges (self):
		funcRef = "RubiksCube .algoFaceEdges"
		return

	def algoFace1Cross (self, theSide = userAlgoStartingSide):
		funcRef = "RubiksCube .algoFace1Cross"
		#  Tries to solve the cross on the starting face
		#  This assunes the cube has already been sorted into a 3x3
		log (funcRef, "Starting algorithm.")

		oopResult = 0
		topSide = sideOpposites [theSide]

		for extremity in range (4):
			if self .algoCheckEdge (theSide, extremity) == False:
				oopResult += 1

				#  Need to find that edge
				foundSide, neighbourSide, neighbourEdge, targetSide = self .algoFindEdge (theSide, extremity)

				#  Calculate other necessary variables
				while neighbourSide == theSide or neighbourSide == topSide:
					debug (funcRef, "Rotating edge to centre of found face")
					self .rotateASide (foundSide, 0, 0)
					foundSide, neighbourSide, neighbourEdge, targetSide = self .algoFindEdge (theSide, extremity)

				topEdgeStart = sideNeighboursTemp [neighbourSide][topSide]
				topEdgeDest = sideNeighboursTemp [targetSide][topSide]
				neighbourEdgeTop = sideNeighboursTemp [topSide][neighbourSide]

				#  Turn the edge so the face is on the top side
				#  Need to check if the face is adjacent, but not at, the starting side

				debug (funcRef, "Turning target edge to top side")
				undoTurns = self .algoTurnDiff (neighbourSide, neighbourEdge, neighbourEdgeTop)

				#  Rotate so the edge is over the correct face
				debug (funcRef, "Turning target edge to above destination")
				self .algoTurnDiff (topSide, topEdgeStart, topEdgeDest)

				#  Undo previous turns to keep pre-solved cross-edges
				#  in place
				debug (funcRef, "Undoing damage to existing cross")
				if neighbourSide != targetSide:
					if undoTurns == -1:
						self .rotateASide (neighbourSide, 0, 0)
					elif undoTurns == 1:
						self .rotateASide (neighbourSide, 1, 0)
					elif undoTurns == 2:
						self .rotateASide (neighbourSide, 1, 0)
						self .rotateASide (neighbourSide, 1, 0)

				#  Flip back down
				debug (funcRef, "Rotating target edge into destination")
				self .rotateASide (targetSide, 0, 0)
				self .rotateASide (targetSide, 0, 0)
		log (funcRef, "Algorithm complete.")
		return oopResult

	def algoFace1Corners (self, theSide = userAlgoStartingSide):
		funcRef = "RubiksCube .algoFace1Corners"
		#  You next!
		return

	def algoTurnDiff (self, theSide, startEdge, destEdge):
		funcRef = "RubiksCube .algoTurnDiff"
		#  Function to turn an edge on a given side to a specified destination
		#  Calculate direction of turn
		turnAmount = turnDiffs [startEdge][destEdge]
		if turnAmount == -1:
			#  Rotate CCW
			debug (funcRef, "Turning CCW *1")
			self .rotateASide (theSide, 1, 0)
			undoTurns = -1
		elif turnAmount == 1:
			#  Rotate CW
			debug (funcRef, "Turning CW  *1")
			self .rotateASide (theSide, 0, 0)
			undoTurns = 1
		elif turnAmount == 2:
			#  Rotate twice
			debug (funcRef, "Turning CW  *2")
			self .rotateASide (theSide, 0, 0)
			self .rotateASide (theSide, 0, 0)
			undoTurns = 2
		elif turnAmount != 0:
			die (funcRef, "Bad amount to turn (`edgeDiff`)")
		else:
			debug (funcRef, "Not turning")
		return turnAmount

	def algoCheckEdge (self, theSide, extremity):
		funcRef = "RubiksCube .algoCheckEdge"
		#  Checks if a given edge is in the correct place

		#  Get some useful co-ordinates
		xCoord, yCoord = self .extremityToCoords (extremity)

		if self .sideMatrix [theSide][xCoord][yCoord] != theSide:
			debug (funcRef, "Edge [%d][%d][%d] out of place" % (theSide, xCoord, yCoord))
			return False
		else:
			#  Get the neighbouring face
			neighbourSide = sideNeighbours [theSide][extremity][0]
			xCoordNeighbour, yCoordNeighbour = self .extremityToCoords (sideNeighbours [theSide][extremity][1])

			if neighbourSide != self .sideMatrix [neighbourSide][xCoordNeighbour][yCoordNeighbour]:
				debug (funcRef, "Edge [%d][%d][%d] out of place due to [%d][%d][%d]" % (theSide, xCoord, yCoord, neighbourSide, xCoordNeighbour, yCoordNeighbour))
				return False
			else:
				debug (funcRef, "Edge [%d][%d][%d] correct" % (theSide, xCoord, yCoord))
				return True

	def algoFindEdge (self, targetSide, extremity):
		funcRef = "RubiksCube .algoFindEdge"
		#  Checks if a given edge is in the correct place

		#  Calculate where we're trying to match against
		targetNeighbour = sideNeighbours [targetSide][extremity][0]

		#  Loop throuugh each edge and see if that's our boy
		for currSide in range (6):
			for currEdge in range (4):
				#  Get current edge co-ordinates
				xCoord, yCoord = self .extremityToCoords (currEdge)
				if self .sideMatrix [currSide][xCoord][yCoord] == targetSide:
					#  Get the complimenting face
					#  We essentially lookup the bordering side, loopup
					#  the relevant face, get co-ords for that edge, then read
					#  its value so we can compare it to `targetNeighbour`
					neighbourSide = sideNeighbours [currSide][currEdge]
					xCoordNeighbour, yCoordNeighbour = self .extremityToCoords (neighbourSide [1])

					if self .sideMatrix [neighbourSide [0]][xCoordNeighbour][yCoordNeighbour] == targetNeighbour:
						#  Return the relevant side & extremity, printing
						#  this and the complement face position too
						debug (funcRef, "Found edge at [%d][%d][%d] + [%d][%d][%d]" % (currSide, xCoord, yCoord, neighbourSide [0], xCoordNeighbour, yCoordNeighbour))
						return (currSide, neighbourSide [0], neighbourSide [1], targetNeighbour)
					else:
						debug (funcRef, "Edge [%d][%d][%d]:  Complement edge [%d][%d][%d] incorrect" % (currSide, xCoord, yCoord, neighbourSide [0], xCoordNeighbour, yCoordNeighbour))

				else:
					debug (funcRef, "Edge [%d][%d][%d] not relevant" % (currSide, xCoord, yCoord))

		#  Couldn't find it!
		die (funcRef, "Couldn't find edge %d -> %d" % (targetSide, extremity))

	def algoCheckCorner (self, theSide, extremity1, extremity2):
		funcRef = "RubiksCube .algoCheckCorner"
		#
		return

	def algoFindCorner (self, targetSide, extremity1, extremity2):
		funcRef = "RubiksCube .algoFindCorner"
		#
		return



	##  Execution Function(s)

	def solve (self):
		#  Perform an initial shuffle
		self .shuffle (100)
		#self .replayMoves (lastMoves)
		#self .rotateASide (3, 0, 0)

		#  Show off a bit
		sleep (0.5)

		#  Get everything looking like a 3x3
		self .algoFaceCentre ()
		self .algoFaceEdges ()

		#  Solve the first face
		while self .algoFace1Cross (3) > 0:
			pass
		self .algoFace1Corners (3)

		return



theRubiksCube = RubiksCube ()


lastMoves = (
(5,1,0),
(4,1,0),
(0,1,0),
(3,1,0),
(5,0,0),
(2,1,0),
(1,1,0),
(2,0,0),
(3,1,0),
(4,0,0),
(3,1,0),
(5,0,0),
(3,0,0),
(1,0,0),
(2,0,0),
(5,0,0),
(5,0,0),
(5,1,0),
(2,1,0),
(5,0,0),
(1,1,0),
(1,0,0),
(4,0,0),
(2,1,0),
(5,0,0),
(5,1,0),
(3,0,0),
(0,1,0),
(0,0,0),
(2,1,0),
(1,0,0),
(5,1,0),
(3,1,0),
(3,1,0),
(1,0,0),
(4,1,0),
(0,0,0),
(4,1,0),
(2,1,0),
(4,1,0),
(3,1,0),
(0,0,0),
(1,0,0),
(3,1,0),
(1,0,0),
(2,1,0),
(1,1,0),
(4,0,0),
(5,0,0),
(0,0,0),
(0,0,0),
(3,1,0),
(1,1,0),
(0,1,0),
(4,1,0),
(3,0,0),
(0,0,0),
(5,1,0),
(3,0,0),
(5,0,0),
(5,1,0),
(3,1,0),
(0,0,0),
(3,1,0),
(3,1,0),
(3,0,0),
(3,1,0),
(3,0,0),
(0,0,0),
(3,0,0),
(3,1,0),
(3,0,0),
(5,0,0),
(4,0,0),
(1,1,0),
(0,0,0),
(1,0,0),
(4,0,0),
(0,0,0),
(4,1,0),
(4,1,0),
(5,0,0),
(1,1,0),
(3,0,0),
(0,1,0),
(3,1,0),
(1,1,0),
(3,0,0),
(1,1,0),
(3,0,0),
(5,1,0),
(3,0,0),
(4,1,0),
(5,1,0),
(2,0,0),
(5,1,0),
(2,0,0),
(1,0,0),
(5,1,0),
(0,0,0),
)
