import MazeControl
import SensorReader
import time
import SignDetector

if __name__ == '__main__':
    maze=MazeControl.MazeControl()
    sr=SensorReader.SensorReader(5)
    sd=SignDetector.SignDetector()
	
    while True:
        try:
            start=time.time()
            # check sensor readings
            ul,ur,uf =sr.getSensorReadings()      
            print ("Distance left: "+str(ul)+"cm")
            #print ("Distance right: "+str(ur)+"cm")
            #print ("Distance front: "+str(uf)+"cm")

            # check motor movements
            #maze.mc.turnLeft()
            #maze.mc.turnRight()
            #maze.mc.turnBack()
            #maze.mc.moveForward(5.5,0,0) # just goes straight, no adjusting

            # autonomous maze movement
            #maze.moveMaze(ul,ur,uf)

            #check sign detector
            #sd.grabImage()
            '''
            print ("total time: "+str((time.time()-start)*1000)+"ms")
            maze.mc.moveForward(5.5,0,0)
            time.sleep(0.8)
            maze.mc.stop()        
            time.sleep(0.8)
            maze.mc.turnBack()
            time.sleep(0.8)
            '''
            #time.sleep(0.5)

        except KeyboardInterrupt:
            maze.kill()
            sr.kill()
            raise
