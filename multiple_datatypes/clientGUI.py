import socket
import pickle
import cv2
import time

SERVER = "169.254.226.72"
PORT = 1422
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER, PORT))
print(f"[NEW CONNECTION] With {SERVER} established")


while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(8192) # Prev 16
        if new_msg:
            start_time = time.time()    # For finding different frame size sending times    
            msglen = int(msg[:HEADERSIZE])
            new_msg = False


        full_msg += msg


        if len(full_msg)-HEADERSIZE == msglen:

            RaspDataIn = pickle.loads(full_msg[HEADERSIZE:])

            img = RaspDataIn["image"]
            print(f'Temperatuer value: {RaspDataIn["temp"]}')
            print(f'pressure value: {RaspDataIn["pressure"]}')
            print(f'leak value: {RaspDataIn["leak"]}')
            print(f'Angle: {RaspDataIn["angle"]}')
            print(f'Step: {RaspDataIn["step"]}')
            print(f'lockedZones: {RaspDataIn["lockedZones"]}')
            print(f'Length of sonar data readings: {len(RaspDataIn["dataArray"])}') # TODO: LENGTH GETS LONGER FOR EACH ITERATION

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