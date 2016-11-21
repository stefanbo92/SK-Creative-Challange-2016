import MazeControl
import SensorReader
import time


if __name__ == '__main__':
    mc=MazeControl.MazeControl()
    sr=SensorReader.SensorReader(5)
    while True:
        try:
            start=time.time()
            # check sensor readings
            ul,ur,uf =sr.getSensorReadings()      
            print ("Distance left: "+str(ul)+"cm")
            #print ("Distance right: "+str(ur)+"cm")
            #print ("Distance front: "+str(uf)+"cm")

            # check motor movements
            #mc.mc.turnLeft()
            #mc.mc.turnRight()
            #mc.mc.turnBack()
            #mc.mc.moveForward(5.5,0,0) # just goes straight, no adjusting

            # autonomous maze movement
            #mc.moveMaze(ul,ur,uf)
            stop=time.time() 
            print ("total time: "+str((stop-start)*1000)+"ms")
        except KeyboardInterrupt:
            mc.kill()
            sr.kill()
            raise
