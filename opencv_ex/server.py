import socket
import sys
import cv2
import pickle
import numpy
import struct
import time

HOST=''
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)
print 'Te ascult patroane'

conn,addr=s.accept()

data = ""

while True:
    last_time=time.time()
    size = conn.recv(20)
    if int(size) > 0:
        conn.send(str(1))
    else:
        conn.send(str(0))
    data = ""
    while len(data) < int(size):
      data += conn.recv(4096)
    conn.send(str(1))
    img = cv2.imdecode(numpy.fromstring(data,dtype=numpy.uint8),1)
    print('fps: {0}'.format(1 / (time.time() - last_time)))
    cv2.imshow('frame',img)
    cv2.waitKey(1)


