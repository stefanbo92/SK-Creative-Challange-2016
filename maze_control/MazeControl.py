##
##    The class MazeControl will make the robot move through the maze.
##    In order to use it just create a MazeControl object and constantly
##    call moveMaze(ul,ur,uf), where ul, ur and uf are filtered ultrasonic
##    distances in cm of left, right and front sensor:
##
##        mc=MazeControl()
##        while True:
##            ul,ur,uf =getSensorReadings()
##            mc.moveMaze(ul,ur,uf)
##
   
import numpy as np
import time
import wiringpi

class MazeControl:

    def __init__(self):
        #specify params
        forwardSpeed=0.6
        turnSpeed=0.8
        turnTime=1.0

        #init all pins
        velLeftPin=1
        dirLeftPin=2
        velRightPin=3
        dirRightPin=4
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
    def moveMaze(ul,ur,uf):
        # edit for better algorithm
        if uf>3:
            moveForward(ul,ur,uf)
        elif ul>5:
            turnLeft()
        elif ur>5:
            turnRight()
        else:
            turnBack()

    def moveForward(ul,ur,uf):
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

    def turnLeft():
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

    def turnRight():
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

    def turnBack():
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
    


