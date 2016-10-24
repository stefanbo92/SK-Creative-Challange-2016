#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from std_msgs.msg import String
#import nms
import time



#PARAMS
saveSize=100
numContrours=1000
approxAccuracy=0.03

def talker():
    
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('detector', anonymous=True)
    cap=cv2.VideoCapture(0)
  
    saveCount=0
    #while not True:
    while not rospy.is_shutdown():
        start_time = time.time()
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        #pub.publish(hello_str)
         
        ret,img=cap.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray,5)
        #blur = cv2.GaussianBlur(gray,(1,1),1000)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)


        
        #morphologyEx closing  
        kernel=np.ones((5,5),np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.erode(thresh,kernel,iterations = 1)
        threshImg=thresh.copy()
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea,reverse=True)[:numContrours]

        contoursFiltered=[]
        warp=blank_image = np.zeros((saveSize,saveSize,1), np.uint8)
        boxes=[]
        boxesFull=[]
            
        for i in range(len(contours)):
             sign = contours[i]
             peri = cv2.arcLength(sign,True)
             approx = cv2.approxPolyDP(sign,approxAccuracy*peri,True)
             #approx = cv2.approxPolyDP(sign,3,True)
             #print approx
             #print ("Length of Poly "+str(i)+" is: "+str(len(approx)))
             if (len(approx)==4) and cv2.contourArea(approx) > 1000 and cv2.isContourConvex(approx):
                 #contoursFiltered.append(sign)
                 rect = cv2.minAreaRect(sign)
                 #print ("rect is "+str(rect))
                 (x, y, w, h) = cv2.boundingRect(approx)
		 ar = w / float(h)
		 if 0.9<ar<1.1:
                     contoursFiltered.append(sign)
                     r = cv2.cv.BoxPoints(rect)
                     #boxes = np.vstack([boxes, np.array([r[2][0],r[2][1],r[0][0],r[0][1]])])
                     boxesFull.append(r)
                     #nonmax supression
                     #boxes=np.array([[1,1,3,3],[2,2,4,4],[20,20,40,40]])
                     #filteredBoxes=nms.non_max_suppression_fast(boxes,0)
                     
                     #print ("Box Points:")
                     #print r
                     

        print ("Number of boxes before filter:")
        print len(boxesFull)

        toDelete =[]
        
        for i in range (len(boxesFull)):
            if i not in toDelete:
                print ("Point 1:")
                pt1=np.array([boxesFull[i][0][0],boxesFull[i][0][1]])
                for j in range (len(boxesFull)):           
                    print ("dist: ")
                    dist=boxesFull[i][0][0]-boxesFull[j][0][0]+boxesFull[i][0][1]-boxesFull[j][0][1]
                    print dist
                    print ("Abs:")
                    print abs(dist)
                    #print cv2.norm((pt1-np.array([boxesFull[j][0][0],boxesFull[j][0][1]])))
                    if (i!=j) and abs(dist)<50 and dist<0:
                        print "loeschen!!"
                        toDelete.append(j)

        print ("zu loeschen:")
        #toDelete=sorted(toDelete)
        print toDelete
        filteredBoxes=[]
        for i in range(len(boxesFull)):
            if i not in toDelete:
                filteredBoxes.append(boxesFull[i])

        print ("Number of Boxes after filter:")
        print len(filteredBoxes)
        
        #boxes=np.array([[1,1,3,3],[2,2,4,4],[20,20,40,40]])
        #boxes = np.vstack([boxes, np.array([2,2,4,4])])
        #print boxes
        #filteredBoxes=nms.non_max_suppression_fast(boxes,0)
        #print filteredBoxes 
        for i in range(len(filteredBoxes)):
            cv2.circle(img,(int(filteredBoxes[i][0][0]),int(filteredBoxes[i][0][1])), 2, (0,0,255), -1)
            cv2.circle(img,(int(filteredBoxes[i][1][0]),int(filteredBoxes[i][1][1])), 2, (0,0,255), -1)
            cv2.circle(img,(int(filteredBoxes[i][2][0]),int(filteredBoxes[i][2][1])), 2, (0,0,255), -1)
            cv2.circle(img,(int(filteredBoxes[i][3][0]),int(filteredBoxes[i][3][1])), 2, (0,0,255), -1)
        


            #corners from lower right-> lower left -> upper left -> upper right
            newCorners = np.float32([[saveSize,saveSize],[0,saveSize],[0,0],[saveSize,0]])
            imageCorners = np.float32([[filteredBoxes[i][0][0],filteredBoxes[i][0][1]],[filteredBoxes[i][1][0],filteredBoxes[i][1][1]],[filteredBoxes[i][2][0],filteredBoxes[i][2][1]],[filteredBoxes[i][3][0],filteredBoxes[i][3][1]]])
            #get perspective transform
            H = cv2.getPerspectiveTransform(imageCorners,newCorners)
            warp = cv2.warpPerspective(img,H,(saveSize+1,saveSize+1))
            cv2.imwrite("img/"+str(saveCount)+".png",warp)
            saveCount+=1
            if saveCount>20:
                saveCount=0
            

            
        #cv2.drawContours(img,contoursFiltered,-1,(0,255,0),1)
 
        
        cv2.imshow("Thresh", threshImg)
        cv2.imshow("Image", img)
        #cv2.imshow("warp", warp)
        
        print("Time: %s milliseconds" % ((time.time() - start_time)*1000)) 
        print ("_________________________")
        cv2.waitKey(1)
        
        

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
