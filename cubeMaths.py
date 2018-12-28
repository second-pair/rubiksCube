#! /usr/bin/python



##  Notes

#  Author:  Blair Edwards 2018
#  This will end up holding the cube matrix and the cube-solving algorithms

#  I've decided to let the RubiksCubeMatrix class controll the RubiksCubeVisual
#  cube directly, since it will make the solving process much easier and allow
#  the solving algorithm to update visuals as of when it needs to.
#  This should avoid having the main rubiksCube function calling a step of the
#  algorithm; retrieving the results; updating the visuals; then calling the
#  next step.

from preferences import *

class RubiksCubeMatrix:
	def __init__ (self):
		self .faceMatrix = []

	def init (self, cubeCount):
		self .cubeCount = cubeCount
		self .theRubiksCubeVisual = RubiksCubeVisual ()
		generateFaces ()

	def generateFaces (self):
		#  Generate each face
		for i in range (6):
			self .faceMatrix .append ([])

			for j in range (self .cubeCount):
				self .faceMatrix [i] .append ([])

				for k in range (self .cubeCount):
					self .faceMatrix [i][j] .append (i)

		#  Generate the visual cube
		self .theRubiksCubeVisual .init ()
		for currFace in range (6):
			#RubiksCubeVisual .generateFace (self .faceMatrix (currFace))
			pass

	def getFace (self, faceToGet):
		return self .faceMatrix [faceToGet]

	def swapLines (self, line1: tuple, line2: tuple):
		#  Function to rotate a slice of faces
		#  We'll need a different way to select the slice being rotated

		#  Figure out which items actually needto be swapped
		#  Due to how the indexing works, we'll need to account for skipping
		#  across sub-lists

		#  Start swapping
		tempLine = []
		for i in range (self .cubeCount):
			#  Store one face's slice in a temporary variable
			tempLine .append (self .faceMatrix [line1][i])
		#  Like this, but better.
		for i in range (self .cubeCount):
			faceMatrix [line1][i] = faceMatrix [line2][i]
		for i in range (self .cubeCount):
			faceMatrix [line2][i] = faceMatrix [line3][i]
		for i in range (self .cubeCount):
			faceMatrix [line3][i] = faceMatrix [line4][i]
		for i in range (self .cubeCount):
			#  Use the temporary variable to fill in the final face-slice
			faceMatrix [line4][i] = tempLine [i]

		def renderTheFaces (self):
			theRubiksCubeVisual .renderTheFaces ()

theRubiksCubeMatrix = RubiksCubeMatrix ()
