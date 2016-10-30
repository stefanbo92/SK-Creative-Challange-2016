#!/usr/bin/env python
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError



def imgPublisher():
    #create image publisher
    image_pub = rospy.Publisher('img_topic', Image, queue_size=10)
    bridge = CvBridge()
    rospy.init_node('imgPublisher', anonymous=True)

    # video capture
    cap=cv2.VideoCapture(0)
  
    while not rospy.is_shutdown():
        #get image
        ret,img=cap.read()

        # publish opencv image as ROS message 
        try:
          image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
        except CvBridgeError as e:
          print(e)
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)
         

if __name__ == '__main__':
    try:
        imgPublisher()
    except rospy.ROSInterruptException:
        pass

