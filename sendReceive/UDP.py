
"""
UDP CLIENT PROGRAM
"""


import socket
import pickle
import cv2

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("169.254.226.72", 20001)
bufferSize          = 60000

 

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

while 1:
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    camera_dict = pickle.loads(msgFromServer[0])
    
    #msg = "Message from Server {}".format(msgFromServer[0])

    print(camera_dict["ret"])

    if camera_dict["ret"]:
        camera_dict["ret"] = False
        scaled_up = cv2.resize(camera_dict["frame"],None, fx=10, fy=10, interpolation=cv2.INTER_AREA)
        cv2.imshow('frame',scaled_up)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break