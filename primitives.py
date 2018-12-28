#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  Trying my best to abstract all the primitives info to its own file

import pyglet
from pyglet .gl import *
from preferences import *
#from pygletHandler import *



class CubeFace:
	def __init__ (self):
		self .renderBatch = pyglet .graphics .Batch ()

	def init (self, xPos = 0, yPos = 0, zPos = 0, xAngle = 0, yAngle = 0, zAngle = 0, cubeLength = userCubeLength, startColour = 0):
		self .xPos = xPos - int (cubeLength / 2)
		self .yPos = yPos - int (cubeLength / 2)
		self .zPos = zPos - int (cubeLength / 2)
		self .xAngle = xAngle
		self .yAngle = yAngle
		self .zAngle = zAngle

		self .cubeLength = cubeLength
		self .faceColour = startColour

		self .createTheFace ()

	def createTheFace (self):
		#  Builds the cube's vertices
		#  This now builds a "unit langth" model and scales it by the cubeLength
		adjCubeLength = self .cubeLength / 10

		#  Set as 0s initially, then transform to desired location
		xN = self .xPos
		yN = self .yPos
		zN = self .zPos
		xF = self .xPos + int (adjCubeLength * 10)
		yF = self .yPos + int (adjCubeLength * 10)
		zF = self .zPos + int (adjCubeLength * 10)
		b = int (adjCubeLength * userCubeFaceBorderMargin)

		#  Generate the vertices - don't ask how
		#  We'll need to update these to include the rotation data
		positionData = [
			xN+b,yN+b,zN, xF-b,yN+b,zN, xF-b,yF-b,zN, xN+b,yF-b,zN,
			xN,yN,zN, xF-b,yN,zN, xF-b,yN+b,zN, xN,yN+b,zN,
			xF-b,yN,zN, xF,yN,zN, xF,yF-b,zN, xF-b,yF-b,zN,
			xN+b,yF-b,zN, xF,yF-b,zN, xF,yF,zN, xN,yF,zN,
			xN,yN+b,zN, xN+b,yN+b,zN, xN+b,yF,zN, xN,yF,zN
		]

		#  Generate the colour printFaceCount
		#  Currently black borders round the coloured face
		colourData = []
		for j in range (4):
			for k in range (3):
				colourData .append (userFaceColours[self .faceColour][k] / 255)
		for l in range (48):
			colourData .append (0)
		#  This is left over from before and can probably disappear

		#  Calculate the number of vertices
		self .verticesCount = len (positionData) // 3

		#  Rotate the face

		#  Add all that to the internal vertex list
		self .vertices = self .renderBatch .add (self .verticesCount, pyglet .gl .GL_QUADS, None,
		    ('v3i', positionData),
		    ('c3f', colourData)
		)

	def transform (self):
		#  This'll probably disappear soon
		pass

	def render (self):
		self .renderBatch .draw ()

	#  Positional Data
	def getPos (self):
		return (self .xPos, self .yPos, self .zPos)
	def getAngles (self):
		return (self .xAngle, self .yAngle, self .zAngle)
	def getcubeLength (self):
		return self .cubeLength

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
	def setFaceColour (self, newFaceColour):
		#  The first 12 points hold the coloured face data
		newColours = []
		for j in range (4):
			for k in range (3):
				newColours .append (userFaceColours [newFaceColour][k] / 255)
		self .vertices .colors [:12] = newColours
