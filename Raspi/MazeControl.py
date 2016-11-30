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
        # 3: front sign detected
        # 4: backward sign detected
        self.detectionMode=0  


    #refreshing SensorReadings
    def refreshSensors(self):
        for i in range(self.filterLength):
            self.sr.getSensorReadings()
            
    # ul, ur, uf are filtered ultrasonic distances in cm of left,
    # right and front sensor
    def moveMaze(self,ul,ur,uf):
        #update buffer
        self.sd.grabImage()

        #check current state
        if self.detectionMode==1:
            # algorithm for keeping left
            self.keepLeft(ul,ur,uf)
        elif self.detectionMode==2:
            # algorithm for keeping right
            self.keepRight(ul,ur,uf)
        elif self.detectionMode==3:
            #move default
            self.moveDefault(ul,ur,uf)
        elif self.detectionMode==4:
            #turn around
            self.mc.turnBack()
            self.detectionMode=0
        else:
            #make sign detection
            #self.detectionMode=self.sd.detect()
            self.moveDefault(ul,ur,uf)

    # default mode: just go straight until a wall appears in front of robot
    def moveDefault(self):
        ul,ur,uf=self.sr.getSensorReadings()
        print (str(ul)+" "+str(ur)+" "+str(uf))
        
        if uf>10.2: #opt:5.5cm
            self.mc.moveForwardControlledPD(ul,ur,uf)
            #self.mc.moveForwardControlled(ul,ur,uf)
        elif ul>15:
            self.mc.turnLeft()
            self.refreshSensors()
        elif ur>15:
            self.mc.turnRight()
            self.refreshSensors()
        else:
            self.mc.turnBack()
            self.refreshSensors()

    # left sign detected: go straight until you can turn left, then turn
    def keepLeft(self,ul,ur,uf):
        if ul<15:
            self.mc.moveForward(ul,ur,uf)
        else:
            #time.sleep(0.3)
            self.mc.turnLeft()
            self.refreshSensors()
            self.detectionMode=0

    # right sign detected: go straight until you can turn right, then turn
    def keepRight(self,ul,ur,uf):
        if ur<15:
            self.mc.moveForward(ul,ur,uf)
        else:
            self.mc.turnRight()
            self.refreshSensors()
            self.detectionMode=0

    def kill(self):
        # Reset GPIO settings
        self.mc.kill()
        self.sd.kill()
        
    

