__author__ = 'Ian'

import math
import time

from .dspfilter import *

__all__ = [ "MecanumVelocityProfile", "MecanumXYTVPFilter" ]


class MecanumVelocityProfile( DSPFilter_2_2 ):
	def __init__( self, exponent ):
		super( ).__init__( )
		self.exponent = exponent
		self.a = None
		self.b = None

	def setExponent( self, exponent ):
		self.exponent = exponent

	def compute( self, Magnitude, Direction ):
		self.a = math.pow( Magnitude, self.exponent )
		self.b = Direction

	def reset( self ):
		self.a = None
		self.b = None


class MecanumXYTVPFilter( DSPFilter_2_2 ):
	def __init__( self, vRamp ):
		self.vRamp = vRamp
		self.cx = 0.0
		self.cy = 0.0
		self.timeDiff = time.time( )

	def setVRamp( self, vRamp ):
		self.vRamp = vRamp

	def compute( self, x, y ):
		# Need more research into timing in python...
		xDiff = x - self.cx
		yDiff = y - self.cy
		self.timeDiff = time.time( ) - self.timeDiff
		if (math.fabs( xDiff ) < self.timeDiff * self.vRamp) or self.vRamp == 0:
			self.cx = x
		else:
			self.cx = (self.vRamp if (xDiff > 0) else -self.vRamp) * self.timeDiff

		if (math.fabs( yDiff ) < self.timeDiff * self.vRamp) or self.vRamp == 0:
			self.cy = y
		else:
			self.cy = (self.vRamp if (yDiff > 0) else -self.vRamp) * self.timeDiff

	def readA( self ):
		return self.cx

	def readB( self ):
		return self.cy

	def reset( self ):
		pass
