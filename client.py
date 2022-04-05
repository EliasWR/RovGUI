## CLIENT COMMUNICATION SIDE, GUI

import socket
import numpy as np
import sys
import cv2
import pickle

# Video source - can be camera index number given by 'ls /dev/video*
# or can be a video file, e.g. '~/Video.avi'
cap = cv2.VideoCapture(0)

# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
# 
#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 
#     # Display the resulting frame
#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# 
# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()

ret, frame = cap.read()
ref_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
frame_resize = ref_frame[::2, ::2]


print(sys.getsizeof(frame))
print(sys.getsizeof(frame_resize))
# print(ret)
# print(frame)
# print(sys.getsizeof(frame))

HEADER = 64     # Gives how many bytes that should be received
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Disconnect!"
ADDR = (HOST, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR) 

def send(msg):


    message = pickle.dumps(msg)
    # message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length = pickle.dumps(send_length)
    print(len(send_length))
    # send_length += b' ' * (HEADER-len(send_length))
    # send_length += b' ' * 100 
    print(len(send_length))

    #msg_length = msg_length.encode(FORMAT)


    ### converting to string
    ##str_val = str(msg_length)
    ### converting string to bytes
    ##byte_val = str_val.encode()
    ##print(byte_val)

    client.send(send_length)
    client.send(message)

send("frame")

