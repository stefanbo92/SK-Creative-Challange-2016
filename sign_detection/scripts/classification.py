#!/usr/bin/env python

import cv2

def classify(img):
    # define all templates
    template=[]
    template.append(cv2.imread("src/sign_detection/templates/0.png",0))
    template.append(cv2.imread("src/sign_detection/templates/1.png",0))
    template.append(cv2.imread("src/sign_detection/templates/2.png",0))
    template.append(cv2.imread("src/sign_detection/templates/3.png",0))

    out=[]

    # loop through all warped images
    for i in range(len(img)):
        corr=[]
        # test each template
        for j in range (len(template)):
            res = cv2.matchTemplate(img[i],template[j],cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            corr.append(max_val)
        # save correlation value for each template for every image
        out.append(corr)
    return out

