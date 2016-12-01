import initVars as iV
import os
import numpy as np
import tensorflow as tf
#import matplotlib.pyplot as plt
import datetime
import sys
import cv2
#from scipy.misc import  imread,imresize
import operator
import time
import math

#define functions
# tf Graph input
x = tf.placeholder(tf.float32, [None, iV.n_input])
y = tf.placeholder(tf.float32, [None, iV.n_output])
keepratio = tf.placeholder(tf.float32)

# Functions! 
pred = iV.conv_basic(x, iV.weights, iV.biases, keepratio, 1)['out']
init = tf.initialize_all_variables()
print ("FUNCTIONS READY")

def orderCorners(corners):
    meanX = sum(x[0] for x in corners) / 4
    meanY = sum(x[1] for x in corners) / 4   
    def getKey(item):
        return math.atan2(item[0] - meanX, item[1] - meanY)
     
    return sorted(corners, key=getKey)

    

# Launch the graph
sess = tf.Session()
sess.run(init)

#Load weights from saver 
saver = tf.train.Saver() 
saver.restore(sess, "../nets/signs_fc.ckpt-8")
print("Model restored.")

#PARAMS
saveSize=100
numContrours=1000
approxAccuracy=0.03

#openCV stuff
cap=cv2.VideoCapture(0)


while(True):
    start_time=time.time()
    ret,img=cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray,5)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        
    #morphologyEx opening and erosion
    kernel=np.ones((5,5),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.erode(thresh,kernel,iterations = 1)
    #threshImg=thresh.copy()
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
            contoursFiltered.append(sign)
            #get rectangle corners and sort them
            r = orderCorners(cv2.cv.BoxPoints(rect))
            w=cv2.norm(r[0],r[3])
            h=cv2.norm(r[0],r[1])
            ar = w / float(h) 
            if 0.9<ar<1.1:
                #save bounding boxes with the right aspect ratio
                boxes.append(r)
                     

    # perform non max supression of bounding boxes
    toDelete =[]
    for i in range (len(boxes)):
        if i not in toDelete:
            for j in range (len(boxes)):           
                dist=boxes[i][0][0]-boxes[j][0][0]+boxes[i][0][1]-boxes[j][0][1]
                # delete boxes that too close, choosing the inner box
                if (i!=j) and abs(dist)<100 and dist>0:
                    toDelete.append(j)

    # actually delete the supressed boxes
    filteredBoxes=[]
    for i in range(len(boxes)):
        if i not in toDelete:
            filteredBoxes.append(boxes[i])

    # draw corners of filtered bounding boxes and extract the warped boxes
    warp=np.zeros((saveSize,saveSize,1), np.uint8)
    warpedSquares=[]
    #cv2.drawContours(img,contoursFiltered,-1,(0,255,0),1)
    for i in range(len(filteredBoxes)):     
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

    #classify with DNN
    for i in range(len(warpedSquares)):
        #img_gray_resize=imresize(warpedSquares[i], [128, 128])/255.
        img_gray_resize=cv2.resize(warpedSquares[i], (128, 128))/255.
        img_grayvec   = np.reshape(img_gray_resize, (1, -1))
        predictiton=sess.run(tf.nn.softmax(pred), feed_dict={x: img_grayvec,keepratio:1.}) #make prediction
        #print (predictiton)
        index, value = max(enumerate(predictiton[0]), key=operator.itemgetter(1)) #find highest value in output vector
        className=""
        if index==0:  
            className="Left"
        elif index ==1:
            className="Right"
        elif index ==2:
            className="Treasure"
        elif index ==3:
            className="Turn Back"
        else:
            className="??"

        print ("Prediciton is class '%s' with accuracy %0.3f"%(className,value))
    
    # show images and print time
    cv2.imshow("Image", img)
    #cv2.imshow("Thresh", threshImg)
    #cv2.imshow("warp", warp)    
    print("Time SignDetection: %s milliseconds" % ((time.time() - start_time)*1000)) 
    print ("_________________________")


    pressed=cv2.waitKey(1)
    if pressed==107: #if 'k' is pressed
        break

cap.release()
cv2.destroyAllWindows()

sess.close()
print ("Session closed.")
