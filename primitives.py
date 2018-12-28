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

	def init (self, xPos = 0, yPos = 0, zPos = 0, cubeLength = userCubeLength, theFace = 0):
		self .xPos = xPos - int (cubeLength / 2)
		self .yPos = yPos - int (cubeLength / 2)
		self .zPos = zPos - int (cubeLength / 2)

		self .cubeLength = cubeLength
		self .theFace = theFace
		self .faceColour = theFace

		self .createTheFace ()


	def createTheFace (self):
		#  Builds the cube's vertices
		#  This now builds a "unit langth" model and scales it by the cubeLength
		adjCubeLength = self .cubeLength / 10
		#  Calculate the border "thickness"
		b = int (adjCubeLength * userCubeFaceBorderMargin)

		#  Instead of actually faffing around with 3D rotation, how's about
		#  we just work it out manually instead?
		#  Set as 0s initially, then transform to desired location
		xN = self .xPos
		yN = self .yPos
		zN = self .zPos
		xF = self .xPos + int (adjCubeLength * 10)
		yF = self .yPos + int (adjCubeLength * 10)
		zF = self .zPos + int (adjCubeLength * 10)

		#  Good ol' lookup table for the correct vertices pattern
		positionData = getFaceVertices (xN, yN, zN, xF, yF, zF, b, self .theFace)

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

	def render (self):
		self .renderBatch .draw ()


	#  Positional Data
	def getPos (self):
		return (self .xPos, self .yPos, self .zPos)
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



def getFaceVertices (xN, yN, zN, xF, yF, zF, b, whichFace):
	#  Generate the vertices - don't ask how
	if whichFace == 0:
		#  Bottom
		faceVertices = [
			xN+b,yN,zN+b, xF-b,yN,zN+b, xF-b,yN,zF-b, xN+b,yN,zF-b,
			xN,yN,zN, xF-b,yN,zN, xF-b,yN,zN+b, xN,yN,zN+b,
			xF-b,yN,zN, xF,yN,zN, xF,yN,zF-b, xF-b,yN,zF-b,
			xF,yN,zF-b, xF,yN,zF, xN,yN,zF, xN,yN,zF-b,
			xN+b,yN,zF, xN,yN,zF, xN,yN,zN+b, xN+b,yN,zN+b
		]

	elif whichFace == 1:
		#  Front
		faceVertices = [
			xN+b,yN+b,zN, xF-b,yN+b,zN, xF-b,yF-b,zN, xN+b,yF-b,zN,
			xN,yN,zN, xF-b,yN,zN, xF-b,yN+b,zN, xN,yN+b,zN,
			xF-b,yN,zN, xF,yN,zN, xF,yF-b,zN, xF-b,yF-b,zN,
			xN+b,yF-b,zN, xF,yF-b,zN, xF,yF,zN, xN,yF,zN,
			xN,yN+b,zN, xN+b,yN+b,zN, xN+b,yF,zN, xN,yF,zN
		]

	elif whichFace == 2:
		#  Right
		faceVertices = [
			xF,yN+b,zN+b, xF,yN+b,zF-b, xF,yF-b,zF-b, xF,yF-b,zN+b,
			xF,yN,zN, xF,yN,zN+b, xF,yF-b,zN+b, xF,yF-b,zN,
			xF,yF-b,zN, xF,yF,zN, xF,yF,zF-b, xF,yF-b,zF-b,
			xF,yF,zF-b, xF,yF,zF, xF,yN+b,zF, xF,yN+b,zF-b,
			xF,yN+b,zF, xF,yN,zF, xF,yN,zN+b, xF,yN+b,zN+b
		]

	elif whichFace == 3:
		#  Back
		faceVertices = [
			xN+b,yN+b,zF, xF-b,yN+b,zF, xF-b,yF-b,zF, xN+b,yF-b,zF,
			xN,yN,zF, xN+b,yN,zF, xN+b,yF-b,zF, xN,yF-b,zF,
			xN,yF-b,zF, xN,yF,zF, xF-b,yF,zF, xF-b,yF-b,zF,
			xF-b,yF,zF, xF,yF,zF, xF,yN+b,zF, xF-b,yN+b,zF,
			xN+b,yN,zF, xF,yN,zF, xF,yN+b,zF, xN+b,yN+b,zF
		]

	elif whichFace == 4:
		#  Left
		faceVertices = [
			xN,yN+b,zN+b, xN,yF-b,zN+b, xN,yF-b,zF-b, xN,yN+b,zF-b,
			xN,yN,zN, xN,yF-b,zN, xN,yF-b,zN+b, xN,yN,zN+b,
			xN,yF-b,zN, xN,yF,zN, xN,yF,zF-b, xN,yF-b,zF-b,
			xN,yF,zF-b, xN,yN+b,zF-b, xN,yN+b,zF, xN,yF,zF,
			xN,yN,zF, xN,yN+b,zF, xN,yN+b,zN+b, xN,yN,zN+b
		]

	elif whichFace == 5:
		#  Top
		faceVertices = [
			xN+b,yF,zN+b, xF-b,yF,zN+b, xF-b,yF,zF-b, xN+b,yF,zF-b,
			xN,yF,zN, xF-b,yF,zN, xF-b,yF,zN+b, xN,yF,zN+b,
			xF-b,yF,zN, xF,yF,zN, xF,yF,zF-b, xF-b,yF,zF-b,
			xF,yF,zF, xN+b,yF,zF, xN+b,yF,zF-b, xF,yF,zF-b,
			xN,yF,zF, xN+b,yF,zF, xN+b,yF,zN+b, xN,yF,zN+b
		]

	return faceVertices
