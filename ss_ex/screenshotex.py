import numpy
import cv2
import mss
import time
from screeninfo import get_monitors

m = get_monitors()

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {'top': 0, 'left': 0, 'width': m[0].width, 'height': m[0].height}

    while 'Screen capturing':
        last_time = time.time()

        img = numpy.array(sct.grab(monitor))

        cv2.imshow('OpenCV/Numpy normal', img)
        cv2.waitKey(25)
