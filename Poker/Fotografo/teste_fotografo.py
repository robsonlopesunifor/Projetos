import numpy
import cv2
import pyautogui
from PIL import Image

PILImage = pyautogui.screenshot(region=(0,0, 300, 400))
opencvImage = cv2.cvtColor(numpy.array(PILImage), cv2.COLOR_RGB2BGR)
#cv2.imshow('Demo 2 Image',opencvImage)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
