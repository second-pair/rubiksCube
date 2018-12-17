#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  Trying my best to abstract all the primitives info to its own file

import pyglet
from pyglet .gl import *
from pygletHandler import *



##  Classes
class Cube:
	verticesCount = 24
	verticesType = "v3i"
	renderBatch = pyglet .graphics .Batch ()


	def __init__ (self, cubeSize, xPos, yPos, zPos):
		self .cubeSize = cubeSize
		self .xPos = xPos
		self .yPos = yPos
		self .zPos = zPos
		self .buildCube ()
		self .renderBatch .add (self .verticesCount, pyglet .gl .GL_QUADS, None, (self .verticesType, self .vertices))
		#cubesBatch .add (cube1 .getVerticesCount (), pyglet .gl .GL_QUADS, None, (cube1 .getVerticesType (), cube1 .getVertices ()))

	def getRenderBatch (self):
		return self .renderBatch

	def getPos (self):
		return (self .xPos, self .yPos)

	def getCubeSize (self):
		return self .cubeSize

	#def setVerticesCount (self):
	
	def getVerticesCount (self):
		#  Change this to work out automatically - we'll probably be changing the shape of things often
		return self .verticesCount

	def getVertices (self):
		return self .vertices

	def getVerticesType (self):
		return self .verticesType

	def buildCube (self):
		xN = self .xPos
		yN = self .yPos
		zN = self .zPos
		xF = self .xPos + self .cubeSize
		yF = self .yPos + self .cubeSize
		zF = self .zPos + self .cubeSize
		
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
		xF = self .xPos + self .cubeSize
		yF = self .yPos + self .cubeSize
		zF = self .zPos + self .cubeSize
	
		return (
			xN,yN,zN, xF,yN,zN, xF,yN,zF, xN,yN,zF,
			xN,yF,zN, xF,yF,zN, xF,yF,zF, xN,yF,zF
		)

	def printCornerVertices (self):
		xN = self .xPos
		yN = self .yPos
		zN = self .zPos
		xF = self .xPos + self .cubeSize
		yF = self .yPos + self .cubeSize
		zF = self .zPos + self .cubeSize

		print ("ULF:  ")
		print ("LLF:  ")
		

class RubiksCube:
	theCubes = []
	#number, size, x, y, z

	def __init__ (self, cubeCount, cubeLength, xPos, yPos, zPos):
		self .cubeCount = cubeCount
		self .cubeLength = cubeLength
		self .xPos = xPos
		self .yPos = yPos
		self .zPos = zPos

		self .generateCubes ()

	#  Generate the cubes
	def generateCubes (self):
		for i in range (self .cubeCount):
			#  Grab a new cube
			newCube = Cube (self .cubeLength, self .xPos, self .yPos, self .zPos)
			#  Add it to the list of cubes
			self .theCubes .append (newCube)
			#  Add it to the render queue
			self .renderBatch .add (newCube .getVerticesCount (), pyglet .gl .GL_QUADS, None, (newCube .getVerticesType (), newCube .getVertices ()))

	def renderTheCubes (self):
		print ("Rendering later")
			



##  Batches

#cubesBatch = pyglet .graphics .Batch ()



##  Primitives
#rCube1 = RubiksCube (1, 15, 0, 0, 0)
cube1 = Cube (15, 0, 0, 0)
#cubesBatch .add (cube1 .getVerticesCount (), pyglet .gl .GL_QUADS, None, (cube1 .getVerticesType (), cube1 .getVertices ()))

print (cube1 .getCornerVertices ())

'''
cube1 = cubesBatch .add (24, pyglet .gl .GL_QUADS, None, ("v3i", (
	50, 50, 50,
	50, 80, 50,
	80, 80, 50,
	80, 50, 50,

	50, 50, 50,
	50, 80, 50,
	50, 80, 80,
	50, 50, 80,

	50, 50, 50,
	80, 50, 50,
	80, 50, 80,
	50, 50, 80,

	50, 80, 50,
	50, 80, 80,
	80, 80, 80,
	80, 80, 50,

	80, 50, 50,
	80, 50, 80,
	80, 80, 80,
	80, 80, 50,

	50, 50, 80,
	50, 80, 80,
	80, 80, 80,
	80, 50, 80
	)))
'''
'''
cube2 = cubesBatch .add (8, pyglet .gl .GL_QUADS, None, ("v3i", (
	0, 0, 100,
	0, 10, 100,
	10, 10, 100,
	10, 0, 100,
	
	0, 0, 0,
	0, 10, 0,
	10, 10, 0,
	10, 0, 0
	)))
'''
