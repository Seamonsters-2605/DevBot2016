__author__ = 'Ian'

import wpilib
import math
__all_ = ["SmartJoystick"]

class SmartJoystick(wpilib.Joystick):
	def __init__(self, port, AxisDeadband = 0):
		super().__init__( port )
		self.axisDeadBand = AxisDeadband

	def setDeadband(self, deadband):
		self.axisDeadBand = deadband
	def checkDeadband(self, i):
		if math.fabs(i) <= self.axisDeadBand:
			return 0
		else:
			return i

	def getY(self, hand=None ,invert=False):
		return self.checkDeadband(self.getRawAxis(self.axes[self.AxisType.kY])) * -1 if invert else 1

	def getX(self, hand=None , invert=False):
		return self.checkDeadband(self.getRawAxis(self.axes[self.AxisType.kX])) * -1 if invert else 1

	def getZ(self, hand=None, invert = False):
		return self.checkDeadband(self.getRawAxis(self.axes[self.AxisType.kZ])) * -1 if invert else 1