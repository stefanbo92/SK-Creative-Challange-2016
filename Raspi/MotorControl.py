import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)


class MotorControl:

    def __init__(self):
        #specify params
        self.forwardSpeed=40
        self.turnSpeed=35
        self.turnTime=0.45
        self.wallDist=15
        self.P=0.05

        #init all pins
        # vel=forward (A), dir=backward (B)
        self.velLeftPin=9 #pin21
        self.dirLeftPin=25 #pin22
        self.velRightPin=11 #pin23
        self.dirRightPin=8 #pin24
        GPIO.setup(self.velLeftPin,GPIO.OUT)  
        GPIO.setup(self.dirLeftPin,GPIO.OUT)
        GPIO.setup(self.velRightPin,GPIO.OUT)  
        GPIO.setup(self.dirRightPin,GPIO.OUT)

        # init PWM pins
        self.pwmLeftA=GPIO.PWM(self.velLeftPin, 50) # 50Hz PWM
        self.pwmRightA=GPIO.PWM(self.velRightPin, 50)
        self.pwmLeftA.start(0)
        self.pwmRightA.start(0)
        self.pwmLeftB=GPIO.PWM(self.dirLeftPin, 50) # 50Hz PWM
        self.pwmRightB=GPIO.PWM(self.dirRightPin, 50)
        self.pwmLeftB.start(0)
        self.pwmRightB.start(0)
        

    def stop(self):
        self.pwmLeftA.ChangeDutyCycle(0)
        self.pwmRightA.ChangeDutyCycle(0)
        self.pwmLeftB.ChangeDutyCycle(0)
        self.pwmRightB.ChangeDutyCycle(0)
        
    def moveForward(self,ul,ur,uf):
        self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightA.ChangeDutyCycle(self.forwardSpeed)
        if ul<self.wallDist:
            #turn left wheel more
            self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed*1.2)
            print "going right!"
        elif ul>self.wallDist and ul<50:
            #turn right wheel more
            self.pwmRightA.ChangeDutyCycle(self.forwardSpeed*1.2)
            print "going left!"

    def moveForwardControlled(self,ul,ur,uf):
        self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightA.ChangeDutyCycle(self.forwardSpeed)
        #control loop if distance to wall is not appropriate
        if ul<50:
            error=ul-self.wallDist
            if error<=0:
                print "going right"
                self.pwmLeftA.ChangeDutyCycle(min([self.forwardSpeed*(1+self.P*-error),self.forwardSpeed*1.4,100]))
            else:
                print "going left"
                self.pwmRightA.ChangeDutyCycle(min([self.forwardSpeed*(1+self.P*error),self.forwardSpeed*1.4,100]))

    def moveBack(self):
        self.pwmLeftB.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightB.ChangeDutyCycle(self.forwardSpeed)
        
    def turnLeft(self):
        #stop both wheels
        self.stop()
        time.sleep(0.3)
        #turn right wheel forward
        self.pwmRightA.ChangeDutyCycle(self.turnSpeed)
        #turn left wheel backward
        self.pwmLeftB.ChangeDutyCycle(self.turnSpeed)
        #wait
        time.sleep(self.turnTime)
        # stop both wheels
        self.pwmRightA.ChangeDutyCycle(0)
        self.pwmLeftB.ChangeDutyCycle(0)

    def turnRight(self):
        #stop both wheels
        self.stop()
        time.sleep(0.3)
        #turn right wheel backward
        self.pwmRightB.ChangeDutyCycle(self.turnSpeed)
        #turn left wheel forward
        self.pwmLeftA.ChangeDutyCycle(self.turnSpeed)   
        #wait
        time.sleep(self.turnTime)
        # stop both wheels
        self.pwmRightB.ChangeDutyCycle(0)
        self.pwmLeftA.ChangeDutyCycle(0)

    def turnBack(self):
        #stop both wheels
        self.stop()
        time.sleep(0.3)
        #turn right wheel backward
        self.pwmRightB.ChangeDutyCycle(self.turnSpeed)
        #turn left wheel forward
        self.pwmLeftA.ChangeDutyCycle(self.turnSpeed)   
        #wait long
        time.sleep(1.86*self.turnTime)
        # stop both wheels
        self.pwmRightB.ChangeDutyCycle(0)
        self.pwmLeftA.ChangeDutyCycle(0)

    def kill(self):
        # Reset GPIO settings
        self.stop()
        GPIO.cleanup()
        
    


