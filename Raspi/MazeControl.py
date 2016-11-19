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
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)


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
        GPIO.setup(self.velLeftPin,GPIO.OUT)  
        GPIO.setup(self.dirLeftPin,GPIO.OUT)
        GPIO.setup(self.velRightPin,GPIO.OUT)  
        GPIO.setup(self.dirRightPin,GPIO.OUT)

        # init PWM pins
        self.pwmLeft=GPIO.PWM(self.velLeftPin, 500) # 500Hz PWM
        self.pwmRight=GPIO.PWM(self.velRightPin, 500)
        self.pwmLeft.start(0)
        self.pwmRight.start(0)
        
        #initially set both motors to forward
        GPIO.output(self.dirLeftPin, 1)
        GPIO.output(self.dirRightPin, 1)

        # init object detection
        
        # detectionMode
        # 0: default (no sign detected)
        # 1: left sign detected
        # 2: right sign detected
        # 3: front sign detected
        # 4: backward sign detected
        self.detectionMode=0  


    # ul, ur, uf are filtered ultrasonic distances in cm of left,
    # right and front sensor
    def moveMaze(self,ul,ur,uf):
        # edit for better algorithm
        if self.detectionMode==1:
            # algorithm for keeping left
        elif self.detectionMode==2:
            # algorithm for keeping right
        elif self.detectionMode==3:
            #move default
            self.moveDefault(ul,ur,uf)
        elif self.detectionMode==4:
            #turn around
            self.turnBack()
        else:
            self.moveDefault(ul,ur,uf)

    def moveDefault(self,ul,ur,uf):
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
            self.pwmLeft.ChangeDutyCycle(self.turnSpeed)
        elif ul>4 and ul<20:
            #turn right wheel more
            self.pwmRight.ChangeDutyCycle(self.turnSpeed)
        else:
            #turn same speed
            self.pwmLeft.ChangeDutyCycle(self.forwardSpeed)
            self.pwmRight.ChangeDutyCycle(self.forwardSpeed)

    def turnLeft(self):
        #turn right wheel forward
        self.pwmRight.ChangeDutyCycle(self.turnSpeed)
        #turn left wheel backward
        GPIO.output(self.dirLeftPin, 0)
        self.pwmLeft.ChangeDutyCycle(self.turnSpeed)
        #wait
        time.sleep(self.turnTime)
        # stop both wheels
        self.pwmRight.ChangeDutyCycle(0)
        GPIO.output(self.dirLeftPin, 1)
        self.pwmLeft.ChangeDutyCycle(0)

    def turnRight(self):
        #turn right wheel backward
        GPIO.output(self.dirRightPin, 0)
        self.pwmRight.ChangeDutyCycle(self.turnSpeed)
        #turn left wheel forward
        self.pwmLeft.ChangeDutyCycle(self.turnSpeed)
        #wait
        time.sleep(self.turnTime)
        # stop both wheels
        self.pwmRight.ChangeDutyCycle(0)
        GPIO.output(self.dirRightPin, 1)
        self.pwmLeft.ChangeDutyCycle(0)

    def turnBack(self):
        #turn right wheel backward
        GPIO.output(self.dirRightPin, 0)
        self.pwmRight.ChangeDutyCycle(self.turnSpeed)
        #turn left wheel forward
        self.pwmLeft.ChangeDutyCycle(self.turnSpeed)
        #wait long
        time.sleep(2*self.turnTime)
        # stop both wheels
        self.pwmRight.ChangeDutyCycle(0)
        GPIO.output(self.dirRightPin, 1)
        self.pwmLeft.ChangeDutyCycle(0)

    def kill(self):
        # Reset GPIO settings
        self.pwmLeft.stop()
        self.pwmRight.stop()
        GPIO.cleanup()
        
    


