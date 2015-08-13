__author__ = 'Ian'

import math
import wpilib

from wpilib.motorsafety import MotorSafety
from enum import Enum

__all__ = ["Drive"]




# put something in here free motors bla bla


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

		def motorI(self):
			return -1 if self.motorInverted else 1

	kDefaultExpirationTime = 0.1
	kDefaultSensitivity = 0.5
	kDefaultMaxOutput = 1.0

	def __init__( self, FL , FR , RL  , RR  , config):

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
	#Set Functions
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

		self.enabledMotorFix( )

	def setMaxVelocity( self, max ):
		self.MaxV = max * 1.0

	def setPreScale( self, Translation, Rotation ):
		self.prescaleR = Rotation
		self.prescaleT = Translation

	def setSinInverted(self, inverted):
		self.sinInverted = inverted
	#Enable And Disable
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
	#Drive Functions
	def setTranslation( self, X, Y ):
		self.TX = X * math.sqrt( 2 ) * self.prescaleT
		self.TY = Y * self.prescaleT

	def setRotation( self, R ):
		self.TR = R * self.prescaleR

	def pushTransform( self ):
		LX = self.TX
		LY = self.TY
		LR = self.TR
		# implement xy filters here?

		# implement rotation filters here

		forceMag = math.sqrt( (LX * LX) + (LY * LY) )

		ForceAngle = math.atan2( LX, LY )

		ForceAngle += self.PI_DIV_4

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


			self.scaleSpeeds( Speeds )

			self.MInfoFL.setPoint = Speeds[0]
			self.FLMotor.set( Speeds[0] )
			self.MInfoFR.setPoint = Speeds[1]
			self.FRMotor.set( Speeds[1] )
			self.MInfoRL.setPoint = Speeds[2]
			self.RLMotor.set( Speeds[2] )
			self.MInfoRR.setPoint = Speeds[3]
			self.RRMotor.set( Speeds[3] )
	#Get Functions
	def getEnabled( self ):
		return self.enabled

	def getMotorScale( self ):
		return self.Scale


	def getPreScaleT( self ):
		return self.prescaleT

	def getPreScaleR( self ):
		return self.prescaleR

	def getDescription( self ):
		return "Robot Drive"

	def getNumMotors( self ):
		return 4

	#Utility Functions
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

	def scaleSpeeds( self, WheelSpeeds ):
		for i in range( len( WheelSpeeds ) ):
			WheelSpeeds[i] *= self.MaxV

	def configMotors( self ):
		self.CANTalonConfig.configure( self.FLMotor )
		self.CANTalonConfig.configure( self.FRMotor )
		self.CANTalonConfig.configure( self.RLMotor )
		self.CANTalonConfig.configure( self.RRMotor )

	def configSensorI( self ):
		self.FLMotor.reverseSensor( self.MInfoFL.sensorInverted )
		self.FRMotor.reverseSensor( self.MInfoFR.sensorInverted )
		self.RLMotor.reverseSensor( self.MInfoRL.sensorInverted )
		self.RRMotor.reverseSensor( self.MInfoRR.sensorInverted )

	def enabledMotorFix( self ):
		if self.enabled:

			self.configSensorI()

			self.FLMotor.set(
				self.MInfoFL.setPoint * (-1 if self.MInfoFL.motorInverted else 1) )
			self.FRMotor.set(
				self.MInfoFR.setPoint * (-1 if self.MInfoFR.motorInverted else 1) )
			self.RLMotor.set(
				self.MInfoRL.setPoint * (-1 if self.MInfoRL.motorInverted else 1) )
			self.RRMotor.set(
				self.MInfoRR.setPoint * (-1 if self.MInfoRR.motorInverted else 1) )
