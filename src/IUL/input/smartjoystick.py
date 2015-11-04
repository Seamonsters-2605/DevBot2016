__author__ = 'Ian'

import wpilib

__all_ = [ "SmartJoystick" ]


class SmartJoystick( wpilib.Joystick ):
    def __init__( self, port, axisDeadband=0 ):
        super( ).__init__( port )
        self.axisDeadband = axisDeadband

    def setDeadband( self, deadband ):
        self.axisDeadband = deadband

    def checkDeadband( self, joystickValue ):
        if abs( joystickValue ) <= self.axisDeadband:
            return 0.0
        else:
            return joystickValue

    def getY( self, hand=None, inv=False ):
        return self.checkDeadband( self.getRawAxis( self.axes[ self.AxisType.kY ] ) ) * (-1.0 if inv else 1.0)

    def getX( self, hand=None, inv=False ):
        return self.checkDeadband( self.getRawAxis( self.axes[ self.AxisType.kX ] ) ) * (-1.0 if inv else 1.0)

    def getZ( self, hand=None, inv=False ):
        return self.checkDeadband( self.getRawAxis( self.axes[ self.AxisType.kZ ] ) ) * (-1.0 if inv else 1.0)

    def getBolButton( self, bNumber ):
        bNumber = int( bNumber )
        if bNumber < 0 or bNumber > self.getButtonCount( ):
            raise ValueError( "This is not a valid button" )

        if self.getRawButton( bNumber ) == 0:
            return False
        return True
