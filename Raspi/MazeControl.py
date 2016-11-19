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



class MazeControl:

    def __init__(self):
        #create Motor controller
        self.mc=MotorControl.MotorControl()
        self.sd=SignDetector.SignDetector()

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
            self.detectionMode=0
            self.sd.detect()
            #self.moveDefault(ul,ur,uf)

    # default mode: just go straight until a wall appears in front of robot
    def moveDefault(self,ul,ur,uf):
        if uf>3:
            self.mc.moveForward(ul,ur,uf)
        elif ul>5:
            self.mc.turnLeft()
        elif ur>5:
            self.mc.turnRight()
        else:
            self.mc.turnBack()

    # left sign detected: go straight until you can turn left, then turn
    def keepLeft(self,ul,ur,uf):
        if ul<5:
            self.mc.moveForward(ul,ur,uf)
        else:
            #time.sleep(0.3)
            self.mc.turnLeft()
            self.detectionMode=0

    # right sign detected: go straight until you can turn right, then turn
    def keepRight(self,ul,ur,uf):
        if ur<5:
            self.mc.moveForward(ul,ur,uf)
        else:
            self.mc.turnRight()
            self.detectionMode=0

    def kill(self):
        # Reset GPIO settings
        self.mc.kill()
        self.sd.kill()
        
    

