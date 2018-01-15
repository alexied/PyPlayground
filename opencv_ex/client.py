import numpy
import socket
import cv2
import time
import mss
import screeninfo
from PIL import Image
from io import BytesIO

#clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clientsocket.connect(('192.168.0.102', 8089))
m = screeninfo.get_monitors()
monitor = {'top': 0, 'left': 0, 'width': 640, 'height': 480}

# def sample(img):
#     payload = img.tostring()
#     print(len(payload))
#     res = clientsocket.send(str(len(payload)))
#     if res != len(str(len(payload))):
#         print("Could not send all data")
#         print(res)
#     acknowledge = clientsocket.recv(1)
#     if int(acknowledge) == 1:
#         clientsocket.send(payload)
#     else:
#         print("ackg failed")
#     while True:
#         sack = clientsocket.recv(1)
#         if int(sack) == 1:
#             break

def convToJpeg():
    with mss.mss() as sct:
        with BytesIO() as ramfile:
            grabs = sct.grab(monitor)
            ret,payload=cv2.imencode(".jpg",numpy.array(grabs),[int(cv2.IMWRITE_JPEG_QUALITY), 40])
            #cv2.imwrite(ramfile,numpy.array(grabs),[int(cv2.IMWRITE_JPEG_QUALITY), 40])
            dsa = cv2.imdecode(numpy.fromstring(payload, dtype=numpy.uint8), 1)
            cv2.imshow('img', dsa)
            cv2.waitKey(1)
    return 0

def getImg():
    with mss.mss() as sct:
        while True:
            last_time = time.time()
            grabs = sct.grab(monitor)
            ret, payload = cv2.imencode(".jpg", numpy.array(grabs), [int(cv2.IMWRITE_JPEG_QUALITY), 40])
            dsa = cv2.imdecode(numpy.fromstring(payload, dtype=numpy.uint8), 1)
            cv2.imshow('img', dsa)
            cv2.waitKey(25)
            print('fps: {0}'.format(1 / (time.time() - last_time)))


def screen_record_efficient():
    # 800x600 windowed mode
    mon = {'top': 40, 'left': 0, 'width': 800, 'height': 640}

    title = '[MSS] FPS benchmark'
    fps = 0
    sct = mss.mss()
    last_time = time.time()

    while time.time() - last_time < 10:
        img = numpy.asarray(sct.grab(mon))
        fps += 1

        cv2.imshow(title, img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    return fps

getImg()