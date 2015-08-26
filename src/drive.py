__author__ = 'Ian'

import math
import wpilib

# from wpilib.motorsafety import MotorSafety #Implement this in the future

from enum import Enum

__all__ = ["Drive"]


class Drive( ):
	PI_DIV_4 = math.pi / 4.0

	class MotorPosition( Enum ):
		kFrontLeft = 0
		kFrontRight = 1
		kRearLeft = 2
		kRearRight = 3

	class MotorInfo:
		def __init__( self ):
			self.sensorInverted = False
			self.motorInverted = False

			self.setPoint = 0.0

		def motorI( self ):
			return -1 if self.motorInverted else 1

	kDefaultExpirationTime = 0.1
	kDefaultSensitivity = 0.5
	kDefaultMaxOutput = 1.0

	acceptedFilterTypes = ["1_1", "2_2"]

	def __init__( self, FL, FR, RL, RR, config ):

		super( ).__init__( )

		self.FLMotor = FL
		self.FRMotor = FR
		self.RLMotor = RL
		self.RRMotor = RR
		self.config = config

		self.enabled = False

		self.TX = 0.0
		self.TY = 0.0
		self.TR = 0.0
		self.MaxV = 1

		self.prescaleR = 1
		self.prescaleT = 1

		self.sinInverted = False

		self.MInfoFL = self.MotorInfo( )
		self.MInfoFR = self.MotorInfo( )
		self.MInfoRL = self.MotorInfo( )
		self.MInfoRR = self.MotorInfo( )

		self.XYFilter = None
		self.RFilter = None
		self.MDFilter = None

	# Set Functions
	def setTalonConfig( self, CANTalonConfig ):
		self.config = CANTalonConfig

		self.configMotors( )

	def setMotorInversions( self, FL, FR, RL, RR ):
		self.MInfoFL.motorInverted = FL
		self.MInfoFR.motorInverted = FR
		self.MInfoRL.motorInverted = RL
		self.MInfoRR.motorInverted = RR

		self.enabledMotorFix( )

	def setSensorInversions( self, FL, FR, RL, RR ):
		self.MInfoFL.sensorInverted = FL
		self.MInfoFR.sensorInverted = FR
		self.MInfoRL.sensorInverted = RL
		self.MInfoRR.sensorInverted = RR

		self.enabledMotorFix( )

	def setMaxVelocity( self, max ):
		self.MaxV = max * 1.0

	def setPreScale( self, Translation, Rotation ):
		self.prescaleR = Rotation
		self.prescaleT = Translation

	def setSinInverted( self, inverted ):
		self.sinInverted = inverted

	# Enable And Disable
	def enable( self ):
		self.enabled = True
		self.configMotors( )
		self.configSensorI( )

	def disable( self ):
		self.enabled = False
		self.MInfoFL.setPoint = 0.0
		self.FLMotor.set( 0.0 )
		self.MInfoFR.setPoint = 0.0
		self.FRMotor.set( 0.0 )
		self.MInfoRL.setPoint = 0.0
		self.RLMotor.set( 0.0 )
		self.MInfoRR.setPoint = 0.0
		self.RRMotor.set( 0.0 )

	# Drive Functions
	def setTranslation( self, X, Y ):
		self.TX = X * math.sqrt( 2 ) * self.prescaleT
		self.TY = Y * self.prescaleT

	def setRotation( self, R ):
		self.TR = R * self.prescaleR

	def pushTransform( self ):
		LX = self.TX
		LY = self.TY
		LR = self.TR

		# XY filters
		if self.XYFilter != None:
			for filter in self.XYFilter:
				filter.compute( LX, LY )
				LX = filter.readA( )
				LY = filter.readB( )
				
		# Rotation filters
		if self.RFilter != None:
			for filter in self.RFilter:
				filter.compute( LR )
				LR = filter.readA( )

		forceMag = math.sqrt( (LX * LX) + (LY * LY) )

		forceAngle = math.atan2( LX, LY )

		forceAngle += Drive.PI_DIV_4

		# Magnitude / Direction filters
		if self.MDFilter != None:
			for filter in self.MDFilter:
				filter.compute( forceMag, forceAngle )
				forceMag = filter.readA( )
				forceAngle = filter.readB( )

		sinCalc = math.sin( forceAngle ) * forceMag
		cosCalc = math.cos( forceAngle ) * forceMag

		if self.enabled:
			Speeds = [0] * 4

			Speeds[0] = ((cosCalc if self.sinInverted else sinCalc) + LR) * self.MInfoFL.motorI( )
			Speeds[1] = ((sinCalc if self.sinInverted else cosCalc) - LR) * self.MInfoFR.motorI( )
			Speeds[2] = ((sinCalc if self.sinInverted else cosCalc) + LR) * self.MInfoRL.motorI( )
			Speeds[3] = ((cosCalc if self.sinInverted else sinCalc) - LR) * self.MInfoRR.motorI( )

			wpilib.RobotDrive.normalize( Speeds )

			self.scaleSpeeds( Speeds )

			self.MInfoFL.setPoint = Speeds[0]
			self.FLMotor.set( Speeds[0] )
			self.MInfoFR.setPoint = Speeds[1]
			self.FRMotor.set( Speeds[1] )
			self.MInfoRL.setPoint = Speeds[2]
			self.RLMotor.set( Speeds[2] )
			self.MInfoRR.setPoint = Speeds[3]
			self.RRMotor.set( Speeds[3] )

	# Get Functions
	def getEnabled( self ):
		return self.enabled

	def getMotorScale( self ):
		return self.MaxV

	def getPreScaleT( self ):
		return self.prescaleT

	def getPreScaleR( self ):
		return self.prescaleR

	def getDescription( self ):
		return "Robot Drive"

	def getNumMotors( self ):
		return 4

	# Utility Functions
	def stopMotor( self ):
		if self.FLMotor is not None:
			self.FLMotor.set( 0.0 )
		if self.FRMotor is not None:
			self.FRMotor.set( 0.0 )
		if self.RLMotor is not None:
			self.RLMotor.set( 0.0 )
		if self.RRMotor is not None:
			self.RRMotor.set( 0.0 )

	def scaleSpeeds( self, WheelSpeeds ):
		for i in range( len( WheelSpeeds ) ):
			WheelSpeeds[i] *= self.MaxV

	def configMotors( self ):
		self.config.configure( self.FLMotor )
		self.config.configure( self.FRMotor )
		self.config.configure( self.RLMotor )
		self.config.configure( self.RRMotor )

	def configSensorI( self ):
		self.FLMotor.reverseSensor( self.MInfoFL.sensorInverted )
		self.FRMotor.reverseSensor( self.MInfoFR.sensorInverted )
		self.RLMotor.reverseSensor( self.MInfoRL.sensorInverted )
		self.RRMotor.reverseSensor( self.MInfoRR.sensorInverted )

	def enabledMotorFix( self ):
		if self.enabled:
			self.configSensorI( )

			self.FLMotor.set( self.MInfoFL.setPoint * (-1 if self.MInfoFL.motorInverted else 1) )
			self.FRMotor.set( self.MInfoFR.setPoint * (-1 if self.MInfoFR.motorInverted else 1) )
			self.RLMotor.set( self.MInfoRL.setPoint * (-1 if self.MInfoRL.motorInverted else 1) )
			self.RRMotor.set( self.MInfoRR.setPoint * (-1 if self.MInfoRR.motorInverted else 1) )

	def checkFilterType( self, filter ):
		if hasattr( filter, "getType" ):
			if filter.getType( ) not in self.acceptedFilterTypes:
				raise ValueError( "That is not a valid type of filter fo this application" )
			return filter.getType( )
		else:
			raise ValueError( "did not pass in a valid filter" )

	def addXYFilter( self, filter ):
		if filter != None and self.checkFilterType( filter ) == "2_2":
			if self.XYFilter == None:
				self.XYFilter = []
			self.XYFilter.append( filter )

	def removeXYFilter( self, filter ):
		# note this only gets the first index of that filter, same for all of the remove functions
		if filter != None and self.checkFilterType( filter ) == "2_2":
			ind = self.XYFilter.index( filter )
			if ind != -1:
				self.XYFilter.pop( ind )
				if len( self.XYFilter ) == 0:  # separate this out into its own function at some point..
					self.XYFilter = None
	def addRFilter( self, filter ):
		if filter != None and self.checkFilterType( filter ) == "1_1":
			if self.RFilter == None:
				self.RFilter = []
			self.RFilter.append( filter )

	def removeRFilter( self, filter ):
		if filter != None and self.checkFilterType( filter ) == "1_1":
			ind = self.RFilter.index( filter )
			if ind != -1:
				self.RFilter.pop( ind )
				if len( self.RFilter ) == 0:
					self.RFilter = None

	def addMDFilter( self, filter ):
		if filter != None and self.checkFilterType( filter ) == "2_2":
			if self.MDFilter == None:
				self.MDFilter = []
			self.MDFilter.append( filter )

	def removeMDFilter( self, filter ):
		if filter != None and self.checkFilterType( filter ) == "2_2":
			ind = self.MDFilter.index( filter )
			if ind != -1:
				self.MDFilter.pop( ind )
				if len( self.MDFilter ) == 0:
					self.MDFilter = None
