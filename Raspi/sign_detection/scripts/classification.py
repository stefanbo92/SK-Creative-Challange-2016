#!/usr/bin/env python

import cv2
import numpy as np

class SignClassifier:

    def __init__(self):
        # define all templates
        self.template=[]
        self.template.append(cv2.imread("../templates/0.png",0))
        self.template.append(cv2.imread("../templates/1.png",0))
        self.template.append(cv2.imread("../templates/2.png",0))
        self.template.append(cv2.imread("../templates/3.png",0))
    def classify(self,img):
        out=[]
        # loop through all warped images
        for i in range(len(img)):
            corr=[]
            # test each template
            for j in range (len(self.template)):
                #res = cv2.matchTemplate(img[i],template[j],cv2.TM_CCORR_NORMED)
                #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                max_val=np.sum(np.square(np.subtract(np.asarray(img[i]),np.asarray(self.template[j]))))
                corr.append(max_val)
            # save correlation value for each template for every image
            out.append(corr)
        return out


