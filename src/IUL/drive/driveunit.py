__author__ = 'Ian'
import wpilib
from ..util.vector import Vector
import copy
from math import pi
HALF_PI = pi/2.0
TWO_PI = pi*2
class DriveUnit:
    def __init__(self, angleMotor , magMotor , AngleConfig = None , MagnitudeConfig = None , angleTalon = False , magTalon = False , maxV = 1023):
        self.AngUseOpenLoop = False
        self.MagUseOpenLoop = False

        if hasattr(angleMotor, "set"):
            self.angleMotor = angleMotor
            if not hasattr(self.angleMotor, "getDescription"):
                self.AngUseOpenLoop = True
        elif not angleTalon:
            self.angleMotor = wpilib.CANTalon(angleMotor)
        else:
            self.angleMotor = wpilib.Talon(angleMotor)
            self.AngUseOpenLoop = True

        if hasattr(magMotor ,"set"):
            self.magMotor = magMotor
            if not hasattr(magMotor, "getDescription"):
                self.MagUseOpenLoop = True
        elif not magTalon:
            self.magMotor = wpilib.CANTalon(magMotor)
        else:
            self.magMotor = wpilib.Talon(magMotor)
            self.MagUseOpenLoop = True

        #copyConfigs
        if MagnitudeConfig != None:
            self.MagnitudeConfig = copy.deepcopy(MagnitudeConfig)
        else:
            self.MagnitudeConfig = None
        if AngleConfig != None:
            self.AngleConfig = copy.deepcopy(AngleConfig)
        else:
            self.AngleConfig = None

        self.setPointVector = Vector()

        self.maxV = maxV
        self.encClicksRev = 0
        self.clicksPerRadian = 0


    def enable(self):
        try:
            if self.AngleConfig != None:
                self.AngleConfig.configure(self.angleMotor)
        except ValueError:
            self.AngUseOpenLoop = True

        try:
            if self.MagnitudeConfig != None:
                self.MagnitudeConfig.configure(self.magMotor)
        except ValueError:
            self.MagUseOpenLoop = True

        self.enabled = True

        self.setPointVector = Vector()



    def disable(self):
        pass

    def calibrateAngle(self, useSensor = True, sensorAngle = 0.0 ):
        if useSensor:
            pass
        else:
            self.angleMotor.setPosition(0)

    def setMagDir(self, magnitude = None , angle = None , Degrees = False):
        if magnitude == None:
            magnitude = self.getMagnitudeSetpoint()

        if angle == None:
            angle = self.getAngleSetpoint()

        self.setPointVector.setMagDir(magnitude , angle , Degrees)

    def setVector(self, vector):
        if not ( hasattr(vector, "getType") and vector.getType() == "Vector"):
            raise ValueError("You didn't pass the correct data type")
        self.setPointVector = vector

    def getAngleSetpoint(self):
        return self.setPointVector.getDirection()

    def getMagnitudeSetpoint(self):
        return  self.setPointVector.getMagnitude()

    def pushTransform(self):
        if self.MagUseOpenLoop:
            self.magMotor.set(self.getMagnitudeSetpoint())
        else:
            self.magMotor.set(self.getMagnitudeSetpoint() * self.maxV)

        self.setAngleMotor(self.getAngleSetpoint())

    def calculateShift(self,angleA,angleB,inClicks = True):
        angleA = self.normilizeTwoPi(angleA)
        angleB = self.normilizeTwoPi(angleB)
        short = min(abs(abs(angleB - angleA) - TWO_PI), abs(angleB - angleA))
        shift = None
        if self.normilizeTwoPi(angleA + short) == angleB:
            shift = short
        elif self.normilizeTwoPi(angleA - short) == angleB:
            shift = short * -1
        else:
            shift = 9090
            raise ValueError("Something went wrong with the angle shift calc: short: %f shift: %f"%(short, shift))
        if inClicks:
            return self.getClicksFromAngle(shift)
        else:
            return shift

    def setAngleMotor(self, setPoint):
        currentA = self.getCurrentAngle()
        shift = self.calculateShift(currentA , setPoint)
        self.angleMotor.set(self.angleMotor.getSensorPosition() + shift)

    def getClicksFromAngle(self, angle):
        return angle * (self.clicksPerRadian)

    def getCurrentAngle(self):
        """Returns a radian measure constrained on 0 to 2pi"""
        if self.AngUseOpenLoop:
            print("Cannot calculate angle as this is not a CANTalon")
            return 0
        currentClicks = self.angleMotor.getSensorPosition()
        angle = currentClicks / self.clicksPerRadian
        return self.normilizeTwoPi(angle)

    def getType(self):
        return "DriveUnit"

    def getAngleMotor(self):
        return self.angleMotor

    def getMagMotor(self):
        return self.magMotor

    def setMaxVelocity(self, Max):
        self.maxV = Max

    def setEncoderClicksRev(self, clicksRev):
        self.encClicksRev = clicksRev
        self.clicksPerRadian = clicksRev / TWO_PI

    def normilizeTwoPi(self, angle ):
        """Takes an radian measure and constrains it to 0 to two pi."""
        angle = angle % (TWO_PI)
        if angle < 0:
            TWO_PI - abs(angle)
        return angle