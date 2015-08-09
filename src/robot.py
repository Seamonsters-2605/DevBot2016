__author__ = 'Ian'

import wpilib

from drive import Drive
from CANTalonConfig import CANTalonConfig
from smartjoystick import SmartJoystick


class MyRobot( wpilib.IterativeRobot ):
	def robotInit( self ):
		# Motor Config
		self.VelocityConfig = CANTalonConfig( wpilib.CANTalon.ControlMode.Speed,
											  wpilib.CANTalon.FeedbackDevice.QuadEncoder )
		self.VelocityConfig.SetPIDF( 0.5, 0.0, 2.0, 0.0 );
		self.VelocityConfig.SetControlSlot( 0 );
		self.VelocityConfig.SetRampRates( 25.0, 0.0 );
		self.VelocityConfig.SetBrake( True );
		# self.VelocityConfig
		# Motor Declared
		self.M_FL = wpilib.CANTalon( 51 )
		self.M_FR = wpilib.CANTalon( 52 )
		self.M_RL = wpilib.CANTalon( 53 )
		self.M_RR = wpilib.CANTalon( 54 )

		# self.M_FR.reverseSensor(False)
		# self.M_RR.reverseSensor(False)

		# self.M_FR.reverseOutput(True)
		# self.M_RR.reverseOutput(True)
		self.Drive = Drive( self.M_FL, self.M_FR, self.M_RL, self.M_RR, self.VelocityConfig )
		self.Drive.setMotorInversions( False, True, False, True )
		self.Drive.setSensorInversions( False, True, False, True )
		self.Drive.setMaxVelocity( 3000 )



		# Sticks
		self.RightStick = SmartJoystick( 1 , AxisDeadband=0.08)
		self.LeftStick = SmartJoystick( 0  , AxisDeadband=0.08)

	# Drive
	# self.Drive = wpilib.RobotDrive( self.M_FL, self.M_RL, self.M_FR, self.M_RR )
	# self.Drive.setInvertedMotor(1,True)
	# self.Drive.setInvertedMotor(3, True)

	def autonomousInit( self ):
		self.auto_loop_counter = 0

	def autonomousPeriodic( self ):
		pass

	def teleopInit( self ):
		self.Drive.enable()
		print("Enabled")

	def teleopPeriodic( self ):
		self.Drive.setTranslation( self.LeftStick.getX( ), self.LeftStick.getY( ))
		self.Drive.setRotation( self.RightStick.getX( ) )
		self.Drive.pushTransform( )

	def testInit( self ):
		pass

	def testPeriodic( self ):
		pass
	def disabledInit(self):
		self.Drive.disable()

if __name__ == "__main__":
	wpilib.run( MyRobot )
