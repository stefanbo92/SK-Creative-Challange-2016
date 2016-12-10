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
   
import time
import MotorControl
import SignDetector
import SensorReader



class MazeControl:

    def __init__(self):
        #create Motor controller
        self.filterLength=5
        #self.delayTime=0.3
        self.delaySteps=8
        self.frontDist=7.2
        self.mc=MotorControl.MotorControl()
        self.sd=SignDetector.SignDetector()
        self.sr=SensorReader.SensorReader(self.filterLength)

        #init filter
        for i in range(self.filterLength):
            self.sr.getSensorReadings()

        # init object detection
        
        # detectionMode
        # 0: default (no sign detected)
        # 1: left sign detected
        # 2: right sign detected
        # 3: treasure
        # 4: backward sign detected
        # 5: bomb
        self.detectionMode=0    
        self.detectionStep=3#20
        self.detectionCount=self.detectionStep


    #refreshing SensorReadings
    def refreshSensors(self):
        for i in range(self.filterLength):
            self.sr.getSensorReadings()
            
    # ul, ur, uf are filtered ultrasonic distances in cm of left,
    # right and front sensor
    def moveMaze(self):
        #get sensor readings
        ul,ur,uf=self.sr.getSensorReadings()
        print (str(ul)+" "+str(ur)+" "+str(uf))
        print ("detection mode: "+str(self.detectionMode))
        #update video buffer
        #self.sd.grabImage()

        #make sign detection each 'self.detectionStep' step
        if self.detectionCount==self.detectionStep:
            self.detectionCount=0
            print "taking image!"
            #self.mc.stopHard()
            self.mc.stop()
            #time.sleep(0.5)
            #for i in range(5):
             #   self.sd.grabImage()
            if self.detectionMode==0:
                self.detectionMode=self.sd.detect()
            else:
                self.sd.grabImage()
                time.sleep(0.01)#time.sleep(0.08)
        else:
            self.sd.grabImage()
            time.sleep(0.01)#time.sleep(0.08)
        self.detectionCount+=1

        #check current state
        if self.detectionMode==1: #turn left
            # algorithm for keeping left
            self.keepLeft(ul,ur,uf)
        elif self.detectionMode==2: #turn right
            # algorithm for keeping right
            self.keepRight(ul,ur,uf)
        elif self.detectionMode==3: #treasure detected
            #move towards treasure and play sound
            if uf>15: #go until sign is close enough
                self.mc.moveForwardControlledPIDboth(ul,ur,uf)
            else:
                #play win sound
                self.mc.stop()
                self.mc.turnBack()
                self.mc.turnBack()
                self.detectionMode=0
        elif self.detectionMode==4: #go back
            #turn around
            self.mc.turnBack()
            self.detectionMode=0
        elif self.detectionMode==5: #bomb found
            #move until bomb explodes
            if uf>15: #go until sign is close enough
                self.mc.moveForwardControlledPIDboth(ul,ur,uf)
            else:
                #play explode sound
                time.sleep(2)
                self.mc.turnBack()
                self.detectionMode=0
        else: #default mode       
            self.moveDefault(ul,ur,uf)

    # default mode: just go straight until a wall appears in front of robot
    def moveDefault(self,ul,ur,uf):
        if uf>self.frontDist: #opt:5.5cm
            self.mc.moveForwardControlledPIDboth(ul,ur,uf)
            #self.mc.moveForwardControlledPID(ul,ur,uf)
            #self.mc.moveForwardControlled(ul,ur,uf)
        elif ul>15:
            self.mc.turnLeft()
            self.refreshSensors()
            self.detectionMode=0
        elif ur>15:
            self.mc.stopHard()
            self.mc.turnRight()
            self.refreshSensors()
            self.detectionMode=0
        else:
            #print "STOP!"
            #self.mc.stop()
            #self.mc.stopHard()
            self.mc.turnBack()
            self.refreshSensors()
            self.detectionMode=0

    # left sign detected: go straight until you can turn left, then turn
    def keepLeft(self,ul,ur,uf):
        if uf>self.frontDist:
            if ul<20:
                self.mc.moveForwardControlledPIDboth(ul,ur,uf)
            else:
                for i in range(self.delaySteps):
                    self.mc.moveForwardControlledPIDboth(ul,ur,uf)
                self.mc.turnLeft()
                self.refreshSensors()
                self.detectionMode=0
        else:
            self.mc.turnBack()
            self.refreshSensors()
            self.detectionMode=0

    # right sign detected: go straight until you can turn right, then turn
    def keepRight(self,ul,ur,uf):
        if uf>self.frontDist:
            if ur<20:
                self.mc.moveForwardControlledPIDboth(ul,ur,uf)
            else:
                #self.mc.moveFront()
                #time.sleep(self.delayTime)
                for i in range(self.delaySteps):
                    self.mc.moveForwardControlledPIDboth(ul,ur,uf)
                    time.sleep(0.08)
                self.mc.turnRight()
                self.refreshSensors()
                self.detectionMode=0
        else:
            self.mc.turnBack()
            self.refreshSensors()
            self.detectionMode=0

    def kill(self):
        # Reset GPIO settings
        self.mc.kill()
        self.sd.kill()
        self.sr.kill()
        
    

