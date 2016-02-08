__author__ = 'Ian'

__all__ = [ "CANTalonConfig" ]


class CANTalonConfig:
    def __init__( self, controlmode, feedbacktype=None ):
        self.Mode = controlmode
        self.feedbackType = feedbacktype
        self.controlSlot = 0
        self.P = 0
        self.I = 0
        self.D = 0
        self.F = 0
        self.IZone = 0
        self.sensorInvertedGlobal = False
        self.closedLoopRamp = 0
        self.motorRamp = 0
        self.brake = False
        self.encClickRev = None

    def setGlobalInversion( self, Sensor ):
        self.sensorInvertedGlobal = Sensor

    def setPIDF( self, P, I, D, F ):
        self.P = P
        self.D = D
        self.I = I
        self.F = F

    def setIZone( self, izone ):
        self.IZone = izone

    def setBraking( self, brake=False ):

        self.brake = brake

    def setRampRates( self, motor, closedloop ):
        self.motorRamp = motor
        self.closedLoopRamp = closedloop

    def setControlSlot( self, slot=None ):
        if (slot > 1) or (slot < -1):
            slot = -1
        self.controlSlot = slot

    def isCANTalon( self, CANTalon ):
        if hasattr( CANTalon, "getDescription" ):
            desc = CANTalon.getDescription( )
            if "CANTalon" in desc:
                return True
            else:
                return False
        else:
            return False
    def setEncoderClicksPerRev(self, encoderClicksPerRev):
        self.encClickRev = encoderClicksPerRev

    def configure( self, CANTalon ):
        if not self.isCANTalon( CANTalon ):
            raise ValueError( "did not pass a object of type CANTalon" )

        CANTalon.changeControlMode( self.Mode )

        if self.feedbackType != None:
            CANTalon.setFeedbackDevice( self.feedbackType )

        if self.controlSlot != -1:
            CANTalon.setProfile( self.controlSlot )
            CANTalon.setPID( self.P, self.I, self.D, self.F, self.IZone )

        CANTalon.reverseSensor( self.sensorInvertedGlobal )
        CANTalon.enableBrakeMode( self.brake )

        CANTalon.setPosition(0)
        CANTalon.set( 0 )
        CANTalon.enableControl( )
