#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  Trying my best to abstract all the primitives info to its own file

import pyglet
from pyglet .gl import *
from pygletHandler import *
from preferences import *



##  Classes
class Cube:
	def __init__ (self, cubeLength, xPos, yPos, zPos):
		self .cubeLength = cubeLength
		self .xPos = xPos - int (cubeLength / 2)
		self .yPos = yPos - int (cubeLength / 2)
		self .zPos = zPos - int (cubeLength / 2)

		self .buildCube ()
		self .setVerticesCount ()

	def getPos (self):
		return (self .xPos, self .yPos, self .zPos)

	def getcubeLength (self):
		return self .cubeLength

	def setVerticesCount (self):
		#  Calculates the number of vertices and stores it
		self .verticesCount = len (self .vertices) // 3

	#  Vertices
	def getVertices (self):
		return self .vertices
	def getVerticesType (self):
		return self .verticesType
	def getVerticesCount (self):
		return self .verticesCount

	#  Colours
	def getColours (self):
		return self .colours
	def getColoursType (self):
		return self .coloursType

	def buildCube (self):
		#  Builds the cube's vertices
		#  This now builds a "unit" model and scales it by the cubeLength
		adjCubeLength = self .cubeLength / 10

		xN = self .xPos
		yN = self .yPos
		zN = self .zPos
		xF = self .xPos + int (adjCubeLength * 10)
		yF = self .yPos + int (adjCubeLength * 10)
		zF = self .zPos + int (adjCubeLength * 10)
		b = int (adjCubeLength * userCubeFaceBorderMargin)

		self .verticesType = "v3i"
		self .vertices = (
			#  What a mess...
			#0,0,0, 0,0,0, 0,0,0, 0,0,0,#
			#  Front
			xN+b,yN+b,zN, xF-b,yN+b,zN, xF-b,yF-b,zN, xN+b,yF-b,zN,
			xN,yN,zN, xF-b,yN,zN, xF-b,yN+b,zN, xN,yN+b,zN,
			xF-b,yN,zN, xF,yN,zN, xF,yF-b,zN, xF-b,yF-b,zN,
			xN+b,yF-b,zN, xF,yF-b,zN, xF,yF,zN, xN,yF,zN,
			xN,yN+b,zN, xN+b,yN+b,zN, xN+b,yF,zN, xN,yF,zN,
			#  Left
			xN,yN+b,zN+b, xN,yF-b,zN+b, xN,yF-b,zF-b, xN,yN+b,zF-b,
			xN,yN,zN, xN,yF-b,zN, xN,yF-b,zN+b, xN,yN,zN+b,
			xN,yF-b,zN, xN,yF,zN, xN,yF,zF-b, xN,yF-b,zF-b,
			xN,yF,zF-b, xN,yN+b,zF-b, xN,yN+b,zF, xN,yF,zF,
			xN,yN,zF, xN,yN+b,zF, xN,yN+b,zN+b, xN,yN,zN+b,
			#  Bottom
			xN+b,yN,zN+b, xF-b,yN,zN+b, xF-b,yN,zF-b, xN+b,yN,zF-b,
			xN,yN,zN, xF-b,yN,zN, xF-b,yN,zN+b, xN,yN,zN+b,
			xF-b,yN,zN, xF,yN,zN, xF,yN,zF-b, xF-b,yN,zF-b,
			xF,yN,zF-b, xF,yN,zF, xN,yN,zF, xN,yN,zF-b,
			xN+b,yN,zF, xN,yN,zF, xN,yN,zN+b, xN+b,yN,zN+b,
			#  Right
			xF,yN+b,zN+b, xF,yN+b,zF-b, xF,yF-b,zF-b, xF,yF-b,zN+b,
			xF,yN,zN, xF,yN,zN+b, xF,yF-b,zN+b, xF,yF-b,zN,
			xF,yF-b,zN, xF,yF,zN, xF,yF,zF-b, xF,yF-b,zF-b,
			xF,yF,zF-b, xF,yF,zF, xF,yN+b,zF, xF,yN+b,zF-b,
			xF,yN+b,zF, xF,yN,zF, xF,yN,zN+b, xF,yN+b,zN+b,
			#  Top
			xN+b,yF,zN+b, xF-b,yF,zN+b, xF-b,yF,zF-b, xN+b,yF,zF-b,
			xN,yF,zN, xF-b,yF,zN, xF-b,yF,zN+b, xN,yF,zN+b,
			xF-b,yF,zN, xF,yF,zN, xF,yF,zF-b, xF-b,yF,zF-b,
			xF,yF,zF, xN+b,yF,zF, xN+b,yF,zF-b, xF,yF,zF-b,
			xN,yF,zF, xN+b,yF,zF, xN+b,yF,zN+b, xN,yF,zN+b,
			#  Back
			xN+b,yN+b,zF, xF-b,yN+b,zF, xF-b,yF-b,zF, xN+b,yF-b,zF,
			xN,yN,zF, xN+b,yN,zF, xN+b,yF-b,zF, xN,yF-b,zF,
			xN,yF-b,zF, xN,yF,zF, xF-b,yF,zF, xF-b,yF-b,zF,
			xF-b,yF,zF, xF,yF,zF, xF,yN+b,zF, xF-b,yN+b,zF,
			xN+b,yN,zF, xF,yN,zF, xF,yN+b,zF, xN+b,yN+b,zF
		)

		self .coloursType = "c3f"
		coloursGenerate = []
		for i in range (6):
			for j in range (4):
				for k in range (3):
					coloursGenerate .append (userFaceColours[i][k] / 255)
			for l in range (48):
				coloursGenerate .append (0)
		self .colours = tuple (coloursGenerate)

	def getCornerVertices (self):
		#  Gets and returns the vertices of all the getCornerVertices

		xN = self .xPos
		yN = self .yPos
		zN = self .zPos
		xF = self .xPos + self .cubeLength
		yF = self .yPos + self .cubeLength
		zF = self .zPos + self .cubeLength

		return (
			xN,yN,zN, xF,yN,zN, xF,yN,zF, xN,yN,zF,
			xN,yF,zN, xF,yF,zN, xF,yF,zF, xN,yF,zF
		)

	def printCornerVertices (self):
		#  This is a fancy-pants version of getCornerVertices (), for visualisation
		xN = self .xPos % 1000
		yN = self .yPos % 1000
		zN = self .zPos % 1000
		xF = (self .xPos + self .cubeLength) % 1000
		yF = (self .yPos + self .cubeLength) % 1000
		zF = (self .zPos + self .cubeLength) % 1000

		print ("                - [%03d,%03d,%03d]" % (xF, yF, zF))
		print ("            -       -")
		print ("        -               -")
		print ("    -                       -")
		print ("- [%03d,%03d,%03d]                 - [%03d,%03d,%03d]" % (xN, yF, zF, xF, yF, zN))
		print ("|   -                       -   |")
		print ("|       -               -       |")
		print ("|           -       -           |")
		print ("|               - [%03d,%03d,%03d] |" % (xN, yF, zN))
		print ("|               |               |")
		print ("|               | [%03d,%03d,%03d] |" % (xF,yN, zF))
		print ("|               |               |")
		print ("- [%03d,%03d,%03d] |               - [%03d,%03d,%03d]" % (xN, yN, zF, xF, yN, zN))
		print ("    -           |           -")
		print ("        -       |       -")
		print ("            -   |   -")
		print ("                - [%03d,%03d,%03d]" % (xN, yN, zN))


class RubiksCube:
	def __init__ (self):
		self .renderBatch = pyglet .graphics .Batch ()

		#  Big dictionary to hold all the cubes in a way that can be easily accessed.
		#  The numbering defines which faces the edges/corners interact with:
		#  Group each relevant face into a number, with each face given its own digit.
		#  Sort the bits, descending.
		#  For example, to select the corner between faces 3, 0, 4:
		#  Group into a number where each face has its own bit: "304"
		#  Sort the bits, descending: "430"
		#  Access as `self .theCubes ["corners"][430]`
		self .theCubes = {
			"faces": {0: [], 1: [], 2: [], 3: [], 4: [], 5: []},
			"edges": {
				10: [], 20: [], 30: [], 40: [],
				21: [], 41: [], 51: [],
				32: [], 52: [],
				43: [], 53: [],
				54: []
			},
			"corners": {210: [], 410: [], 320: [], 430: [], 521: [], 541: [], 532: [], 543: []}
		}

	#  Start building the Rubik's Cube
	def init (self, cubeCount, cubeLength, xPos, yPos, zPos):
		self .cubeCount = cubeCount
		self .cubeLength = cubeLength
		self .xPos = xPos - int (cubeLength * cubeCount / 2)
		self .yPos = yPos - int (cubeLength * cubeCount / 2)
		self .zPos = zPos - int (cubeLength * cubeCount / 2)
		self .generateTheCubes ()

	#  Generates the cubes and adds them to the renderBatch
	def generateTheCubes (self):

		for i in range (6):
			#  Generate Faces
			for j in range (1, self .cubeCount - 1):
				for k in range (1, self .cubeCount - 1):
					if i == 0:
						theXPos = self .xPos + (j * int (self .cubeLength * userCubeSpacing))
						theYPos = self .yPos + (0 * int (self .cubeLength * userCubeSpacing))
						theZPos = self .zPos + (k * int (self .cubeLength * userCubeSpacing))
					elif i == 1:
						theXPos = self .xPos + (j * int (self .cubeLength * userCubeSpacing))
						theYPos = self .yPos + (k * int (self .cubeLength * userCubeSpacing))
						theZPos = self .zPos + (0 * int (self .cubeLength * userCubeSpacing))
					elif i == 2:
						theXPos = self .xPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
						theYPos = self .yPos + (j * int (self .cubeLength * userCubeSpacing))
						theZPos = self .zPos + (k * int (self .cubeLength * userCubeSpacing))
					elif i == 3:
						theXPos = self .xPos + (j * int (self .cubeLength * userCubeSpacing))
						theYPos = self .yPos + (k * int (self .cubeLength * userCubeSpacing))
						theZPos = self .zPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
					elif i == 4:
						theXPos = self .xPos + (0 * int (self .cubeLength * userCubeSpacing))
						theYPos = self .yPos + (j * int (self .cubeLength * userCubeSpacing))
						theZPos = self .zPos + (k * int (self .cubeLength * userCubeSpacing))
					elif i == 5:
						theXPos = self .xPos + (j * int (self .cubeLength * userCubeSpacing))
						theYPos = self .yPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
						theZPos = self .zPos + (k * int (self .cubeLength * userCubeSpacing))
					else:
						continue
					#  Make that cube!
					self .theCubes ["faces"][i] = self .generateACube (theXPos, theYPos, theZPos)

			#  Generate Edges
			for i in (10, 20, 30, 40, 21, 41, 51, 32, 52, 43, 53, 54):
				for j in range (self .cubeCount - 2):
					#theXPos = self .xPos + (x * int (self .cubeLength * userCubeSpacing))
					#theYPos = self .yPos + (y * int (self .cubeLength * userCubeSpacing))
					#theZPos = self .zPos + (z * int (self .cubeLength * userCubeSpacing))
					self .theCubes ["edges"][i] = self .generateACube (450, 450, 450 + (10 * j))

			#  Generate Corners
			for i in (210, 410, 320, 430, 521, 541, 532, 543):
				#  Extract the bits
				b0 = i % 10
				b1 = i // 10 % 10
				b2 = i // 100

				#  Height
				if b0 == 0:
					theYPos = self .yPos + (0 * int (self .cubeLength * userCubeSpacing))
				elif b2== 5:
					theYPos = self .yPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
				#  Depth
				if b1 == 1 or b0 == 1:
					theZPos = self .zPos + (0 * int (self .cubeLength * userCubeSpacing))
				elif b2 == 3 or b1 == 3 or b0 == 3:
					theZPos = self .zPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
				#  Width
				if b2 == 2 or b1 == 2 or b0 == 2:
					theXPos = self .xPos + (0 * int (self .cubeLength * userCubeSpacing))
				elif b2 == 4 or b1 == 4:
					theXPos = self .xPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))

				#  Write that data :D
				self .theCubes ["corners"][i] = self .generateACube (theXPos, theYPos, theZPos)


	def generateACube (self, xPos, yPos, zPos):
		#  Grab a new cube
		newCube = Cube (self .cubeLength, xPos, yPos, zPos)
		#  Add it to the render queue
		self .renderBatch .add (newCube .getVerticesCount (), pyglet .gl .GL_QUADS, None,
			(newCube .getVerticesType (), newCube .getVertices ()),
			(newCube .getColoursType (), newCube .getColours ())
		)
		#  Return it to the caller
		return newCube

	def renderTheCubes (self):
		self .renderBatch .draw ()

	def getTheCubes (self):
		return self .theCubes

	def getACube (self, cubeToGet):
		return self .theCubes [cubeToGet]



##  Initialise the primitives
theRubiksCube = RubiksCube ()
