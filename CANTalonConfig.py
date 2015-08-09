__author__ = 'Ian'

__all__ = ["CANTalonConfig"]

class CANTalonConfig:
	def __init__( self, controlmode, feedbacktype=None ):
		self.Mode = controlmode
		self.FeedbackType = feedbacktype
		self.ControlSlot = 0
		self.P = 0
		self.I = 0
		self.D = 0
		self.F = 0
		self.IZone = 0
		self.SensorInvertedGlobal = False
		self.ClosedLoopRamp = 0
		self.MotorRamp = 0
		self.Brake = False

	def SetGlobalInversion( self, Sensor ):
		self.SensorInvertedGlobal = Sensor

	def SetPIDF( self, P, I, D, F ):
		self.P = P
		self.D = D
		self.I = I
		self.F = F

	def SetBrake( self, brake ):
		self.Brake = brake

	def SetIZone( self, izone ):
		self.IZone = izone

	def SetRampRates( self, motor, closedloop ):
		self.MotorRamp = motor
		self.ClosedLoopRamp = closedloop

	def SetControlSlot( self, slot ):
		if (slot > 1) or (slot < -1):
			slot = -1
		self.ControlSlot = slot

	def Configure( self, CANTalon ):
		CANTalon.changeControlMode( self.Mode )
		if self.FeedbackType != None:
			CANTalon.setFeedbackDevice = self.FeedbackType
		if self.ControlSlot != -1:
			CANTalon.setProfile( self.ControlSlot )
			CANTalon.setPID( self.P, self.I, self.D, self.F, self.IZone )
		CANTalon.reverseSensor( self.SensorInvertedGlobal )
		CANTalon.enableBrakeMode( self.Brake )

		CANTalon.set( 0 )
		CANTalon.enableControl( )
