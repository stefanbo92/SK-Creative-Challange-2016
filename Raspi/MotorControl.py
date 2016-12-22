import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)


class MotorControl:

    def __init__(self):
        #specify params
        self.forwardSpeed=30
        self.turnSpeed=40
        self.maxSpeed=1.7*self.forwardSpeed
        self.turnTime=0.25#0.32 1.71
        self.wallDist=5
        self.errorOld=0
        self.errorIntegrated=0
        '''
        #working PD control!!!
        self.P=0.1
        self.D=3.5
        '''

        self.P=0.15
        self.I=0.00
        self.D=15

        #evaluation
        self.errorVec=[]
        self.urVec=[]
        self.totalErr=0
        self.count=0
        
        #init all GPIO pins
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
        self.pwmLeftA=GPIO.PWM(self.velLeftPin, 500) # 500Hz PWM
        self.pwmRightA=GPIO.PWM(self.velRightPin, 500)
        self.pwmLeftA.start(0)
        self.pwmRightA.start(0)
        self.pwmLeftB=GPIO.PWM(self.dirLeftPin, 500) # 500Hz PWM
        self.pwmRightB=GPIO.PWM(self.dirRightPin, 500)
        self.pwmLeftB.start(0)
        self.pwmRightB.start(0)
        
    #stop all wheels
    def stop(self):
        self.pwmLeftA.ChangeDutyCycle(0)
        self.pwmRightA.ChangeDutyCycle(0)
        self.pwmLeftB.ChangeDutyCycle(0)
        self.pwmRightB.ChangeDutyCycle(0)

    #make a hard stop on all wheels
    def stopHard(self):
        self.pwmLeftA.ChangeDutyCycle(100)
        self.pwmRightA.ChangeDutyCycle(100)
        self.pwmLeftB.ChangeDutyCycle(100)
        self.pwmRightB.ChangeDutyCycle(100)
        time.sleep(0.5)
        self.stop()

    '''  
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
                self.pwmLeftA.ChangeDutyCycle(min([self.forwardSpeed*(1+self.P*-error),self.maxSpeed,100]))
            else:
                print ("going left with "+str(1+self.P*error))
                self.pwmRightA.ChangeDutyCycle(min([self.forwardSpeed*(1+self.P*error),self.maxSpeed,100]))
    
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
                self.pwmLeftA.ChangeDutyCycle(min([self.forwardSpeed*(1-u),self.maxSpeed,100]))
            else:
                print ("going left with "+str((1+u)))
                self.pwmRightA.ChangeDutyCycle(min([self.forwardSpeed*(1+u),self.maxSpeed,100]))
            self.errorOld=error
    '''

    def moveForwardControlledPIDboth(self,ul,ur,uf):
        self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightA.ChangeDutyCycle(self.forwardSpeed+3)       
        #control loop if distance to left wall is not appropriate
        if ul<20 and ul >3:
            error=ul-self.wallDist
            ### Evaluation
            self.totalErr+=abs(error)
            self.errorVec.append(error)
            self.urVec.append(ur)
            self.count+=1
            ### 
            self.errorIntegrated+=error
            u=self.P*error+self.D*(error-self.errorOld)+self.I*self.errorIntegrated
            if u<=0:
                print ("going right with "+str((1-u)))
                self.pwmLeftA.ChangeDutyCycle(min([self.forwardSpeed*(1-u),self.maxSpeed,100]))
            else:
                print ("going left with "+str((1+u)))
                self.pwmRightA.ChangeDutyCycle(min([self.forwardSpeed*(1+u),self.maxSpeed,100]))
            self.errorOld=error
            time.sleep(0.07)
        elif ur<20:
            error=ur-self.wallDist
            ### Evaluation
            self.totalErr+=abs(error)
            self.errorVec.append(error)
            self.count+=1
            ### 
            self.errorIntegrated+=error
            u=self.P*error+self.D*(error-self.errorOld)+self.I*self.errorIntegrated
            if u<=0:
                print ("going left with "+str((1-u)))
                self.pwmRightA.ChangeDutyCycle(min([self.forwardSpeed*(1-u),self.forwardSpeed*9.4,100]))
            else:
                print ("going right with "+str((1+u)))
                self.pwmLeftA.ChangeDutyCycle(min([self.forwardSpeed*(1+u),self.forwardSpeed*9.4,100]))
            self.errorOld=error
            time.sleep(0.07)
        else:
            time.sleep(0.07)
        #time.sleep(0.08)#time.sleep(0.05)
        self.stop()
        time.sleep(0.02)

    # move both wheels backward        
    def moveBack(self):
        self.pwmLeftB.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightB.ChangeDutyCycle(self.forwardSpeed)

    #move both wheels forward
    def moveFront(self):
        self.pwmLeftA.ChangeDutyCycle(self.forwardSpeed)
        self.pwmRightA.ChangeDutyCycle(self.forwardSpeed+3)

    #make a turn to the left   
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

    #make a turn to the right
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

    #make a 180 degree turn
    def turnBack(self):
        #stop both wheels
        self.stop()
        time.sleep(0.3)
        #turn right wheel backward
        self.pwmRightB.ChangeDutyCycle(self.turnSpeed)
        #turn left wheel forward
        self.pwmLeftA.ChangeDutyCycle(self.turnSpeed)   
        #wait long
        time.sleep(1.8*self.turnTime)
        # stop both wheels
        self.stop()
        time.sleep(0.3)

    # function for plotting the distance of the robot to the wall
    # this can be used for evaluation and parameter tuning
    def plotError(self,errorVec,urVec):
        zeroVec=[]
        wallVec=[]
        contVec=[]

        for i in range(len(errorVec)):
            zeroVec.append(0)
            wallVec.append(self.wallDist)
            contVec.append(i)
            
        plt.plot(contVec,errorVec,contVec,zeroVec)#,contVec,urVec,contVec,wallVec)
        plt.ylabel('error')
        plt.xlabel('timestep')
        plt.show()

    def kill(self):
        # Reset GPIO settings
        self.stop()
        GPIO.cleanup()
        print ("Total average error is: "+str(self.totalErr/self.count))
        #self.plotError(self.errorVec,self.urVec)
        



