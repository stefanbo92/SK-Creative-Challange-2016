import MazeControl
import SensorReader
import time


if __name__ == '__main__':
    mc=MazeControl.MazeControl()
    sr=SensorReader.SensorReader(5)
    while True:
        try:
            start=time.time()
            ul,ur,uf =1,2,3#sr.getSensorReadings()      
            print ("Distance left: "+str(ul)+"cm")
            mc.moveMaze(ul,ur,uf)
            stop=time.time() 
            print ("time: "+str((stop-start)*1000)+"ms")
        except KeyboardInterrupt:
            mc.kill()
            sr.kill()
            raise
