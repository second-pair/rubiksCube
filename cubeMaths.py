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

#  Do we want to use one of these?  https://docs.python.org/3/library/collections.html#collections.OrderedDict
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
#  LUT for corner-extremity pairs
cornerExtremities = ((0, 1), (1, 2), (2, 3), (3, 0))
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

		log ("Generated %d faces." % theRubiksCube .getFaceCount ())
		return


	##  Matrix Viewer

	def buildMatricesViewer (self):
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
		#  build Matrix Viewer Generate Face Label

		newLabel = tk .Label (root, text = text)
		newLabel .grid (row = row, column = column)
		self .matricesViewerData .append (newLabel)
		return

	def matricesViewerUpdate (self):
		for i in range (6):
			 self .matricesViewerData [i]['text'] = self .getASide2D (i)
		root .update ()
		return


	##  Overall Cube Generation

	def generateSideMatrix (self):
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
		return self .sideMatrix

	def getASide (self, theSide):
		return self .sideMatrix [theSide]

	def getASide2D (self, theSide):
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


	##  Rotation Functions

	def rotateASide (self, theSide, direction, segDepth):
		#  Function to rotate a face CW or CCW
		#  Need to ensure we don't rotate with depth beyond half-way, since
		#  this'll break the cube-solving logic (the faces are basically
		#  hard-coded to always be in the same places).
		#*
		if segDepth >= self .cubeCount // 2:
			die ("Trying to rotate beyond half-way point (`segDepth` = %d)" % segDepth)

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
		#  Function to rotate a single segment, either clockwise or
		#  anti-clockwise.
		#  This is the sort of thing a compiled language would be great for.
		#*!  Definitely a problem

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

		else:
			die ("`direction` wasn't 1 or 2")
		return

	def getSingleSegment (self, side, extremity, depthNear):
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
		print (theSegment)
		return theSegment

	def setSingleSegment (self, side, extremity, depthNear, theSegment):
		#  Writes a single segment to a side, given the position of
		#  said segment
		#*

		# #  Error checking
		# if extremity > 3:
		# 	die ("`extremity` out of range.")
		# if side > 6:
		# 	die ("`side` out of range.")
		# if depthNear >= self .cubeCount:
		# 	die ("`depthNear` out of range.")

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

	def edgeExtremityToCoords (self, extremity):
		#  Converts an extremity reference to x-y co-ordinates tuple.
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
			die ("extremity out of range")

	def cornerExtremityToCoords (self, extremity1, extremity2):
		#  Converts an extremity pair into x-y co-ordinates
		if extremity1 == extremity2:
			die ("Both extremities were the same!")
		if extremity1 == 1 or extremity2 == 1:
			xCoord = 0
		elif extremity1 == 3 or extremity2 == 3:
			xCoord = self .cubeCount - 1
		else:
			die ("x-extremity out of range")
		if extremity1 == 0 or extremity2 == 0:
			yCoord = 0
		elif extremity1 == 2 or extremity2 == 2:
			yCoord = self .cubeCount - 1
		else:
			die ("y-extremity out of range")
		return (xCoord, yCoord)

	def recordMove (self, theSide, theDirection, theDepth):
		#  Records a given move

		self .recordMoves .write ("(%s,%s,%s),\n" % (theSide, theDirection, theDepth))
		if theDirection == 0:
			log ("F %d;  CW ;  D %d" % (theSide, theDepth))
		elif theDirection == 1:
			log ("F %d;  CCW;  D %d" % (theSide, theDepth))
		else:
			die ("RubiksCube .recordMove", "`theDirection` out of bounds.")

	def replayMoves (self, theMoves):
		for currMove in theMoves:
			self .rotateASide (currMove [0], currMove [1], currMove [2])


	##  Algorithms
	#  We'll need a different algo for 2x2

	def shuffle (self, shuffleAmount = cubeShuffleAmount):
		#  Function to shuffle the cube, for as long as set in preferences.py
		log ("Shuffling the cube...")

		#  Set up the random generator
		random .seed ()

		maxDepth = self .cubeCount // 2
		for i in range (shuffleAmount):
		#while True:
			#  Random variables:  Face, Direction, Depth
			self .rotateASide (random .randrange (6), random .randrange (2), random .randrange (maxDepth))

		log ("Shuffling complete!")
		return

	def algoTurnDiff (self, theSide, startEdge, destEdge):
		#  Function to turn an edge on a given side to a specified destination
		#  Calculate direction of turn
		turnAmount = turnDiffs [startEdge][destEdge]
		if turnAmount == -1:
			#  Rotate CCW
			debug ("Turning CCW *1")
			self .rotateASide (theSide, 1, 0)
			undoTurns = -1
		elif turnAmount == 1:
			#  Rotate CW
			debug ("Turning CW  *1")
			self .rotateASide (theSide, 0, 0)
			undoTurns = 1
		elif turnAmount == 2:
			#  Rotate twice
			debug ("Turning CW  *2")
			self .rotateASide (theSide, 0, 0)
			self .rotateASide (theSide, 0, 0)
			undoTurns = 2
		elif turnAmount != 0:
			die ("Bad amount to turn (`edgeDiff`)")
		else:
			debug ("Not turning")
		return turnAmount

	def algoCornerSwap (self):
		return

	def algoFaceCentre (self):
		return
	def algoFaceEdges (self):
		return

	def algoFace1Cross (self, theSide = userAlgoStartingSide):
		#  Tries to solve the cross on the starting face
		#  This assunes the cube has already been sorted into a 3x3
		log ("Starting algorithm.")

		oopResult = 0
		topSide = sideOpposites [theSide]

		for extremity in range (4):
			if self .algoCheckEdge (theSide, extremity) == False:
				oopResult += 1

				#  Need to find that edge
				foundSide, neighbourSide, neighbourEdge, targetSide = self .algoFindEdge (theSide, extremity)

				#  Calculate other necessary variables
				while neighbourSide == theSide or neighbourSide == topSide:
					debug ("Rotating edge to centre of found face")
					self .rotateASide (foundSide, 0, 0)
					foundSide, neighbourSide, neighbourEdge, targetSide = self .algoFindEdge (theSide, extremity)
				input ("...")

				topEdgeStart = sideNeighboursReverse [neighbourSide][topSide]
				topEdgeDest = sideNeighboursReverse [targetSide][topSide]
				neighbourEdgeTop = sideNeighboursReverse [topSide][neighbourSide]

				#  Turn the edge so the face is on the top side
				#  Need to check if the face is adjacent, but not at, the starting side

				debug ("Turning target edge to top side")
				undoTurns = self .algoTurnDiff (neighbourSide, neighbourEdge, neighbourEdgeTop)
				input ("...")

				#  Rotate so the edge is over the correct face
				debug ("Turning target edge to above destination")
				self .algoTurnDiff (topSide, topEdgeStart, topEdgeDest)
				input ("...")

				#  Undo previous turns to keep pre-solved cross-edges
				#  in place
				debug ("Undoing damage to existing cross")
				if neighbourSide != targetSide:
					if undoTurns == -1:
						self .rotateASide (neighbourSide, 0, 0)
					elif undoTurns == 1:
						self .rotateASide (neighbourSide, 1, 0)
					elif undoTurns == 2:
						self .rotateASide (neighbourSide, 1, 0)
						self .rotateASide (neighbourSide, 1, 0)
				input ("...")

				#  Flip back down
				#*
				debug ("Rotating target edge into destination")
				self .rotateASide (targetSide, 1, 0)
				self .rotateASide (targetSide, 1, 0)
				input ("...")

		log ("Algorithm complete.")
		return oopResult

	def algoFace1Corners (self, theSide = userAlgoStartingSide):
		#  Tries to solve the cornerson the starting face
		#  This should ideally be run after `algoFace1Cross`
		log ("Starting algorithm.")

		oopResult = 0
		topSide = sideOpposites [theSide]

		for extremity1, extremity2 in cornerExtremities:
			if self .algoCheckCorner (theSide, extremity1, extremity2) == False:
				oopResult += 1
				#foundSide, neighbourSide, neighbourEdge, targetSide = self .algoFindEdge (theSide, extremity)
				#foundSide, neighbour1Side, neighbour2Side =
				self .algoFindCorner (theSide, extremity1, extremity2)

		log ("Algorithm complete.")
		return oopResult

	def algoSidesMidEdges(self):
		pass
	def algoTopEdges (self):
		pass
	def algoTopCorners (self):
		pass

	def algoCheckEdge (self, theSide, extremity):
		#  Checks if a given edge is in the correct place

		#  Get some useful co-ordinates
		xCoord, yCoord = self .edgeExtremityToCoords (extremity)

		#  Start checking the corner against the surrounding sides
		if self .sideMatrix [theSide][xCoord][yCoord] != theSide:
			debug ("Edge [%d][%d][%d] out of place" % (theSide, xCoord, yCoord))
			return False
		else:
			#  Get the neighbouring face
			neighbourSide = sideNeighbours [theSide][extremity][0]
			xCoordNeighbour, yCoordNeighbour = self .edgeExtremityToCoords (sideNeighbours [theSide][extremity][1])

			if neighbourSide != self .sideMatrix [neighbourSide][xCoordNeighbour][yCoordNeighbour]:
				debug ("Edge [%d][%d][%d] out of place due to [%d][%d][%d]" % (theSide, xCoord, yCoord, neighbourSide, xCoordNeighbour, yCoordNeighbour))
				return False
			else:
				debug ("Edge [%d][%d][%d] correct" % (theSide, xCoord, yCoord))
				return True

	def algoFindEdge (self, targetSide, extremity):
		#  Finds the location of a given edge
		#  Additionally returns information on the edge's complement face

		#  Calculate where we're trying to match against
		targetNeighbour = sideNeighbours [targetSide][extremity][0]

		#  Loop throuugh each edge and see if that's our boy
		for currSide in range (6):
			for currEdge in range (4):
				#  Get current edge co-ordinates
				xCoord, yCoord = self .edgeExtremityToCoords (currEdge)
				if self .sideMatrix [currSide][xCoord][yCoord] == targetSide:
					#  Get the complimenting face
					#  We essentially lookup the bordering side, lookup
					#  the relevant face, get co-ords for that edge, then read
					#  its value so we can compare it to `targetNeighbour`
					neighbourSide = sideNeighbours [currSide][currEdge]
					xCoordNeighbour, yCoordNeighbour = self .edgeExtremityToCoords (neighbourSide [1])

					if self .sideMatrix [neighbourSide [0]][xCoordNeighbour][yCoordNeighbour] == targetNeighbour:
						#  Return the relevant side & extremity, printing
						#  this and the complement face position too
						debug ("Found edge at [%d][%d][%d] + [%d][%d][%d]" % (currSide, xCoord, yCoord, neighbourSide [0], xCoordNeighbour, yCoordNeighbour))
						return (currSide, neighbourSide [0], neighbourSide [1], targetNeighbour)
					else:
						debug ("Edge [%d][%d][%d]:  Complement edge [%d][%d][%d] incorrect" % (currSide, xCoord, yCoord, neighbourSide [0], xCoordNeighbour, yCoordNeighbour))

				else:
					debug ("Edge [%d][%d][%d] not relevant" % (currSide, xCoord, yCoord))

		#  Couldn't find it!
		die ("Couldn't find edge %d -> %d" % (targetSide, extremity))

	def algoCheckCorner (self, theSide, extremity1, extremity2):
		#  Checks if a given corner is in the correct place

		#  Get some useful co-ordinates
		xCoord, yCoord = self .cornerExtremityToCoords (extremity1, extremity2)

		#  Start checking the corner against the surrounding sides
		if self .sideMatrix [theSide][xCoord][yCoord] != theSide:
			debug ("Corner [%d][%d][%d] out of place" % (theSide, xCoord, yCoord))
			return False
		else:
			#  Get the neighbouring face
			neighbourSide1 = sideNeighbours [theSide][extremity1][0]
			neighbourSide2 = sideNeighbours [theSide][extremity2][0]
			xCoordNeighbour1, yCoordNeighbour1 = self .cornerExtremityToCoords (sideNeighboursReverse [theSide][neighbourSide1], sideNeighboursReverse [neighbourSide2][neighbourSide1])
			xCoordNeighbour2, yCoordNeighbour2 = self .cornerExtremityToCoords (sideNeighboursReverse [theSide][neighbourSide2], sideNeighboursReverse [neighbourSide1][neighbourSide2])

			if neighbourSide1 != self .sideMatrix [neighbourSide1][xCoordNeighbour1][yCoordNeighbour1]:
				debug ("Corner [%d][%d][%d] out of place due to [%d][%d][%d]" % (theSide, xCoord, yCoord, neighbourSide1, xCoordNeighbour1, yCoordNeighbour1))
				return False
			elif neighbourSide2 != self .sideMatrix [neighbourSide2][xCoordNeighbour2][yCoordNeighbour2]:
				debug ("Corner [%d][%d][%d] out of place due to [%d][%d][%d]" % (theSide, xCoord, yCoord, neighbourSide2, xCoordNeighbour2, yCoordNeighbour2))
				return False
			else:
				debug ("Edge [%d][%d][%d] correct" % (theSide, xCoord, yCoord))
				return True

	def algoFindCorner (self, targetSide, extremity1, extremity2):
		#  Finds the location of a given corner
		#  Additionally returns information on the corner's complement faces

		#  Calculate where we're trying to match against
		targetNeighbour1 = sideNeighbours [targetSide][extremity1][0]
		targetNeighbour2 = sideNeighbours [targetSide][extremity2][0]

		#  Loop throuugh each edge and see if that's our boy
		for currSide in range (6):
			for currCornerExtremities in cornerExtremities:
				#  Get current corner co-ordinates
				xCoord, yCoord = self .cornerExtremityToCoords (currCornerExtremities [0], currCornerExtremities [1])
				if self .sideMatrix [currSide][xCoord][yCoord] == targetSide:
					#  Get the complimenting faces
					#  We essentially lookup the bordering sides, lookup
					#  the relevant faces, get co-ords for those faces, then
					#  read its value so we can compare it to the
					#  `targetNeighbour`s
					neighbourSide1 = sideNeighbours [currSide][currCornerExtremities [0]]
					neighbourSide2 = sideNeighbours [currSide][currCornerExtremities [1]]
					xCoordNeighbour1, yCoordNeighbour1 = self .edgeExtremityToCoords (neighbourSide1 [1])
					xCoordNeighbour2, yCoordNeighbour2 = self .edgeExtremityToCoords (neighbourSide2 [1])

					neighbourFace1Value = self .sideMatrix [neighbourSide1 [0]][xCoordNeighbour1][yCoordNeighbour1] == targetNeighbour1
					neighbourFace2Value = self .sideMatrix [neighbourSide2 [0]][xCoordNeighbour2][yCoordNeighbour2] == targetNeighbour2

					#  Check if the found edges are some of the ones we're looking for
					if neighbourFace1Value == targetNeighbour1:
						if neighbourFace2Value == targetNeighbour2:
							#  Return the relevant side & extremity, printing
							#  this and the complement face position too
							debug ("Found Corner at [%d][%d][%d] + [%d][%d][%d] + [%d][%d][%d]" % (currSide, xCoord, yCoord, neighbourSide1 [0], xCoordNeighbour1, yCoordNeighbour1, neighbourSide2 [0], xCoordNeighbour2, yCoordNeighbour2))
							return (currSide, neighbourSide1 [0], neighbourSide1 [1], targetNeighbour1, neighbourSide2 [0], neighbourSide2 [1], targetNeighbour2)
						else:
							debug ("Corner [%d][%d][%d]:  Complement face [%d][%d][%d] incorrect" % (currSide, xCoord, yCoord, neighbourSide2 [0], xCoordNeighbour2, yCoordNeighbour2))

					elif neighbourFace1Value == targetNeighbour2:
						if neighbourFace2Value == targetNeighbour1:
							#  Return the relevant side & extremity, printing
							#  this and the complement face position too
							debug ("Found Corner at [%d][%d][%d] + [%d][%d][%d] + [%d][%d][%d]" % (currSide, xCoord, yCoord, neighbourSide1 [0], xCoordNeighbour1, yCoordNeighbour1, neighbourSide2 [0], xCoordNeighbour2, yCoordNeighbour2))
							return (currSide, neighbourSide1 [0], neighbourSide1 [1], targetNeighbour1, neighbourSide2 [0], neighbourSide2 [1], targetNeighbour2)
						else:
							debug ("Corner [%d][%d][%d]:  Complement face [%d][%d][%d] incorrect" % (currSide, xCoord, yCoord, neighbourSide2 [0], xCoordNeighbour2, yCoordNeighbour2))

					else:
						debug ("Corner [%d][%d][%d]:  Complement face [%d][%d][%d] incorrect" % (currSide, xCoord, yCoord, neighbourSide1 [0], xCoordNeighbour1, yCoordNeighbour1))

				else:
					debug ("Corner [%d][%d][%d] not relevant" % (currSide, xCoord, yCoord))

		#  Couldn't find it!
		die ("Couldn't find edge %d -> %d, %d" % (targetSide, extremity1, extremity2))



	##  Execution Function(s)

	def solve (self):
		#  Perform an initial shuffle
		self .shuffle (100)
		return
		#self .replayMoves (lastMoves)
		self .rotateASide (3, 0, 0)

		# for _ in range (4):
		# 	for i in range (6):
		# 		self .rotateASide (i, 0, 0)
		# for _ in range (4):
		# 	for i in range (5, -1, -1):
		# 		self .rotateASide (i, 1, 0)

		#self .rotateASide (2, 0, 0)
		#self .rotateASide (3, 0, 0)
		#self .rotateASide (4, 0, 0)
		#self .rotateASide (5, 0, 0)

		#  Show off a bit
		sleep (userShowoffDuration)

		#  Get everything looking like a 3x3
		self .algoFaceCentre ()
		self .algoFaceEdges ()

		#  Solve the first face
		while self .algoFace1Cross (3) > 0:
			pass

		return
		sleep (userShowoffDuration)
		self .algoFace1Corners (3)
		sleep (userShowoffDuration)
		self .algoSidesMidEdges()
		sleep (userShowoffDuration)
		self .algoTopEdges ()
		sleep (userShowoffDuration)
		self .algoTopCorners ()

		return



theRubiksCube = RubiksCube ()


lastMoves = (
)
