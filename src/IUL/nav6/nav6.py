__author__ = 'Ian'
import math

import serial

from .nav6protocol import *
import threading
import wpilib.timer


class Nav6( ):
    def __init__( self, serialNumber, updateRate ):
        self.stopRequested = False
        self.ser = serial.Serial(serialNumber,self.getDefaultBaudRate())
        self.updateRate = updateRate
        self.yaw = 0
        self.pitch = 0
        self.roll = 0
        self.yOff = 0
        self.pOff = 0
        self.rOff = 0
        self.cHOff = 0
        self.compassHeading = 0
        self.isStopped = True

    def start( self ):
        self.stopRequested = False
        self.thread = threading.Thread(target=self.serialUpdate,name="Nav6")
        self.thread.start()
        self.zero()
        wpilib.timer.Timer.delay(.2)

    def stop( self ):
        self.stopRequested = True

    def _zero(self):
        print('Zeroing Nav6')
        self.yOff = self.calcOffset(self.yaw)
        self.rOff = self.calcOffset(self.roll)
        self.pOff = self.calcOffset(self.pitch)
        self.cHOff = self.compassHeading

    def getRawYaw(self):
        return self.yaw

    def getRawPitch(self):
        return self.pitch

    def getRawRoll(self):
        return self.roll

    def getRawCompassHeading(self):
        return self.compassHeading

    def getYaw( self ):
        return self.convertTo360(self.yaw) - self.yOff

    def getPitch( self ):
        return self.convertTo360(self.pitch) - self.pOff

    def getRoll( self ):
        return self.convertTo360(self.roll) - self.rOff

    def getCompassHeading( self ):
        return self.compassHeading - self.cHOff

    def sendStreamCommand( self, updateRate=10, streamType='y' ):
        buff = [ 0 ] * 9

        buff[ 0 ] = (PACKET_START_CHAR)
        buff[ 1 ] = (MSGID_STREAM_CMD)
        buff[ 2 ] = streamType

        self.setStreamUint8( buff, 3, updateRate )
        self.setStreamTermination( buff, 5 )

        strBuff = ''
        for item in buff:
            strBuff += item
        print( strBuff )

        barray = str.encode(strBuff)

        self.ser.write(barray)
        self.ser.flush()

    def serialUpdate( self ):
        self.isStopped = False
        responce = ""

        self.sendStreamCommand( self.updateRate )

        while (not self.stopRequested):
            self.ser.flushInput()
            responce = self.ser.readline()

            responce = responce.decode()

            if responce[0] != '!':
                continue

            if len(responce) == 34:
                self.decodeRegularResponse(responce)
            else:
                pass

            wpilib.timer.Timer.delay(.02)

        self.isStopped = True

    def decodeRegularResponse( self, strResponce ):
        self.yaw = float(strResponce[2:9])
        self.pitch = float(strResponce[9:16])
        self.roll = float(strResponce[16:23])
        self.compassHeading = float(strResponce[23:30])

    def decodeQuaternionResponse( self, buffer, length ):
        pass

    def setStreamTermination( self, buffer, messageLength ):
        print( buffer )
        self.setStreamUint8( buffer, messageLength, self.calcaulteChecksum( buffer, messageLength ) )
        buffer[ messageLength + 2 ] = '\r'
        buffer[ messageLength + 3 ] = '\n'

    def calcaulteChecksum( self, buffer, length ):
        sum = 0
        for i in range( length ):
            sum += ord( buffer[ i ] )

        if sum >= 256:
            mult = sum // 256
            sum -= mult * 256

        return sum

    def getSerial( self ):
        return self.ser

    def getDefaultBaudRate( self ):
        return 57600

    def calcOffset(self,ypr):
        if ypr == 0:
            return 0
        elif ypr < 0:
            return  360 - abs(ypr)
        return ypr

    def convertTo360(self,value):
        if value < 0:
            return 360 - abs(value)
        return value


    def setStreamUint8( self, buffer, index, value ):
        hexref = '0123456789ABCDEF'
        buffer[ index + 1 ] = (hexref[ value & 0x0F ])
        buffer[ index ] = (hexref[ value >> 4 ])

    def setStreamUint16( self, buffer, index, value ):
        hexRef = '0123456789ABCDEF'
        buffer[ index + 3 ] = ord( hexRef[ value & 0x0F ] )
        buffer[ index + 2 ] = ord( hexRef[ value >> 4 ] )
        buffer[ index + 1 ] = ord( hexRef[ value >> 8 ] )
        buffer[ index ] = ord( hexRef[ (value >> 12) & 0x000F ] )

    def setStreamFloat( self, buffer, index, value ):  # not finshed
        decRef = '0123456789'
        buffer[ index ] = '+' if value > 0 else '-'
        if value < 0:
            value = -value  # check for error later

        buffer[ index + 1 ] = int( decRef[ int( math.fmod( value * 100.0, 10.0 ) ) ] )
        buffer[ index + 1 ] = int( decRef[ int( math.fmod( value * 10.0, 10.0 ) ) ] )
        buffer[ index + 1 ] = int( decRef[ int( math.fmod( value, 10.0 ) ) ] )
        buffer[ index + 4 ] = int( '.' )
        buffer[ index + 1 ] = int( decRef[ int( math.fmod( value / 10.0, 10.0 ) ) ] )
        buffer[ index + 1 ] = int( decRef[ int( math.fmod( value / 100.0, 10.0 ) ) ] )

    def getStreamUint8( self, buffer, index ):
        zeroRef = int( '0' )
        nineRef = int( '9' )
        aRef = int( 'A' )

        value = 0

        if (buffer[ index ] >= zeroRef and buffer[ index ] <= nineRef):
            value = (buffer[ index ] - zeroRef) << 4
        else:
            value = ((buffer[ index ] - aRef) + 10) << 4

        if (buffer[ index + 1 ] >= zeroRef and buffer[ index + 1 ] <= nineRef):
            value += buffer[ index + 1 ] - zeroRef
        else:
            value += (buffer[ index + 1 ] - aRef) + 10

        return value

    def getStreamInt8( self, buffer, index ):
        return int( self.getStreamUint8( buffer, index ) )

    def getStreamUint16( self, buffer, index ):
        value = self.getStreamUint8( buffer, index ) << 8
        value += self.getStreamUint8( buffer, index + 2 )

        return value

    def getStreamInt16( self, buffer, index ):
        return int( self.getStreamUint8( buffer, index ) )
