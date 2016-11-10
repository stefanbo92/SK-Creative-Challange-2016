##
##    The class MazeControl will make the robot move through the maze.
##    In order to use it just create a MazeControl object and constantly
##    call moveMaze(ul,ur,uf), where ul, ur and uf are filtered ultrasonic
##    distances in cm of left, right and front sensor:
##
##        mc=MazeControl()
##        sr=SensorReader(5)
##        while True:
##            ul,ur,uf =sr.getSensorReadings()
##            mc.moveMaze(ul,ur,uf)
##
   
import numpy as np
import time
import wiringpi

class MazeControl:

    def __init__(self):
        #specify params
        self.forwardSpeed=0.6
        self.turnSpeed=0.8
        self.turnTime=1.0

        #init all pins
        self.velLeftPin=1
        self.dirLeftPin=2
        self.velRightPin=3
        self.dirRightPin=4
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(velLeftPin, 2)
        wiringpi.pinMode(dirLeftPin, 2)
        wiringpi.pinMode(velRightPin, 2)
        wiringpi.pinMode(dirRightPin, 2)

        #initially set both motors to forward
        wiringpi.digitalWrite(dirLeftPin, 1.)
        wiringpi.digitalWrite(dirRightPin, 1.)


    # ul, ur, uf are filtered ultrasonic distances in cm of left,
    # right and front sensor
    def moveMaze(self,ul,ur,uf):
        # edit for better algorithm
        if uf>3:
            self.moveForward(ul,ur,uf)
        elif ul>5:
            self.turnLeft()
        elif ur>5:
            self.turnRight()
        else:
            self.turnBack()

    def moveForward(self,ul,ur,uf):
        if ul<2:
            #turn left wheel more
            wiringpi.digitalWrite(motorLeftPin, turnSpeed)
        elif ul>4 and ul<20:
            #turn right wheel more
            wiringpi.digitalWrite(motorRightPin, turnSpeed)
        else:
            #turn same speed
            wiringpi.digitalWrite(motorLeftPin, forwardSpeed)
            wiringpi.digitalWrite(motorRightPin, forwardSpeed)

    def turnLeft(self):
        #turn right wheel forward
        wiringpi.digitalWrite(motorRightPin, turnSpeed)
        #turn left wheel backward
        wiringpi.digitalWrite(dirLeftPin, 0)
        wiringpi.digitalWrite(motorLeftPin, turnSpeed)
        #wait
        time.sleep(turnTime)
        # stop both wheels
        wiringpi.digitalWrite(motorRightPin, 0.)
        wiringpi.digitalWrite(dirLeftPin, 1.)
        wiringpi.digitalWrite(motorLeftPin, 0.)

    def turnRight(self):
        #turn right wheel backward
        wiringpi.digitalWrite(dirRightPin, 0)
        wiringpi.digitalWrite(motorRightPin, turnSpeed)
        #turn left wheel forward
        wiringpi.digitalWrite(motorLeftPin, turnSpeed)
        #wait
        time.sleep(turnTime)
        # stop both wheels
        wiringpi.digitalWrite(motorLeftPin, 0.)
        wiringpi.digitalWrite(dirRightPin, 1.)
        wiringpi.digitalWrite(motorRightPin, 0.)

    def turnBack(self):
        #turn right wheel backward
        wiringpi.digitalWrite(dirRightPin, 0)
        wiringpi.digitalWrite(motorRightPin, turnSpeed)
        #turn left wheel forward
        wiringpi.digitalWrite(motorLeftPin, turnSpeed)
        #wait long
        time.sleep(2*turnTime)
        # stop both wheels
        wiringpi.digitalWrite(motorLeftPin, 0.)
        wiringpi.digitalWrite(dirRightPin, 1.)
        wiringpi.digitalWrite(motorRightPin, 0.)

    def __exit__(self, exc_type, exc_value, traceback):
        # Reset GPIO settings
        #GPIO.cleanup()
        wiringpi.pinMode(velLeftPin, 0)
        wiringpi.pinMode(dirLeftPin, 0)
        wiringpi.pinMode(velRightPin, 0)
        wiringpi.pinMode(dirRightPin, 0)
    


