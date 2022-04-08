import socket
import pickle
import cv2
import time
import numpy as np
from math import *

SERVER = "169.254.226.72"
PORT = 1422
HEADERSIZE = 10
max_range = 80*200*1450/2   # Might have to be found from sonar class
length = 640
image = np.zeros((length, length, 1), np.uint8)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER, PORT))
print(f"[NEW CONNECTION] With {SERVER} established")


def plotSonarInput(angle, step, data_lst):

    # max_range = 80*200*1450/2   # Might have to be found from sonar class
    # length = 640
    # image = np.zeros((length, length, 1), np.uint8)   # Resetted image every iteration

    center = (length/2,length/2)
    linear_factor = len(data_lst)/center[0]
    for i in range(int(center[0])):
        if(i < center[0]*max_range/max_range):
            try:
                pointColor = data_lst[int(i*linear_factor-1)]
            except IndexError:
                pointColor = 0

        else:
            pointColor = 0
        for k in np.linspace(0,step,8*step):
            image[int(center[0]+i*cos(2*pi*(angle+k)/400)), int(center[1]+i*sin(2*pi*(angle+k)/400)), 0] = pointColor

    # color = cv2.applyColorMap(image,cv2.COLORMAP_JET)
    cv2.imshow('Sonar Image',image)
    cv2.waitKey(25)






while 1:
    full_msg = b''
    new_msg = True
    while 1:
        msg = s.recv(8192) # Prev 16
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg)-HEADERSIZE == msglen:

            RaspDataIn = pickle.loads(full_msg[HEADERSIZE:])

            img = RaspDataIn["image"]
            print(f'temperature value: {RaspDataIn["temp"]}')
            print(f'pressure value: {RaspDataIn["pressure"]}')
            print(f'leak value: {RaspDataIn["leak"]}')
            print(f'Angle: {RaspDataIn["angle"]}')
            print(f'Step: {RaspDataIn["step"]}')
            print(f'lockedZones: {RaspDataIn["lockedZones"]}')
            
            # print(f'length of sonar data readings: {len(RaspDataIn["dataArray"])}') 
            plotSonarInput(RaspDataIn["angle"], RaspDataIn["step"], RaspDataIn["dataArray"])

            
            cv2.imshow('ROV Camera feed', img)
            
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
            
            new_msg = True
            full_msg = b""

            # FORMING MESSAGE FOR RASPBERRY
            RaspDataOut = {
                "light": 30,
                "runZone": -1,
                "mode": 0,
                "forceReset": True
            }


            RaspDataOut = pickle.dumps(RaspDataOut)
            RaspDataOut = bytes(f'{len(RaspDataOut):<{HEADERSIZE}}', 'utf-8') + RaspDataOut
            s.send(RaspDataOut)


