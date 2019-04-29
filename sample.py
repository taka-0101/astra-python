import cv2
import numpy as np
from OpenNIClass import OpenniClass

astra = OpenniClass("file pass")

while True:
    colorImg  = astra.color_update()
    depthImg  = astra.depth_update_(4000,8000)
    #raw_data
    depthData = astra.depth_update()

    cv2.imshow("color",colorImg)
    cv2.imshow("depth",depthImg)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

astra.destructor()