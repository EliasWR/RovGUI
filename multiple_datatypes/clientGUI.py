import socket
import pickle
import cv2
import time

SERVER = "169.254.226.72"
PORT = 65432
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER, PORT))
print(f"[NEW CONNECTION] With {SERVER} established")


while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(20000) # Prev 16
        if new_msg:
            start_time = time.time()    # For finding different frame size sending times
            # print("new msg len:",msg[:HEADERSIZE])
            # print(msg)
            msglen = int(msg[:HEADERSIZE])
            new_msg = False


        full_msg += msg


        if len(full_msg)-HEADERSIZE == msglen:
            # print(f"[RECEIVED] Full message from {SERVER}")
            # print(f'[TRANSMISSION TIME] for frame is {time.time() - start_time} second(s)...')

            img = pickle.loads(full_msg[HEADERSIZE:])
            cv2.imshow('ROV Camera feed', img)
            
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
            
            new_msg = True
            full_msg = b""

            # FORMING MESSAGE FOR RASPBERRY
            output_message = "Hello Raspberry!"
            output_message = pickle.dumps(output_message)
            output_message = bytes(f'{len(output_message):<{HEADERSIZE}}', 'utf-8') + output_message
            # print(f"[SENDING] Message to {SERVER}")
            s.send(output_message)