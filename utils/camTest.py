import cv2
cap=cv2.VideoCapture(0)

while (True):
    ret,img=cap.read()
    #print img.shape
    #crop image [y1:y2,x1:x2]
    img=img[0:480, 100:500]
    #rotate image
    rows,cols,ch =img.shape
    print img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
    img = cv2.warpAffine(img,M,(cols,rows))
    cv2.imshow("img",img)
    pressed=cv2.waitKey(1)
    if pressed==107: #if 'k' is pressed
        break

cap.release()
cv2.destroyAllWindows()
