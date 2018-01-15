import cv2
import numpy as np
from copy import copy

ix,iy = -1,-1
def set_mouse_position(event,x,y,flags,param):
    global ix,iy
    ix,iy = x,y 

img = cv2.imread('entrada.jpg')
cv2.namedWindow('image')
cv2.setMouseCallback('image',set_mouse_position)

img2 = copy(img)
while(1):
    
    cv2.imshow('image',img2)
    k = cv2.waitKey(33)
    print k
    if k == ord('m'):
        img2 = copy(img)
        cv2.circle(img2,(ix,iy),18,(0,255,0),-1)
    elif k == 27:
        break
cv2.destroyAllWindows()
