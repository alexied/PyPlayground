import cv2
import numpy
import socket
import time
import pickle
import struct
import mss
import sys
import screeninfo
import io
import zlib

m = screeninfo.get_monitors()
monitor = {'top': 0, 'left': 0, 'width': 640, 'height': 480}

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.101',8089))
with mss.mss() as sct:
    while True:
        last_time = time.time()
        grabs = sct.grab(monitor)
        img = numpy.array(grabs)
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