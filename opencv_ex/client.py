import cv2
import numpy
import socket
import time
import pickle
import struct
import mss
import sys
import screeninfo

m = screeninfo.get_monitors()
monitor = {'top': 0, 'left': 0, 'width': 640, 'height': 480}

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.101',8089))
with mss.mss() as sct:
    while True:
        last_time = time.time()
        img = numpy.array(sct.grab(monitor))
        data = pickle.dumps(img) #this is slowing me down a lot
        clientsocket.sendall(struct.pack("L", len(data))+data)
        print('fps: {0}'.format(1 / (time.time() - last_time)))