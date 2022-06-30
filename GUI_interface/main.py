
"""
MAIN PROGRAM FOR GUI APPLICATION. HANDLES THE COMMUNICATION WITH THE 
RASPBERRY PI INSIDE THE ROV ENCLOSURE. THIS PROGRAM CONTAINS A TCP 
CLIENT AND A UDP SERVER. PROGRAM IS DEPENDANT ON CONFIG.PY FOR GLOBAL
VARIABLES, AND INTERFACING.PY FOR GUI APPLICATION FUNCTIONALITY.
"""

from xmlrpc.client import Server
import socket
import pickle
import cv2
import time
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
import sys
import cv2
from math import *
import threading
import config
from interfacing import VideoThread, App
import struct

# Sonar constants needed for plotting visualization
MAX_RANGE = 80*200*1450/2
LENGTH = 640
CENTER = (LENGTH/2,LENGTH/2)
image = np.zeros((LENGTH, LENGTH, 1), np.uint8)

"""
Function that creates a circular plot of the sonar readings. Takes
in the angle scanned, step size for next angle and a list of echo
strengths.
"""
def plotSonarInput(angle, step, data_lst):

    linear_factor = len(data_lst)/CENTER[0]
    for i in range(int(CENTER[0])):
        if(i < CENTER[0]*MAX_RANGE/MAX_RANGE):
            try:
                pointColor = data_lst[int(i*linear_factor-1)]
            except IndexError:
                pointColor = 0
        else:
            pointColor = 0
        for k in np.linspace(0,step,8*step):
            image[int(CENTER[0]+i*cos(2*pi*(angle+k)/400)), int(CENTER[1]+i*sin(2*pi*(angle+k)/400)), 0] = pointColor

    # Updates GUI animation with new sonar plot 
    a.update_sonar(cv2.applyColorMap(image, cv2.COLORMAP_JET))    

"""
Function that handles the TCP Communication between the GUI and the
Raspberry Pi. 
"""
def TCPCom():
    # Define connection parameters of RPi server
    SERVER = "169.254.226.72"
    PORT = 1422
    HEADERSIZE = 10

    # Using socket library, initialize a communication object
    # and initialize TCP connection.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER, PORT))

    print(f"[NEW CONNECTION] With {SERVER} established")

    
    full_msg = b''
    new_msg = True
    while 1:
        # Receives TCP packets and stores in variable
        msg = s.recv(8192) # 8192

        # If the start of a data message is sent, find length of expected information
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        # Sum all packets to a full message
        full_msg += msg

        # If length of message is as previously decided, unpack data and call functions
        if len(full_msg)-HEADERSIZE == msglen:

            RaspDataIn = pickle.loads(full_msg[HEADERSIZE:])

            a.setDisplayValues(RaspDataIn["temp"], RaspDataIn["depth"], RaspDataIn["leak"],
            RaspDataIn["lockedZones"], RaspDataIn["salinity"], RaspDataIn["conductivity"],
            RaspDataIn["density"])
            plotSonarInput(RaspDataIn["angle"], RaspDataIn["step"], RaspDataIn["dataArray"])
                
            # Resets for next message
            new_msg = True
            full_msg = b""

        # If TCP packet was not succesfully unpacked last message
        # reset the input buffer
        if len(full_msg) > 2500:    
            new_msg = True
            full_msg = b""
                
                
        # If user has performed actions on GUI, sends commands over TCP to RPi
        if config.newCommands:
            print("[ATTENTION] New commands sent to Raspberry")
            config.newCommands = False

            RaspDataOut = {
                "light": config.light,
                "motorSpeed": config.motorSpeed,
                "runZone": config.runZone,
                "forceReset": config.forceReset,
                "mode": config.mode,
                "takePhoto": config.takePhoto,
                "takeVideo": config.takeVideo
            }

            RaspDataOut = pickle.dumps(RaspDataOut)
            RaspDataOut = bytes(f'{len(RaspDataOut):<{HEADERSIZE}}', 'utf-8') + RaspDataOut
            s.send(RaspDataOut)

"""
Function that handles the UDP communication between the GUI and the 
Raspberry Pi.
"""        
def UDPCom():
    # Datagram set to maximum allowable size
    MAX_DGRAM = 2**16
    dat = b''

    """
    Function that dumps the UDP buffer.
    """
    def dump_buffer(s):
        while True:
            seg, addr = s.recvfrom(MAX_DGRAM)
            print(seg[0])
            if struct.unpack('B', seg[0:1])[0] == 1:
                print("UDP input buffer emptied")
            break
        
    # Using socket library, initialize a communication object
    # and initialize UDP connection.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('169.254.226.73', 20001))

    # Dumps buffer, so that completely new data will be read at this point 
    dump_buffer(s)

    # Continuously checking for UDP datagrams and unpacks if an entire message
    # has been received, else summing up datagrams until this is true
    while 1:
        seg, _ = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
            try:
                config.rovCamera = img
            except:
                print("error (-215:Assertion failed)")
            if cv2.waitKey(20) & 0xFF == ord('q'):  
                break
            dat = b''

    cv2.destroyAllWindows()
    s.close()


if __name__=="__main__":

    # Initializing GUI objects
    app = QApplication(sys.argv)
    a = App()

    # Opening an UDP server in GUI application
    cam_communication = threading.Thread(target=UDPCom)
    cam_communication.start()

    # Opening a TCP client in GUI application
    other_communication = threading.Thread(target=TCPCom)
    other_communication.start()

    # Opens GUI as a seperate window
    a.show()
    sys.exit(app.exec_())