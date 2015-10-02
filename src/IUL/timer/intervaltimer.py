__author__ = 'Ian'

from wpilib import Timer

__all__ = [ "IntervalTimer" ]


class IntervalTimer:
    def _init__( self ):
        self.time = 0.0
        self.offset = 0.0
        self.running = False

    def start( self ):
        if self.running:
            return
        self.offset = Timer.getMsClock( )
        self.running = True

    def stop( self ):
        current = Timer.getMsClock( )

        self.offset = current - self.offset

        self.time = self.offset

        self.running = False

    def reset( self ):
        self.running = False
        self.time = 0.0

    def restart( self ):
        self.offset = Timer.getMsClock( )

        self.time = 0.0
        self.running = True

    def getTimeMS( self ):
        current = Timer.getMsClock( )

        current -= self.offset
        current += self.time
        return float( current )
