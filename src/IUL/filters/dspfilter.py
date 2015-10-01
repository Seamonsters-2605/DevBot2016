__author__ = 'Ian'

__all__ = [ "DSPFilter_1_1", "DSPFilter_2_1", "DSPFilter_1_2", "DSPFilter_2_2" ]


class DSPFilter_1_1:
	def __init__( self ):
		self.a = None

	def compute( self, feed ):
		pass

	def read( self ):
		if self.a != None:
			return self.a

	def reset( self ):
		pass

	# dont override this
	def getType( self ):
		return "1_1"


class DSPFilter_2_1:
	def __init__( self ):
		self.a = None

	def compute( self, feedA, feedB ):
		pass

	def read( self ):
		if self.a != None:
			return self.a

	def reset( self ):
		pass

	# dont override this
	def getType( self ):
		return "2_1"


class DSPFilter_1_2:
	def __init__( self ):
		self.a = None
		self.b = None

	def compute( self, feed ):
		pass

	def readA( self ):
		if self.a != None:
			return self.a

	def readB( self ):
		if self.b != None:
			return self.b

	def reset( self ):
		pass

	# dont override this
	def getType( self ):
		return "1_2"


class DSPFilter_2_2:
	def __init__( self ):
		self.a = None
		self.b = None

	def compute( self, feedA, feedB ):
		pass

	def readA( self ):
		if self.a != None:
			return self.a

	def readB( self ):
		if self.b != None:
			return self.b

	def reset( self ):
		pass

	# dont override this
	def getType( self ):
		return "2_2"
