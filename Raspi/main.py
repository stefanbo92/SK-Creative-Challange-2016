import MazeControl
import SensorReader


if __name__ == '__main__':
    mc=MazeControl()
    sr=SensorReader(5)
    while True:
        try:
            ul,ur,uf =sr.getSensorReadings()
            mc.moveMaze(ul,ur,uf)
        except KeyboardInterrupt:
            mc.kill()
            sr.kill()
            raise
