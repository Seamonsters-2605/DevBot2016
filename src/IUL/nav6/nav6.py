__author__ = 'Ian'
import math

from .nav6protocol import *
from IUL import serial
from ..timer import intervaltimer

class Nav6():
	def __init__(self, serial1 , updateRate):
		self.stopRequested = False
		self.serial = serial.Serial(port=0 , baudrate= self.getDefaultBaudRate())
		self.updateRate = updateRate
		self.yaw = 0
		self.pitch = 0
		self.roll = 0
		self.compassHeading = 0
		self.gravity = [0.0 , 0.0 , 0.0]
		self.acceleration = [0.0 , 0.0 , 0.0]
		self.orientation = Quaternion()
		self.isStopped = True

		pass

	def start(self):
		self.stopRequested = False

		# threading
		# ???

	def stop(self, wait = False):
		self.stopRequested = True

	def getYaw(self):
		return self.yaw

	def getPitch(self):
		return self.pitch

	def getRoll(self):
		return self.roll

	def getCompassHeading(self):
		return self.compassHeading

	def getDefaultBaudRate(self):
		return 57600

	def sendStreamCommand(self, updateRate):
		buff = [0] * 9

		buff[0] = Nav6Protocol.PACKET_START_CHAR
		buff[1] = Nav6Protocol.MSGID_STREAM_CMD
		buff[2] = Nav6Protocol.STREAM_CMD_STREAM_TYPE_QUATERNION
		self.setStreamUint8 ( buff , 3, updateRate)
		self.setStreamTermination ( buff , 5 )

		self.serial.write(buff)
		self.serial.flush()
		#reset serial???

	def calcaulteChecksum(self , buffer , length):
		sum = 0
		for buff in buffer:
			sum += buff
		return sum

	def setStreamUint8(self, buffer , index , value):
		hexref = '0123456789ABCDEF'
		buffer [ index + 1 ] = int( hexref [ value & 0x0F])
		buffer [ index  ] = int( hexref [ value >> 4] )


	def setStreamUint16(self, buffer , index , value):
		hexRef = '0123456789ABCDEF'
		buffer[ index + 3 ] =  int( hexRef[ value & 0x0F])
		buffer[ index + 2 ] = int ( hexRef[ value >> 4 ])
		buffer[ index + 1 ] = int ( hexRef[ value >> 8 ])
		buffer [ index ] = int ( hexRef[ (value >> 12) & 0x000F ])

	def setStreamFloat(self , buffer , index , value ): #not finshed
		decRef = '0123456789'
		buffer[ index ] = '+' if value > 0 else '-'
		if value < 0:
			value = -value # check for error later

		buffer[ index + 1] = int( decRef[ int( math.fmod(value * 100.0, 10.0))] )
		buffer[ index + 1] = int( decRef[ int( math.fmod(value * 10.0, 10.0))] )
		buffer[ index + 1] = int( decRef[ int( math.fmod(value , 10.0))] )
		buffer[ index + 4] = int('.')
		buffer[ index + 1] = int( decRef[ int( math.fmod(value / 10.0, 10.0))] )
		buffer[ index + 1] = int( decRef[ int( math.fmod(value / 100.0, 10.0))] )

	def getStreamUint8(self , buffer , index ):
		zeroRef = int('0')
		nineRef = int('9')
		aRef = int('A')

		value = 0

		if ( buffer [ index ] >= zeroRef and buffer[ index ] <= nineRef):
			value = ( buffer[index] - zeroRef ) << 4
		else:
			value = ( ( buffer[index] - aRef) + 10 ) << 4

		if ( buffer [ index + 1 ] >= zeroRef and buffer[index + 1] <= nineRef ):
			value += buffer[ index + 1] - zeroRef
		else:
			value += ( buffer[ index + 1] - aRef) + 10

		return value

	def getStreamInt8(self , buffer , index ):
		return  int( self.getStreamUint8( buffer , index ) )

	def getStreamUint16(self , buffer , index ):
		value = self.getStreamUint8( buffer , index ) << 8
		value += self.getStreamUint8( buffer, index + 2 )

		return  value

	def getStreamInt16(self , buffer , index ):
		return  int( self.getStreamUint8( buffer , index ))

	def getStreamNumber(self, buffer ,index ):
		zeroRef = int('0')
		minusRef = int('-')

		sign = bool(buffer[ index ] == minusRef)

		value = ( buffer [ index + 6 ] - zeroRef) / 100.0
		value += ( buffer [ index + 5 ] - zeroRef) / 10.0
		value += ( buffer [ index + 3 ] - zeroRef)
		value += ( buffer [ index + 2 ] - zeroRef) * 10
		value += ( buffer [ index + 1 ] - zeroRef) * 100

		if( sign ):
			value = - value

		return  value

	def setStreamTermination(self , buffer , messageLength ):
		self.setStreamUint8( buffer , messageLength, self.calcaulteChecksum( buffer, messageLength))
		buffer[ messageLength + 2 ] = '\r'
		buffer[ messageLength + 3 ] = '\n'
		buffer[ messageLength + 4] = '\0'

	def serialUpdate(self, buffer , messageLength):
		timeout = intervaltimer.IntervalTimer()
		offset = 0

		self.serial.setTimeout( 2000 )
		self.serial.open()

		self.sendStreamCommand( self.updateRate)
		timeout.start()

		while( not self.stopRequested):
			if ( timeout.getTimeMS() > 3000):
				self.sendStreamCommand(self.updateRate)
				timeout.restart()
				offset = 0




	def decodeRegularResponse(self , buffer , length):
		pass

	def decodeQuaternionResponse(self , buffer , length):
		pass


class Quaternion ():
	def __init__ (self):
		self.x
		self.y
		self.z
		self.w


