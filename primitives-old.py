class RubiksCubeVisual:
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
		#  Don't ask how this all works...

		#  Generate Faces
		#  I think I can optimise this one a bit
		for i in self .theCubes ["faces"]:#range (6):
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
					self .theCubes ["faces"][i] .append (self .generateACube (theXPos, theYPos, theZPos))

		#  Generate Edges
		for i in self .theCubes ["edges"]:#(10, 20, 30, 40, 21, 41, 51, 32, 52, 43, 53, 54):
			#  Extract the bits
			bit0 = i % 10
			bit1 = i // 10

			#  Basically, we can work out which direction each edge travels
			#  based on which faces it's touching.  3 sets of tests, for each
			#  direction.

			for j in range (1, self .cubeCount - 1):
				#  Could be Y- or Z-bound, can fix X
				if bit0 == 2 or bit1 == 2:
					theXPos = self .xPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
				elif bit0 == 4 or bit1 == 4:
					theXPos = self .xPos + (0 * int (self .cubeLength * userCubeSpacing))
				else:
					#  Must be X-bound
					theXPos = self .xPos + (j * int (self .cubeLength * userCubeSpacing))

				#  Could be X- or Z-bound, can fix Y
				if bit0 == 0 or bit1 == 0:
					theYPos = self .yPos + (0 * int (self .cubeLength * userCubeSpacing))
				elif bit0 == 5 or bit1 == 5:
					theYPos = self .yPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
				else:
					#  Must be Y-bound
					theYPos = self .yPos + (j * int (self .cubeLength * userCubeSpacing))

				#  Could be X- or Y-bound, can fix Z
				if bit0 == 1 or bit1 == 1:
					theZPos = self .zPos + (0 * int (self .cubeLength * userCubeSpacing))
				elif bit0 == 3 or bit1 == 3:
					theZPos = self .zPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
				else:
					#  Must be Z-bound
					theZPos = self .zPos + (j * int (self .cubeLength * userCubeSpacing))

				#  Add the cube
				self .theCubes ["edges"][i] .append (self .generateACube (theXPos, theYPos, theZPos))

		#  Generate Corners
		for i in self .theCubes ["corners"]:#(210, 410, 320, 430, 521, 541, 532, 543):
			#  Extract the bits
			bit0 = i % 10
			bit1 = i // 10 % 10
			bit2 = i // 100

			#  Here, we perform 3 sets of ifs (one per co-ordinate) to zero in
			#  on which extreme that co-ordinate is at.  Do that 3 times and
			#  you've got your (x, y, z).

			#  Differentiate height
			if bit0 == 0:
				theYPos = self .yPos + (0 * int (self .cubeLength * userCubeSpacing))
			elif bit2== 5:
				theYPos = self .yPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
			#  Differentiate depth
			if bit1 == 1 or bit0 == 1:
				theZPos = self .zPos + (0 * int (self .cubeLength * userCubeSpacing))
			elif bit2 == 3 or bit1 == 3 or bit0 == 3:
				theZPos = self .zPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))
			#  Differentiate width
			if bit2 == 2 or bit1 == 2 or bit0 == 2:
				theXPos = self .xPos + (0 * int (self .cubeLength * userCubeSpacing))
			elif bit2 == 4 or bit1 == 4:
				theXPos = self .xPos + ((self .cubeCount - 1) * int (self .cubeLength * userCubeSpacing))

			#  Write that data :D
			self .theCubes ["corners"][i] .append (self .generateACube (theXPos, theYPos, theZPos))


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

	def renderTheFaces (self):
		#  Updates the cube's positions via the Pyglet batch
		self .renderBatch .draw ()

	def getTheCubes (self):
		#  Returns the whole cubes dictionary
		return self .theCubes

	def getACube (self, key1, key2):
		#  Grab a single cube, without having to copy the entire dictionary
		return self .theCubes [key1][key2]

	def printCubeCount (self):
		#  Sum up the number of stored cubes
		theCount = 0
		for level1 in self .theCubes:
			for level2 in self .theCubes [level1]:
				for level3 in self .theCubes [level1][level2]:
					theCount += 1
		print ("%d cubes counted." % theCount)


	def updateCubePositions (self):
		#  This is basically the equivalent of peeling all the stickers off and
		#  Sticking them back on where we want

		#for cube in theCubes etc
		#theCube nowLooksLike theRubiksCubeMatrix [whatever]
		pass


	#  Actually, I think I'm doing this wrongself.#  This should probably be a
	#  function that just rotates the individual cubes to reflect the status
	#  of another matrix.
	def rotateAFace (self, faceToRotate, direction):
		#  Firstly, we add all the face-, edge- and corner-cubes to a list
		#  Note:  We need to unwrap the sub-lists returned from the dictionay

		#faceCentre = (0, 0, 0) + something  #  May not be needed?

		#  Grab the face-cubes
		theFace = self .theCubes ["faces"][faceToRotate]

		#  Grab the edge-cubes
		for edgeDict in self .theCubes ["edges"]:
			theEdges = []
			#  Extract the bits
			bit0 = edgeDict % 10
			bit1 = edgeDict // 10

			if bit0 == faceToRotate or bit1 == faceToRotate:
				theEdges .append (self .theCubes ["edges"][edgeDict])

		#  Grab the corner-cubes
		for cornerDict in self .theCubes ["corners"]:
			theCorners = []
			#  Extract the bits
			bit0 = cornerDict % 10
			bit1 = cornerDict // 10 % 10
			bit2 = cornerDict // 100

			if bit0 == faceToRotate or bit1 == faceToRotate or bit2 == faceToRotate:
				theCorners .append (self .theCubes ["corners"][cornerDict])

		#  Add a timer, somehow??
		#pyglet .clock .schedule (update)

		#  Let's just print it for now...
		print ("Rotating %d cubes..." % len (rotatingCubes))
