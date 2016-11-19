# image_publisher

This is a simple ROS node that opens a video stream and publishes it as a ROS message. This can be used to send image from raspberry pi to laptop for image processing. The message is named ""


The topic is called "/img_topic"



Usage:
```{r, engine='bash', count_lines}
rosrun image_publisher image_Publisher.py 
```
