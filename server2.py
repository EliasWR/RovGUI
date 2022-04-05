import socket
import time
import pickle
import numpy as np
import cv2

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1243))
s.listen(5)

# Open CV capture a single frame
cam = cv2.VideoCapture(0)


while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    
    # d = np.array([[2,2],[2,2]])
    ret_val, img = cam.read()
    d = img
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    # print(msg)
    clientsocket.send(msg)

    