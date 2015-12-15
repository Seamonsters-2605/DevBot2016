__author__ = 'Ian'
import wpilib
from ..util.vector import Vector
import copy
from math import pi
import math

class DriveUnit:
    def __init__(self, angleMotor , magMotor , AngleConfig = None , MagnitudeConfig = None  , nav = None , angleTalon = False , magTalon = False , maxV = 1023):

        #NEW ADDITION(S)
        self.DriveBackward = False
        self.DeadZoned = False

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

        self.ZeroedAngle = 0.0
        ######ADDED######

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

    def zeroAngleTo90(self):
        self.ZeroedAngle = self.getCurrentAngle(True, False)

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
        #if self.MagUseOpenLoop:
        #    self.magMotor.set(self.getMagnitude())
        #else:
        #    self.magMotor.set(self.getMagnitude() * self.maxV)

        #calcShortestToAngleSet METHOD ALSO DETERMINES WHETHER OR NOT TO DRIVE FORWARD

        if self.getMagnitude() < .1:
            self.DeadZoned = True
        else:
            self.DeadZoned = False

        short = self.calcShortestToAngleSet(self.getAngle())
        polarity = 1
        if self.DriveBackward:
            polarity = -1

        if self.MagUseOpenLoop:
            self.magMotor.set(self.getMagnitude() * polarity)
        else:
            self.magMotor.set(self.getMagnitude() * self.maxV * polarity)

        self.angleMotor.set(self.getClicksFromAngle(short))

    def calcShortestToAngleSet(self, angle):#Returns the angle the wheel needs to orient itself to, by adding the changed amount to the current angle of the wheel

        pi = math.pi
        self.DriveBackward = False
        DesiredAngle = self.getAngle() - pi / 2 + self.ZeroedAngle
        CurrentAngle = self.getCurrentAngle(False, False)#BOTH ANGLES INCLUDE ZEROING
        CurrentAngleAbsolute = self.getCurrentAngle(True, False)
        print("Angle: " + str(CurrentAngleAbsolute))
        print("Adjustment: " + str(0-pi/2+self.ZeroedAngle))
        print("Adjusted Aim Angle: " + str(DesiredAngle))


        if self.DeadZoned:
            return CurrentAngleAbsolute

        ForwardAngleA = (DesiredAngle-CurrentAngle) % (2*pi)
        ForwardAngleB = (2*pi - abs(ForwardAngleA)) * (-1) * self.getPolarity(ForwardAngleA)#Negative polarity
        BackwardAngleA = (ForwardAngleA + pi) % (2*pi)
        BackwardAngleB = (2*pi-abs(BackwardAngleA)) * (-1) * self.getPolarity(BackwardAngleA)#Negative polarity also
        print(str(self.getCurrentAngle(True, False)))

        shortestPath = ForwardAngleA
        self.DriveBackward = False
        if (abs(ForwardAngleB) < abs(shortestPath)):
            shortestPath = ForwardAngleB
            self.DriveBackward = False
        if (abs(BackwardAngleA) < abs(shortestPath)):
            shortestPath = BackwardAngleA
            self.DriveBackward = True
        if (abs(BackwardAngleB) < abs(shortestPath)):
            shortestPath = BackwardAngleB
            self.DriveBackward = True

        result = shortestPath + CurrentAngleAbsolute#Changed to CurrentAngleAbsolute
        print("Result: " + str(result))
        return result

    def getPolarity(self, number):
        if number >= 0:
            return 1
        return -1

    def getClicksFromAngle(self, angle):
        return angle * (self.clicksPerRadian)

    def getCurrentAngle(self, Absolute = False, IncludeZero = False):
        currentClicks = self.angleMotor.getSensorPosition()
        angle = currentClicks / self.clicksPerRadian

        if IncludeZero:
            angle = angle - self.ZeroedAngle

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