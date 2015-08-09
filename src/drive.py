__author__ = 'Ian'

import hal
import warnings
import math
import weakref
import wpilib

from wpilib.motorsafety import MotorSafety
from wpilib.talon import Talon
from wpilib.canjaguar import CANJaguar
from enum import Enum

__all__ = ["Drive"]

PI_Div_4 = 0.78539816339


# put something in here free motors bla bla


#class Drive( MotorSafety ):
class Drive( ):
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
		def motorI(self):
			return -1 if self.motorInverted else 1

	kDefaultExpirationTime = 0.1
	kDefaultSensitivity = 0.5
	kDefaultMaxOutput = 1.0

	# kMecanum_Reported = False

	PI_Div_4 = 0.78539816339

	def __init__( self, *args ):
		super( ).__init__( )

		self.enabled = False
		self.powerscale = 1.0
		self.TX = 0.0
		self.TY = 0.0
		self.TR = 0.0
		self.MaxV = 1
		self.prescaleR = 1
		self.prescaleT = 1
		self.sinInverted = False

		if len( args ) == 5:
			self.FLMotor = args[0]
			self.FRMotor = args[1]
			self.RLMotor = args[2]
			self.RRMotor = args[3]
			self.CANTalonConfig = args[4]
		else:
			raise ValueError( "don't know how to handle %d positional arguments" % len( args ) )

		self.MInfoFL = self.MotorInfo( )
		self.MInfoFR = self.MotorInfo( )
		self.MInfoRL = self.MotorInfo( )
		self.MInfoRR = self.MotorInfo( )

		self.configMotors( )
		# other defaults
		self.maxOutput = Drive.kDefaultMaxOutput
		self.sensitivity = Drive.kDefaultSensitivity

		# set up motor safety
		#self.setExpiration( self.kDefaultExpirationTime )
		#self.setSafetyEnabled( True )

	def setTalonConfig( self, CANTalonConfig ):
		self.CANTalonConfig = CANTalonConfig

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

	def setPowerscale( self, powerscale ):
		self.powerscale = powerscale

		self.enabledMotorFix( )

	def configMotors( self ):
		self.CANTalonConfig.Configure( self.FLMotor )
		self.CANTalonConfig.Configure( self.FRMotor )
		self.CANTalonConfig.Configure( self.RLMotor )
		self.CANTalonConfig.Configure( self.RRMotor )

	def configSensorI( self ):
		self.FLMotor.reverseSensor( self.MInfoFL.sensorInverted )
		self.FRMotor.reverseSensor( self.MInfoFR.sensorInverted )
		self.RLMotor.reverseSensor( self.MInfoRL.sensorInverted )
		self.RRMotor.reverseSensor( self.MInfoRR.sensorInverted )

	def enabledMotorFix( self ):
		if self.enabled:
			self.FLMotor.set(
				self.MInfoFL.setPoint * (-self.powerscale if self.MInfoFL.motorInverted else self.powerscale) )
			self.FRMotor.set(
				self.MInfoFR.setPoint * (-self.powerscale if self.MInfoFR.motorInverted else self.powerscale) )
			self.RLMotor.set(
				self.MInfoRL.setPoint * (-self.powerscale if self.MInfoRL.motorInverted else self.powerscale) )
			self.RRMotor.set(
				self.MInfoRR.setPoint * (-self.powerscale if self.MInfoRR.motorInverted else self.powerscale) )

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

	def getEnabled( self ):
		return self.enabled

	def pushTransform( self ):
		LX = self.TX
		LY = self.TY
		LR = self.TR
		# implement xy filters here?

		# implement rotation filters here

		forceMag = math.sqrt( (LX * LX) + (LY * LY) )

		ForceAngle = math.atan2( LX, LY )

		ForceAngle += PI_Div_4

		# implement mag direction filterrrss

		sinCalc = math.sin( ForceAngle ) * forceMag
		cosCalc = math.cos( ForceAngle ) * forceMag

		if self.enabled:
			Speeds = [0] * 4

			Speeds[0] = ((cosCalc if self.sinInverted else sinCalc) + LR) * self.MInfoFL.motorI()
			Speeds[1] = ((sinCalc if self.sinInverted else cosCalc) - LR) * self.MInfoFR.motorI()
			Speeds[2] = ((sinCalc if self.sinInverted else cosCalc) + LR) * self.MInfoRL.motorI()
			Speeds[3] = ((cosCalc if self.sinInverted else sinCalc) - LR) * self.MInfoRR.motorI()

			wpilib.RobotDrive.normalize( Speeds )


			self.ScaleSpeeds( Speeds )

			self.MInfoFL.setPoint = Speeds[0]
			self.FLMotor.set( Speeds[0] )
			self.MInfoFR.setPoint = Speeds[1]
			self.FRMotor.set( Speeds[1] )
			self.MInfoRL.setPoint = Speeds[2]
			self.RLMotor.set( Speeds[2] )
			self.MInfoRR.setPoint = Speeds[3]
			self.RRMotor.set( Speeds[3] )

	def setMaxVelocity( self, max ):
		self.MaxV = max * 1.0

	def getMotorScale( self ):
		return self.Scale

	def setPreScale( self, Translation, Rotation ):
		self.prescaleR = Rotation
		self.prescaleT = Translation

	def setSinInverted(self, inverted):
		self.sinInverted = inverted
	def getPreScaleT( self ):
		return self.prescaleT

	def getPreScaleR( self ):
		return self.prescaleR

	def setTranslation( self, X, Y ):
		self.TX = X * math.sqrt( 2 ) * self.prescaleT
		self.TY = Y * self.prescaleT

	def setRotation( self, R ):
		self.TR = R * self.prescaleR

	def ScaleSpeeds( self, WheelSpeeds ):
		for i in range( len( WheelSpeeds ) ):
			WheelSpeeds[i] *= self.MaxV

	def getDescription( self ):
		return "Robot Drive"

	def stopMotor( self ):

		if self.FLMotor is not None:
			self.FLMotor.set( 0.0 )
		if self.FRMotor is not None:
			self.FRMotor.set( 0.0 )
		if self.RLMotor is not None:
			self.RLMotor.set( 0.0 )
		if self.RRMotor is not None:
			self.RRMotor.set( 0.0 )
		#self.feed( )


	def getNumMotors( self ):
		return 4

