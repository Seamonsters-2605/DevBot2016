__author__ = 'Ian'

import wpilib

from drive import Drive
from cantalonconfig import CANTalonConfig
from IUL.input.smartjoystick import SmartJoystick
from IUL.filters.filters import *
from IUL.nav6.nav6 import Nav6


class MyRobot( wpilib.IterativeRobot ):
    def robotInit( self ):
        # Motor Config
        self.VelocityConfig = CANTalonConfig( wpilib.CANTalon.ControlMode.Speed,
                                              wpilib.CANTalon.FeedbackDevice.QuadEncoder )
        self.VelocityConfig.setPIDF( 0.5, 0.0, 2.0, 0.0 )
        self.VelocityConfig.setControlSlot( 0 )
        self.VelocityConfig.setRampRates( 25.0, 0.0 )
        self.VelocityConfig.setBraking( True )
        # self.VelocityConfig
        # Motor Declared
        self.M_FL = wpilib.CANTalon( 51 )
        self.M_FR = wpilib.CANTalon( 52 )
        self.M_RL = wpilib.CANTalon( 53 )
        self.M_RR = wpilib.CANTalon( 54 )

        self.lift = wpilib.CANTalon( 41 )

        self.vProfile = MecanumVelocityProfile( 2 )
        self.strafeTVP = MecanumXYTVPFilter( 4 )

        self.Drive = Drive( self.M_FL, self.M_FR, self.M_RL, self.M_RR, self.VelocityConfig )
        self.Drive.setMotorInversions( False, True, False, True )
        self.Drive.setSensorInversions( False, True, False, True )
        self.Drive.setMaxVelocity( 1023 )
        self.Drive.addMDFilter( self.vProfile )
        self.Drive.addXYFilter( self.strafeTVP )

        # Sticks
        self.RightStick = SmartJoystick( 1, axisDeadband=0.08 )
        self.LeftStick = SmartJoystick( 0, axisDeadband=0.08 )

        self.nav = Nav6(0,15)

    # Drive
    # self.Drive = wpilib.RobotDrive( self.M_FL, self.M_RL, self.M_FR, self.M_RR )
    # self.Drive.setInvertedMotor(1,True)
    # self.Drive.setInvertedMotor(3, True)

    def autonomousInit( self ):
        self.auto_loop_counter = 0

    def autonomousPeriodic( self ):
        pass

    def teleopInit( self ):
        self.Drive.enable( )
        print( "Enabled" )

    def teleopPeriodic( self ):
        if self.LeftStick.getBolButton( 1 ):
            self.lift.set( 1 )
        elif self.LeftStick.getBolButton( 2 ):
            self.lift.set( -1 )
        else:
            self.lift.set( 0 )

        self.Drive.setTranslation( self.LeftStick.getX( ), self.LeftStick.getY( inv=True ) )
        self.Drive.setRotation( self.RightStick.getX( ) )
        self.Drive.pushTransform( )

    def testInit( self ):
        pass

    def testPeriodic( self ):
        pass

    def disabledInit( self ):
        self.Drive.disable( )


if __name__ == "__main__":
    wpilib.run( MyRobot )
