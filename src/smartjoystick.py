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
		if abs(i) <= self.axisDeadBand:
			return 0.0
		else:
			return i

	def getY(self, hand=None ,inv=False):
		return self.checkDeadband(self.getRawAxis(self.axes[self.AxisType.kY])) * (-1.0 if inv else 1.0)

	def getX(self, hand=None, inv=False):
		"""Get the X value of the joystick.

		This depends on the mapping of the joystick connected to the current
		port.

		:param hand: Unused
		:returns: The X value of the joystick.
		:rtype: float
		"""
		x = self.checkDeadband(self.getRawAxis(self.axes[self.AxisType.kX])) * (-1.0 if inv else 1.0)
		print("X: " + str(x))
		return x

	def getZ(self, hand=None, inv = False):
		return self.checkDeadband(self.getRawAxis(self.axes[self.AxisType.kZ])) * (-1.0 if inv else 1.0)