import numpy
import socket
import cv2
import time
import mss
import screeninfo
import threading
from PIL import Image
from io import BytesIO

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.102', 8089))
m = screeninfo.get_monitors()
monitor = {'top': 0, 'left': 0, 'width': 640, 'height': 480}

def ss_encode():
    return 0

def getImg():
    with mss.mss() as sct:
        while True:
            last_time = time.time()
            asarr = numpy.asarray(sct.grab(monitor))
            ret, payload = cv2.imencode(".jpg", asarr , [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            plen = str(len(payload))
            res = clientsocket.send(plen)
            if res != len(str(len(payload))):
              print("Could not send all data")
              print(res)
            acknowledge = clientsocket.recv(1)
            if int(acknowledge) == 1:
              clientsocket.send(payload)
            else:
                print("ackg failed")
            while True:
              sack = clientsocket.recv(1)
              if int(sack) == 1:
                  break

getImg()

def sendone():
    with mss.mss() as sct:
                last_time = time.time()
                asarr = numpy.asarray(sct.grab(monitor))
                ret, payload = cv2.imencode(".jpg", asarr , [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                plen = str(len(payload))
                res = clientsocket.send(plen)
                if res != len(str(len(payload))):
                  print("Could not send all data")
                  print(res)
                acknowledge = clientsocket.recv(1)
                if int(acknowledge) == 1:
                  clientsocket.send(payload)
                else:
                    print("ackg failed")