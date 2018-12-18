#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  Trying my best to abstract all the primitives info to its own file

import pyglet
from pyglet .gl import *
from pygletHandler import *



##  Classes
class Cube:
	def __init__ (self, cubeLength, xPos, yPos, zPos):
		self .cubeLength = cubeLength
		self .xPos = xPos
		self .yPos = yPos
		self .zPos = zPos

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
		xF = self .xPos + int (10 * adjCubeLength)
		yF = self .yPos + int (10 * adjCubeLength)
		zF = self .zPos + int (10 * adjCubeLength)

		self .verticesType = "v3i"
		self .vertices = (
			#  Need to add colours to these
			#  Front
			xN,yN,zN, xF,yN,zN, xF,yF,zN, xN,yF,zN,
			#  Left
			xN,yN,zN, xN,yF,zN, xN,yF,zF, xN,yN,zF,
			#  Bottom
			xN,yN,zN, xF,yN,zN, xF,yN,zF, xN,yN,zF,
			#  Right
			xF,yN,zN, xF,yN,zF, xF,yF,zF, xF,yF,zN,
			#  Top
			xN,yF,zN, xF,yF,zN, xF,yF,zF, xN,yF,zF,
			#  Back
			xN,yN,zF, xF,yN,zF, xF,yF,zF, xN,yF,zF
		)

		self .coloursType = "c3f"
		self .colours = (
			#  Front
			253.0 / 255, 144.0 / 255, 80, 253.0 / 255, 144.0 / 255, 80, 253.0 / 255, 144.0 / 255, 80, 253.0 / 255, 144.0 / 255, 80,
			#  Left
			1,1,1, 1,1,1, 1,1,1, 1,1,1,
			#  Bottom
			1,1,1, 1,1,1, 1,1,1, 1,1,1,
			#  Right
			1,1,1, 1,1,1, 1,1,1, 1,1,1,
			#  Top
			1,1,1, 1,1,1, 1,1,1, 1,1,1,
			#  Back
			1,1,1, 1,1,1, 1,1,1, 1,1,1
		)

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
		self .theCubes = []

	#  Start building the Rubik's Cube
	def init (self, cubeCount, cubeLength, xPos, yPos, zPos):
		self .cubeCount = cubeCount
		self .cubeLength = cubeLength
		self .xPos = xPos
		self .yPos = yPos
		self .zPos = zPos
		self .generateTheCubes ()

	#  Generates the cubes and adds them to the renderBatch
	def generateTheCubes (self):
		for i in range (self .cubeCount):
			for j in range (self .cubeCount):
				for k in range (self .cubeCount):
					theXPos = self .xPos + (i * int (self .cubeLength * 1.5))
					theYPos = self .yPos + (j * int (self .cubeLength * 1.5))
					theZPos = self .zPos + (k * int (self .cubeLength * 1.5))

					#  Grab a new cube
					newCube = Cube (self .cubeLength, theXPos, theYPos, theZPos)
					#  Add it to the list of cubes
					self .theCubes .append (newCube)
					#  Add it to the render queue
					self .renderBatch .add (newCube .getVerticesCount (), pyglet .gl .GL_QUADS, None,
						(newCube .getVerticesType (), newCube .getVertices ()),
						(newCube .getColoursType (), newCube .getColours ())
					)

	def renderTheCubes (self):
		self .renderBatch .draw ()

	def getTheCubes (self):
		return self .theCubes

	def getACube (self, cubeToGet):
		return self .theCubes [cubeToGet]



##  Initialise the primitives
theRubiksCube = RubiksCube ()
