import cv2
import socket
import struct
import numpy as np


def cameraCommunication():
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
        
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('169.254.226.73', 20001))
    dat = b''
    dump_buffer(s)

    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
        #img = cv2.resize(img,None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            try:
                cv2.imshow('frame', img)
            except:
                print("error (-215:Assertion failed)")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            dat = b''
    # cap.release()
    cv2.destroyAllWindows()
    s.close()

cameraCommunication()