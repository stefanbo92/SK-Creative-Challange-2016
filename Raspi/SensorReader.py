##
##    The class SensorReader will read the raw ultrasonic sensor measurements
##    and converts them into centimeter. After this, the readings will be filtered by a
##    median filter of the size which is specified as a parameter. The function
##    getSensorReadings() can be called every timestep and will return the
##    three filtered ultrasonic readings of the left, right and front sensor.
##
##        sr=SensorReader(5)
##        while True:
##            ul,ur,uf =sr.getSensorReadings()
##
   
import numpy as np
import RPi.GPIO as GPIO
import time

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)


class SensorReader:

    # creates a SensorReader object that will get the raw sensor readings and
    # filter them with a median filter of specified size
    def __init__(self,size):
        self.size=size
        self.readingsLeft=np.zeros(size)
        self.readingsRight=np.zeros(size)
        self.readingsFront=np.zeros(size)

        # Define GPIO to use on Pi
        self.triggerLeft=22 #pin15
        self.echoLeft=23 #pin16
        self.triggerRight=3
        self.echoRight=4
        self.triggerFront=5
        self.echoFront=6

        # Set pins as output and input
        GPIO.setup(self.triggerLeft,GPIO.OUT)  
        GPIO.setup(self.echoLeft,GPIO.IN)
##        GPIO.setup(self.triggerRight,GPIO.OUT)  
##        GPIO.setup(self.echoRight,GPIO.IN)
##        GPIO.setup(self.triggerFront,GPIO.OUT)  
##        GPIO.setup(self.echoFront,GPIO.IN)  

        # Set trigger to False (Low)
        GPIO.output(self.triggerLeft, False)
##        GPIO.output(self.triggerRight, False)
##        GPIO.output(self.triggerFront, False)
        # Allow module to settle
        time.sleep(0.5)
        print "SensorReader created!"


    # returns the filtered sensor readings ul, ur and uf
    def getSensorReadings(self):
        values=self.getCurrentValues()
        ul,ur,uf=self.filterReading(values)
        return ul,ur,uf
        
    # filters the raw sensor readings with a median filter of size self.size
    def filterReading(self,values):
        for i in reversed(xrange(self.size-1)):
            self.readingsLeft[i+1]=self.readingsLeft[i]
            self.readingsRight[i+1]=self.readingsRight[i]
            self.readingsFront[i+1]=self.readingsFront[i]
        self.readingsLeft[0]=values[0]
        self.readingsRight[0]=values[1]
        self.readingsFront[0]=values[2]
        filterLeft=np.sort(self.readingsLeft)
        filterRight=np.sort(self.readingsRight)
        filterFront=np.sort(self.readingsFront)
        return filterLeft[self.size/2],filterRight[self.size/2],filterFront[self.size/2]

    # reads the GPIO pins and returns an array with unfiltered sensor readings
    def getCurrentValues(self):
        # read the raw distance values in cm
        valueLeft=self.readUltrasonic(self.triggerLeft,self.echoLeft)
        valueRight=0#self.readUltrasonic(self.triggerRight,self.echoRight)
        valueFront=0#self.readUltrasonic(self.triggerFront,self.echoFront)
        # save the sensor readings in an array and return it
        values=np.array([valueLeft,valueRight,valueFront])
        return values

    # triggers the trigger pin of ultrasonic module, then it waits
    # for the echo and calculates the distance in cm
    def readUltrasonic(self,trigger,echo):
        # Send 10us pulse to trigger
        GPIO.output(trigger, True)
        time.sleep(0.00001)
        GPIO.output(trigger, False)
        start = time.time()
        start1=time.time()

        # wait for echo
        while GPIO.input(echo)==0 and start-start1<0.1:
          start = time.time()

        stop = time.time()
        while GPIO.input(echo)==1 and stop-start<0.00583:
          stop = time.time()

        # Calculate pulse length
        #elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s), devided
        # by two since the sound did twice the distance
        #distance = ((stop-start) * 34300)/2
        distance = (stop-start) * 17150
        
        return round(distance,2)

    def kill(self):
        # Reset GPIO settings
        GPIO.cleanup()

##sr=SensorReader(5)
##while True:
##    ul,ur,uf =sr.getSensorReadings()
##    print ("Distance: "+str(ul)+"cm")
