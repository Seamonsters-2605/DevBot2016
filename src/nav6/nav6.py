__author__ = 'Ian'
from .nav6protocol import *
import serial
import math


class Nav6():
	def __init__(self, serial1 , updateRate):
		self.stopRequested = False
		self.serial = serial.Serial(port="COM3" , baudrate= self.getDefaultBaudRate())
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

	def setStreamUint8(self, buffer , index , value): #not finished

		buffer [ index + 1 ] = 1
		buffer [ index  ] = 1


	def setStreamUint16(self, buffer , index , value): # not finsihed
		buffer[ index + 3 ] = 1
		buffer[ index + 2 ] = 1
		buffer[ index + 1 ] = 1
		buffer [ index ] = 1

	def setStreamFloat(self , buffer , index , value ): #not finshed
		buffer[ index ] = '+' if value > 0 else '-'
		if value < 0:
			value = -value # check for error later

	def getStreamUint8(self , buffer , index ):
		pass

	def getStreamInt8(self , buffer , index ):
		pass

	def getStreamUint16(self , buffer , index ):
		pass

	def getStreamInt16(self , buffer , index ):
		pass

	def getStreamNumber(self, buffer ,index ):
		pass

	def setStreamTermination(self , buffer , index ):
		pass

	def serialUpdate(self, buffer , messageLength):
		pass

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


