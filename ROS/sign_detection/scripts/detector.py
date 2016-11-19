#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import time
import classification
import operator
import math



#PARAMS
saveSize=100
numContrours=1000
approxAccuracy=0.03

def talker():
    
    #pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('detector', anonymous=True)
    cap=cv2.VideoCapture(0)
  
    saveCount=0
    #while not True:
    while not rospy.is_shutdown():
        start_time = time.time()

        #get image, turn to grayscale, median blur and perform adaptive threshold 
        ret,img=cap.read()
        #img=res = cv2.resize(img,(img.shape[1]/2, img.shape[1]/2), interpolation = cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray,5)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        
        #morphologyEx opening and erosion
        kernel=np.ones((5,5),np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.erode(thresh,kernel,iterations = 1)
        threshImg=thresh.copy()
        #find contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea,reverse=True)[:numContrours]

        contoursFiltered=[]
        
        boxes=[]

        #loop over all contours
        for i in range(len(contours)):
             sign = contours[i]
             peri = cv2.arcLength(sign,True)
             #approximate poligon with certain accuracy
             approx = cv2.approxPolyDP(sign,approxAccuracy*peri,True)
             #filter all polygons that dont have four corners, a certain area and are convex
             if (len(approx)==4) and cv2.contourArea(approx) > 1000 and cv2.isContourConvex(approx):
                 # get bounding rectangle for contour and calculate aspect ratio 
                 rect = cv2.minAreaRect(sign)
                 (x, y, w, h) = cv2.boundingRect(approx)
		 ar = w / float(h)
		 if 0.9<ar<1.1:
                     #save bounding boxes with the right aspect ratio
                     contoursFiltered.append(sign)
                     r = cv2.cv.BoxPoints(rect)
                     #print "Box corners:"
                     r=orderCorners(r)
                     #print r
                     boxes.append(r)
                     

        #print ("Number of boxes before nonmax supression:")
        #print len(boxes)

        # perform non max supression of bounding boxes
        toDelete =[]
        for i in range (len(boxes)):
            if i not in toDelete:
                #print ("Point "+str(i)+":")
                pt1=np.array([boxes[i][0][0],boxes[i][0][1]])
                for j in range (len(boxes)):           
                    dist=boxes[i][0][0]-boxes[j][0][0]+boxes[i][0][1]-boxes[j][0][1]
                    #print ("Abs:")
                    #print abs(dist)
                    #print cv2.norm((pt1-np.array([boxes[j][0][0],boxes[j][0][1]])))
                    # delete boxes that too close, choosing the inner box
                    if (i!=j) and abs(dist)<100 and dist>0:
                        toDelete.append(j)

        #print ("zu loeschen:")
        #print toDelete
        filteredBoxes=[]
        for i in range(len(boxes)):
            if i not in toDelete:
                filteredBoxes.append(boxes[i])

        #print ("Number of Boxes after filter:")
        #print len(filteredBoxes)
        

        # draw corners of filtered bounding boxes and extract the warped boxes
        warp= np.zeros((saveSize,saveSize,1), np.uint8)
        warpedSquares=[]
        #cv2.drawContours(img,contoursFiltered,-1,(0,255,0),1)
        for i in range(len(filteredBoxes)):
            print ("Box corners: ")
            print filteredBoxes[i]
            cv2.circle(img,(int(filteredBoxes[i][0][0]),int(filteredBoxes[i][0][1])), 2, (255,0,0), -1)
            cv2.circle(img,(int(filteredBoxes[i][1][0]),int(filteredBoxes[i][1][1])), 2, (0,0,255), -1)
            cv2.circle(img,(int(filteredBoxes[i][2][0]),int(filteredBoxes[i][2][1])), 2, (0,0,255), -1)
            cv2.circle(img,(int(filteredBoxes[i][3][0]),int(filteredBoxes[i][3][1])), 2, (0,0,255), -1)

            #corners from upper left-> lower left -> lower right -> upper right
            newCorners = np.float32([[0,0],[0,saveSize],[saveSize,saveSize],[saveSize,0]])
            imageCorners = np.float32([[filteredBoxes[i][0][0],filteredBoxes[i][0][1]],[filteredBoxes[i][1][0],filteredBoxes[i][1][1]],[filteredBoxes[i][2][0],filteredBoxes[i][2][1]],[filteredBoxes[i][3][0],filteredBoxes[i][3][1]]])
            #get perspective transform
            H = cv2.getPerspectiveTransform(imageCorners,newCorners)
            warp = cv2.warpPerspective(gray,H,(saveSize+1,saveSize+1))
            #warpedSquares.append(warp)
            #otsu filtering
            blurSign = cv2.GaussianBlur(warp,(5,5),0)
            ret2,otsu = cv2.threshold(blurSign,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            warpedSquares.append(otsu)
            #save image
            #cv2.imwrite("img/"+str(saveCount)+".png",otsu)
            saveCount+=1
            if saveCount>50:
                saveCount=0


        correlations=classification.classify(warpedSquares)
        #print correlations
        #draw results into image
        for i in range(len(warpedSquares)):
            index, value=min(enumerate(correlations[i]), key=operator.itemgetter(1))
            print "Correlations:"
            print correlations [i]
            #print ("min value: "+str(value))
            if value< 2500: #if value>0.95:
                className=""
                if index==0:  
                    className="left"
                elif index ==1:
                    className="down"
                elif index ==2:
                    className="right"
                elif index ==3:
                    className="up"
                else:
                    className="???"
                cv2.putText(img, className, (int(filteredBoxes[i][0][0]),int(filteredBoxes[i][0][1])), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,0),2)
                #cv2.imwrite("img/"+className+str(saveCount)+".png",warpedSquares[i])
            
        # show images and print time
        cv2.imshow("Thresh", threshImg)
        cv2.imshow("Image", img)
        #cv2.imshow("warp", warp)    
        print("Time: %s milliseconds" % ((time.time() - start_time)*1000)) 
        print ("_________________________")
        cv2.waitKey(1)

        #publish something
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        #pub.publish(hello_str)


def orderCorners(corners):
    meanX = sum(x[0] for x in corners) / 4
    meanY = sum(x[1] for x in corners) / 4   

    def getKey(item):
        return math.atan2(item[0] - meanX, item[1] - meanY)

    return sorted(corners, key=getKey)
    

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass


