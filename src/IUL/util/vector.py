__author__ = 'Ian'
import math

class Vector:
    def __init__(self,MagDir = None, XY = None, Degrees = False):
        self.magnitude = 0.0
        self.direction = 0.0

        if MagDir != None:
            self.magnitude = MagDir[0]
            if Degrees:
                self.direction = math.radians(MagDir[1])
            else:
                self.direction = MagDir[1]
        elif XY != None:
            self.magnitude,self.direction = self.MDFromXY(XY[0],XY[1])

    def MDFromXY(self,x,y):
        magnitude = math.sqrt(  x**2 + y**2 )
        direction = math.atan2(y,x)

        return magnitude,direction

    def addThis(self, vector):
        x = self.getX() + vector.self.getX()
        y = self.getY() + vector.self.getY()
        return Vector(XY=[x,y])

    def setMagDir(self, Mag, Dir , Degrees = False):
        self.setDirection(Dir, Degrees)
        self.setMagnitude(Mag)

    def setDirection(self,angle,Degrees = False):
        if Degrees:
            self.direction = math.radians(angle)
        else:
            self.direction = angle

    def setMagnitude(self,magnitude):
        self.magnitude = magnitude

    def getX(self):
        return self.magnitude * math.cos(self.direction)

    def getY(self):
        return  self.magnitude * math.sin(self.direction)

    def getMagnitude(self):
        return self.magnitude

    def getDirection(self):
        return self.direction

    def getDirDegrees(self):
        return math.degrees(self.direction)

    @staticmethod
    def add(vector1 , vector2):
        x =vector1.getX() + vector2.getX()
        y = vector1.getX() + vector2.getY()
        return Vector(XY=[x,y])

    def getType(self):
        return "Vector"