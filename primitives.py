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
		self .verticesType = "v3i"
		#self .renderBatch .add (self .verticesCount, pyglet .gl .GL_QUADS, None, (self .verticesType, self .vertices))

	def getRenderBatch (self):
		return self .renderBatch

	def getPos (self):
		return (self .xPos, self .yPos)

	def getcubeLength (self):
		return self .cubeLength

	def setVerticesCount (self):
		self .verticesCount = len (self .vertices) // 3

	def getVerticesCount (self):
		return self .verticesCount

	def getVertices (self):
		return self .vertices

	def getVerticesType (self):
		return self .verticesType

	def buildCube (self):
		xN = self .xPos
		yN = self .yPos
		zN = self .zPos
		xF = self .xPos + self .cubeLength
		yF = self .yPos + self .cubeLength
		zF = self .zPos + self .cubeLength

		self .vertices = (
			xN,yN,zN, xF,yN,zN, xF,yF,zN, xN,yF,zN,
			xN,yN,zN, xN,yF,zN, xN,yF,zF, xN,yN,zF,
			xN,yN,zN, xF,yN,zN, xF,yN,zF, xN,yN,zF,
			xF,yN,zN, xF,yN,zF, xF,yF,zF, xF,yF,zN,
			xN,yF,zN, xF,yF,zN, xF,yF,zF, xN,yF,zF,
			xN,yN,zF, xF,yN,zF, xF,yF,zF, xN,yF,zF
		)

	def getCornerVertices (self):
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

	#  Generate the cubes
	def generateTheCubes (self):
		for i in range (self .cubeCount):
			#  Grab a new cube
			newCube = Cube (self .cubeLength, self .xPos, self .yPos + (15 * i), self .zPos)
			#  Add it to the list of cubes
			self .theCubes .append (newCube)
			#  Add it to the render queue
			self .renderBatch .add (newCube .getVerticesCount (), pyglet .gl .GL_QUADS, None, (newCube .getVerticesType (), newCube .getVertices ()))

	def renderTheCubes (self):
		self .renderBatch .draw ()

	def getTheCubes (self):
		return self .theCubes



##  Initialise the primitives
theRubiksCube = RubiksCube ()
