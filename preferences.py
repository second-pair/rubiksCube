#! /usr/bin/python

#  Author:  Blair Edwards 2018
#  Parameters & Globals
#  Feeling like this is gonna need its own major commenting soon.

#  Error function
#  I've put this here, as it's currently the only thinkg imported by evverything.
from datetime import datetime
def die (callingFunction, theErrorText):
	log (callingFunction, theErrorText)
	exit ()

def debug (callingFunction, theErrorText):
	if userDebugInfo == 1:
		print ("[%s]  %s:  %s" % (datetime .now (), callingFunction, theErrorText))

def log (callingFunction, theErrorText):
	print ("[%s]  %s:  %s" % (datetime .now (), callingFunction, theErrorText))

#  Programme Parameters
#  I should smart-DPI this again
#userScreenWidth = 1800
#userScreenHeight = 1000
userScreenWidth = 1000
userScreenHeight = 800
#userCameraDistance = -250
userCameraDistance = -250
userDebugInfo = 1

#  Matrices Window
showMatricesWindow = 1
matricesWindowScale = 6
matricesWindowCorrection = 2

#  Timey Wimey
userCubeRotateRate = 2
userAlgoMovePeriod = 0.02

#  Cube Parameters
userCubeSize = 3
userCubeLength = 20
userCubeFaceBorderMargin = 1
userCubeSpacing = 1
userAlgoStartingSide = 0
cubeShuffleAmount = 100

#  Colours
userBackgroundColour = (40, 43, 53)
userFaceColours = (	#  Easy dev colours
	(0, 0, 0),		#  0 - Black
	(255, 0, 0),	#  1 - Red
	(0, 255, 0),	#  2 - Green
	(0, 0, 255),	#  3 - Blue
	(127,127, 127),	#  4 - Grey
	(255, 255, 255),#  5 - White
)
'''(
    (251, 9, 44),
    (70, 225, 69),
    (253, 144, 80),
    (133, 114, 248),
    (210, 0, 160),
    (25, 196, 241),
    (50, 50, 50),
    (200, 200, 200),
    (180, 180, 180),
    (160, 160, 160),
    (140, 140, 140),
    (120, 120, 120),
)'''

#  Solving Parameters
#starting face
#shuffling options
#font?


'''
Background		#1E2028 - 40  43  53
Dark Black		#000000 - 0   0   0
Lite Black		#535353 - 83  83  83
Dark Red		#DB2C38 - 219 44  56
Lite Red		#FB092C - 251 9   44
Dark Green		#41B645 - 65  182 69
Lite Green		#46E415 - 70  225 69
Dark Yellow		#C67C48 - 198 124 72
Lite Yellow		#FD9050 - 253 144 80
Dark Blue		#786DC4 - 120 109 196
Lite Blue		#8572F8 - 133 114 248
Dark Magenta	#B21889 - 178 24  137
Lite Magenta	#D200A0 - 210 0   160
Dark Cyan		#00A0BE - 0   160 190
Lite Cyan		#19C4F1 - 25  196 241
Dark White		#D0D0D0 - formerly 55747C - 85 116 124
Lite White		#FFFFFF - 255 255 255
'''
