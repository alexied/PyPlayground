import cv2
import numpy
import socket
import time
import pickle
import struct
import mss
import sys
import screeninfo
from PIL import Image
import io
import zlib

m = screeninfo.get_monitors()
monitor = {'top': 0, 'left': 0, 'width': 640, 'height': 480}
last = numpy.array("[1,2]")
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.102',8089))
with mss.mss() as sct:
    while True:
        last_time = time.time()
        grabs = sct.grab(monitor)
        img = numpy.array(grabs)
        if numpy.array_equal(img,last):
           print "same"
        last = img
        payload = img.tostring()
        print(len(payload))
        res = clientsocket.send(str(len(payload)))
        if res != len(str(len(payload))):
            print("err")
            print(res)
        acknowledge = clientsocket.recv(1)
        if int(acknowledge) == 1 :
            clientsocket.send(payload)
        else:
            print("ackg failed")
        while True:
            sack = clientsocket.recv(1)
            if int(sack) == 1:
                break
        print('fps: {0}'.format(1 / (time.time() - last_time)))

        grabs = sct.grab(monitor)
        img = Image.frombytes('RGB', grabs.size, grabs.rgb)
        #print('fps: {0}'.format(1 / (time.time() - last_time)))
        img.save('image.jpg','jpeg',quality=30,optimize=1)