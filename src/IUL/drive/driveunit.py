__author__ = 'Ian'
import wpilib
from ..util.vector import Vector
import copy
from math import pi

class DriveUnit:
    def __init__(self, angleMotor , magMotor , AngleConfig = None , MagnitudeConfig = None  , nav = None , angleTalon = False , magTalon = False , maxV = 1023):
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

        self.nav = nav
        self.enabled = False

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

    def zeroAngle(self):
        pass

    def setAngle(self, angle):
        self.setPointVector.setDirection(angle)

    def setMagnitude(self, magnitude):
        self.setPointVector.setMagnitude(magnitude)

    def setMagDir(self, magnitude , angle , Degrees = False):
        self.setPointVector.setMagDir(magnitude , angle , Degrees)

    def setVector(self, vector):
        if not ( hasattr(vector, "getType") and vector.getType() == "Vector"):
            raise ValueError("You didn't pass the correct data type")
        self.setPointVector = vector

    def getAngle(self):
        return self.setPointVector.getDirection()

    def getMagnitude(self):
        return  self.setPointVector.getMagnitude()

    def pushTransform(self):
        if self.MagUseOpenLoop:
            self.magMotor.set(self.getMagnitude())
        else:
            self.magMotor.set(self.getMagnitude() * self.maxV)
        short = self.clacShortestToAngleSet(self.getAngle())
        self.angleMotor.set(self.getClicksFromAngle(short))

    def clacShortestToAngleSet(self, angle):
        #nonworking
        currentA = self.getCurrentAngle()
        angle = -(pi - abs((currentA - angle) - pi))
        return angle + currentA



    def getClicksFromAngle(self, angle):
        return angle * (self.clicksPerRadian)

    def getCurrentAngle(self, Absolute = False):
        currentClicks = self.angleMotor.getSensorPosition()
        angle = currentClicks / self.clicksPerRadian
        if Absolute:
            return angle

        rAngle = angle % (2*pi)
        return rAngle


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
        self.clicksPerRadian = clicksRev / (2*pi)