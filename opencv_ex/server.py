import socket
import sys
import cv2
import pickle
import numpy as np
import struct

HOST=''
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print 'Socket created'

s.bind((HOST,PORT))
print 'Socket bind complete'
s.listen(10)
print 'Socket now listening'

conn,addr=s.accept()

data = ""
while True:
    size = conn.recv(20)
    size = 1228800
    print(size)
    if int(size) > 0:
        conn.send(str(1))
    else:
        conn.send(str(0))
    data = ""
    while len(data) < int(size):
      data += conn.recv(4096)
    print(len(data))
    conn.send(str(1))
    img = np.fromstring(data,dtype=np.uint8).reshape(480,640,4)
    cv2.imshow('frame',img)
    cv2.waitKey(1)
