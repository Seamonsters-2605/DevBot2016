__author__ = 'Ian'

import wpilib

from drive import Drive
from cantalonconfig import CANTalonConfig
from IUL.input.smartjoystick import SmartJoystick
from IUL.filters.filters import *
from IUL.nav6.nav6 import Nav6
from IUL.drive.driveunit import DriveUnit


class MyRobot( wpilib.IterativeRobot ):
    def robotInit( self ):
        # Motor Config
        self.PositionConfig = CANTalonConfig( wpilib.CANTalon.ControlMode.Position,
                                              wpilib.CANTalon.FeedbackDevice.QuadEncoder )
        self.PositionConfig.setPIDF( 0.5, 0.0, 2.0, 0.0 )
        self.PositionConfig.setControlSlot( 0 )
        self.PositionConfig.setRampRates( 25.0, 0.0 )
        self.PositionConfig.setBraking( False )

        self.Drive = DriveUnit(11,2, AngleConfig=self.PositionConfig, magTalon= True)
        self.Drive.setEncoderClicksRev(400000)

        # Sticks
        self.RightStick = SmartJoystick( 1, axisDeadband=0.08 )

        self.SmartDashboard = wpilib.SmartDashboard()


    def autonomousInit( self ):
        pass

    def autonomousPeriodic( self ):
        pass

    def teleopInit( self ):
        self.Drive.enable()
        self.Drive.zeroAngleTo90()
        print( "Enabled" )

    def teleopPeriodic( self ):
        if self.RightStick.getBolButton(3):
            self.Drive.zeroAngleTo90()
        vector = self.RightStick.getVector()
        self.Drive.setVector(vector)

        #print("Angle: %f Mag: %f"%(vector.getDirection(),vector.getMagnitude()))
        self.Drive.pushTransform()



    def testInit( self ):
        pass

    def testPeriodic( self ):
        pass

    def disabledInit( self ):
        self.Drive.disable( )


if __name__ == "__main__":
    wpilib.run( MyRobot )
