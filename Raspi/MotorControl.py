import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)


class MotorControl:

    def __init__(self):
        #specify params
        self.forwardSpeed=20
        self.turnSpeed=30
        self.turnTime=0.32
        self.wallDist=5
        self.errorOld=0
        self.errorIntegrated=0
        '''
        #working PD control!!!
        self.P=0.2
        self.D=1.5
        '''

        self.P=0.1
        self.D=3.5
        self.I=0
        #init all pins
        # vel=forward (A), dir=backward (B)
        '''
        self.velLeftPin=9 #pin21
        self.dirLeftPin=25 #pin22
        self.velRightPin=11 #pin23
        self.dirRightPin=8 #pin24
        '''
        self.velRightPin=25 #pin22
        self.dirRightPin=9 #pin21
        self.velLeftPin=8 #pin24
        self.dirLeftPin=11 #pin23
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

    def stopHard(self):
        self.pwmLeftA.ChangeDutyCycle(100)
        self.pwmRightA.ChangeDutyCycle(100)
        self.pwmLeftB.ChangeDutyCycle(100)
        self.pwmRightB.ChangeDutyCycle(100)
      
    def moveForward(self,ul,ur,uf):
        self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightA.ChangeDutyCycle(self.forwardSpeed)
        if ul<(self.wallDist-0.5):
            #turn left wheel more
            self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed*1.3)
            print "going right!"
        elif ul>(self.wallDist+0.5) and ul<50:
            #turn right wheel more
            self.pwmRightA.ChangeDutyCycle(self.forwardSpeed*1.3)
            print "going left!"

    def moveForwardControlled(self,ul,ur,uf):
        self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightA.ChangeDutyCycle(self.forwardSpeed)
        #control loop if distance to wall is not appropriate
        if ul<20:
            error=ul-self.wallDist
            if error<=0:
                print ("going right with "+str(1+self.P*-error))
                self.pwmLeftA.ChangeDutyCycle(min([self.forwardSpeed*(1+self.P*-error),self.forwardSpeed*1.4,100]))
            else:
                print ("going left with "+str(1+self.P*error))
                self.pwmRightA.ChangeDutyCycle(min([self.forwardSpeed*(1+self.P*error),self.forwardSpeed*1.4,100]))

    def moveForwardControlledPID(self,ul,ur,uf):
        self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightA.ChangeDutyCycle(self.forwardSpeed)
        #control loop if distance to wall is not appropriate
        if ul<20:
            error=ul-self.wallDist
            self.errorIntegrated+=error
            u=self.P*error+self.D*(error-self.errorOld)+self.I*self.errorIntegrated
            if u<=0:
                print ("going right with "+str((1-u)))
                self.pwmLeftA.ChangeDutyCycle(min([self.forwardSpeed*(1-u),self.forwardSpeed*9.4,100]))
            else:
                print ("going left with "+str((1+u)))
                self.pwmRightA.ChangeDutyCycle(min([self.forwardSpeed*(1+u),self.forwardSpeed*9.4,100]))
            self.errorOld=error

    def moveForwardControlledPIDboth(self,ul,ur,uf):
        self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightA.ChangeDutyCycle(self.forwardSpeed)
        #preliminary check of both ul and ur?
        
        #control loop if distance to left wall is not appropriate
        if ul<20:
            error=ul-self.wallDist
            self.errorIntegrated+=error
            u=self.P*error+self.D*(error-self.errorOld)+self.I*self.errorIntegrated
            if u<=0:
                print ("going right with "+str((1-u)))
                self.pwmLeftA.ChangeDutyCycle(min([self.forwardSpeed*(1-u),self.forwardSpeed*9.4,100]))
            else:
                print ("going left with "+str((1+u)))
                self.pwmRightA.ChangeDutyCycle(min([self.forwardSpeed*(1+u),self.forwardSpeed*9.4,100]))
            self.errorOld=error
        elif ur<20:
            error=ur-self.wallDist
            self.errorIntegrated+=error
            u=self.P*error+self.D*(error-self.errorOld)+self.I*self.errorIntegrated
            if u<=0:
                print ("going left with "+str((1-u)))
                self.pwmRightA.ChangeDutyCycle(min([self.forwardSpeed*(1-u),self.forwardSpeed*9.4,100]))
            else:
                print ("going right with "+str((1+u)))
                self.pwmLeftA.ChangeDutyCycle(min([self.forwardSpeed*(1+u),self.forwardSpeed*9.4,100]))
            self.errorOld=error
            
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
        self.stop()
        time.sleep(0.3)

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
        self.stop()
        time.sleep(0.3)

    def turnBack(self):
        #stop both wheels
        self.stop()
        time.sleep(0.3)
        #turn right wheel backward
        self.pwmRightB.ChangeDutyCycle(self.turnSpeed)
        #turn left wheel forward
        self.pwmLeftA.ChangeDutyCycle(self.turnSpeed)   
        #wait long
        time.sleep(1.71*self.turnTime)
        # stop both wheels
        self.stop()
        time.sleep(0.3)

    def kill(self):
        # Reset GPIO settings
        self.stop()
        GPIO.cleanup()
        



