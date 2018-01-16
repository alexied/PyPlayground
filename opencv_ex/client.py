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
monitor = {'top': 0, 'left': 0, 'width': 1366, 'height': 768}
payload=[[],[]]
def ss_encode1():
    with mss.mss() as sct:
        global payload
        asarr = numpy.asarray(sct.grab(monitor))
        ret, payload[0] = cv2.imencode(".jpg", asarr, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

def ss_encode2():
    global payload
    with mss.mss() as sct:
        asarr = numpy.asarray(sct.grab(monitor))
        ret, payload[1] = cv2.imencode(".jpg", asarr, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

def getImg():
    cnt=0
    funarr=[ss_encode1,ss_encode2]
    thdarr=[threading.Thread(target=ss_encode1),threading.Thread(target=ss_encode2())]
    thdarr[cnt&1].start()
    while True:
        thdarr[cnt&1].join() #data to be written
        thdarr[(cnt+1)&1] = threading.Thread(target=funarr[(cnt+1)&1])
        thdarr[(cnt+1)&1].start() #start the other thread to prepare next frame
        plen = str(len(payload[cnt&1]))
        res = clientsocket.send(plen)
        if res != len(str(len(payload[cnt&1]))):
          print("Could not send all data")
          print(res)
        acknowledge = clientsocket.recv(1)
        if int(acknowledge) == 1:
          clientsocket.send(payload[cnt&1])
        else:
            print("ackg failed")
        while True:
          sack = clientsocket.recv(1)
          if int(sack) == 1:
              break
        cnt+=1

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