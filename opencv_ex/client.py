import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time
import matplotlib.pyplot as plt
cap=cv2.VideoCapture(0)

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.101',8089))
while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame)
    print len(data)
    clientsocket.sendall(struct.pack("L", len(data))+data)