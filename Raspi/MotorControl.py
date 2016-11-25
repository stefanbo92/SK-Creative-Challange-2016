import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)


class MotorControl:

    def __init__(self):
        #specify params
        self.forwardSpeed=40
        self.turnSpeed=20
        self.turnTime=0.45

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
        if ul<5:
            #turn left wheel more
            self.pwmLeftA.ChangeDutyCycle(self.turnSpeed)
        elif ul>6 and ul<20:
            #turn right wheel more
            self.pwmRightA.ChangeDutyCycle(self.turnSpeed)
        else:
            #turn same speed
            self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed)
            self.pwmRightA.ChangeDutyCycle(self.forwardSpeed)

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
        
    


