# maleChildren
This is the repository for the code for the male children toy project. 

## Raspi
This folder contains all the relevant python files to run the ship robot. In order to start everything just run

```{r, engine='bash', count_lines}
python main.py
```

### Python classes

#### MazeControl.py
This program guides the ship through the maze by using ultrasonic sensors and sign detection.

#### MotorControl.py
This program controlls the two motors to drive straight, turn left and right or turn back.

#### SensorReader.py
This program will read out all the three ultrasonic sensors and also applies a median filter to the measurements.

#### SignDetector.py
This program performs computer vision algorithms to detect the signs in the maze.

#### classification.py
Helper class for the SignDetector. It compares the captured images with templates.


##ROS
The ROS folder can be copied into your catkin workspace and will be built with 

```{r, engine='bash', count_lines}
catkin_make
```

### Packages

#### sign_detection 
This is a ROS node for detecting squares.

#### image_publisher 
Opens USB camera and publishes the images as a ROS message.
