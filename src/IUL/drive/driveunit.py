__author__ = 'Ian'
import wpilib
from ..util.vector import Vector
class DriveUnit:
    def __init__(self, CANAnglePort , CANMagPort , AngleConfig  , MagnitudeConfig  , nav = None):
        self.angleMotor = wpilib.CANTalon(CANAnglePort)
        self.magMotor = wpilib.CANTalon(CANMagPort)
        self.MagnitudeConfig = MagnitudeConfig
        self.AngleConfig = AngleConfig
        self.vector = Vector()

    def enable(self):
        pass

    def disable(self):
        pass

    def zeroAngle(self):
        pass

    def setAngle(self, angle):
        self.vector.setDirection(angle)

    def setMagnitude(self, magnitude):
        self.vector.setMagnitude(magnitude)

    def setMagDir(self, magnitude , angle , Degrees = False):
        self.vector.setMagDir(magnitude , angle , Degrees)

    def setVector(self, vector):
        if not ( hasattr(vector, "getType") and vector.getType() == "Vector"):
            raise ValueError("You didn't pass the correct data type")

    def getAngle(self):
        pass

    def getMagnitude(self):
        pass

    def pushTransform(self):
        pass

    def getType(self):
        return "DriveUnit"
