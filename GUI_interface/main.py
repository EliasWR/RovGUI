from concurrent.futures import thread
import socket
import pickle
import cv2
import time
import numpy as np
from ast import Lambda
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QTime,QTimer
from math import *
import threading
import config
# Importing classes generated from GUI creation
from interfacing import VideoThread, App
import struct

# Sonar constants
MAX_RANGE = 80*200*1450/2   # Might have to be found from sonar class
LENGTH = 640
image = np.zeros((LENGTH, LENGTH, 1), np.uint8)


def plotSonarInput(angle, step, data_lst):

    center = (LENGTH/2,LENGTH/2)
    linear_factor = len(data_lst)/center[0]
    for i in range(int(center[0])):
        if(i < center[0]*MAX_RANGE/MAX_RANGE):
            try:
                pointColor = data_lst[int(i*linear_factor-1)]
            except IndexError:
                pointColor = 0
        else:
            pointColor = 0
        for k in np.linspace(0,step,8*step):
            image[int(center[0]+i*cos(2*pi*(angle+k)/400)), int(center[1]+i*sin(2*pi*(angle+k)/400)), 0] = pointColor

    # Updates GUI animation with new sonar plot 
    a.update_sonar(cv2.applyColorMap(image, cv2.COLORMAP_JET))    

def TCPCom():
    SERVER = "169.254.226.72"
    PORT = 1422
    HEADERSIZE = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER, PORT))
    print(f"[NEW CONNECTION] With {SERVER} established")

    while 1:
        full_msg = b''
        new_msg = True
        while 1:
            # print("Receiving data from raspberry")
            msg = s.recv(8192) # Prev 16
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg
            # print(f"Full messsage: {len(full_msg)}")

            if len(full_msg)-HEADERSIZE == msglen:

                RaspDataIn = pickle.loads(full_msg[HEADERSIZE:])

                a.setDisplayValues(RaspDataIn["temp"], RaspDataIn["depth"], True,
                RaspDataIn["lockedZones"], RaspDataIn["salinity"], RaspDataIn["conductivity"],
                RaspDataIn["density"])

                plotSonarInput(RaspDataIn["angle"], RaspDataIn["step"], RaspDataIn["dataArray"])
                
                new_msg = True
                full_msg = b""

            # If TCP packet was not succesfully unpacked last message
            # reset to input buffer
            if len(full_msg) > 2500:
                new_msg = True
                full_msg = b""
                
                
            # If GUI input variables have been changed, respond with new commands
            if config.newCommands:
                print("[ATTENTION] New commands sent to Raspberry")
                config.newCommands = False

                RaspDataOut = {
                    "light": config.light,
                    "motorSpeed": config.motorSpeed,
                    "runZone": config.runZone,
                    "forceReset": config.forceReset,
                    "mode": config.mode,
                    "takePhoto": config.takePhoto
                    # TODO: TAKE MOVIE
                }

                print(RaspDataOut)  # Data that was sent through TCP
                RaspDataOut = pickle.dumps(RaspDataOut)
                RaspDataOut = bytes(f'{len(RaspDataOut):<{HEADERSIZE}}', 'utf-8') + RaspDataOut
                s.send(RaspDataOut)
            
def UDPCom():
    MAX_DGRAM = 2**16

    def dump_buffer(s):
    # Emptying buffer frame
        while True:
            seg, addr = s.recvfrom(MAX_DGRAM)
            print(seg[0])
            if struct.unpack('B', seg[0:1])[0] == 1:
                print("finish emptying buffer")
            break

    # Getting image udp frame & concate before decode and output image
        
    # Set up UDP socket server
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('169.254.226.73', 20001))

    dat = b''
    dump_buffer(s)

    while True:
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
            if cv2.waitKey(20) & 0xFF == ord('q'):  # Changed from waitkey(1)
                print("Waitkey event entered!")
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