import MazeControl
import SensorReader
import time
import SignDetector

if __name__ == '__main__':
    filterLength=5
    maze=MazeControl.MazeControl()
    sr=SensorReader.SensorReader(filterLength)
    sd=SignDetector.SignDetector()
    
    #init filter
    for i in range(filterLength/2+1):
        ul,ur,uf =sr.getSensorReadings()
	
    while True:
        try:
            start=time.time()
            # check sensor readings
            ul,ur,uf =sr.getSensorReadings()
            print (str(ul)+" "+str(ur)+" "+str(uf))
            #print ("Distance left: "+str(ul)+"cm")
            #print ("Distance right: "+str(ur)+"cm")
            #print ("Distance front: "+str(uf)+"cm")

            # check motor movements
            #maze.mc.turnLeft()
            #maze.mc.moveBack()
            #maze.mc.turnRight()
            #maze.mc.turnBack()
            
            #maze.mc.moveForward(ul,ur,0)
            #maze.mc.moveForwardControlled(ul,ur,0)
            maze.mc.moveForwardControlledPD(ul,ur,0)

            # autonomous maze movement
            #maze.moveDefault()
            #maze.moveMaze(ul,ur,uf)

            #check sign detector
            #sd.grabImage()
            #sd.detect()
            '''
            maze.mc.moveForward(5.5,0,0)
            time.sleep(0.8)
            maze.mc.stop()        
            time.sleep(0.8)
            maze.mc.turnBack()
            time.sleep(0.8)
            '''

            #time.sleep(0.2)
            #print ("total time: "+str((time.time()-start)*1000)+"ms")
            

        except KeyboardInterrupt:
            maze.kill()
            sr.kill()
            raise
