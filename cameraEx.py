"""
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""

import cv2
import time

start_time = time.time()


cap = cv2.VideoCapture(0)
"""i=0 #frame counter
frameTime = 1 # time of each frame in ms, you can add logic to change this value.
while(cap.isOpened()):
    if (i == 100):
        print(f"Time for 100 frames {time.time() - start_time}")
    ret = cap.grab() #grab frame
    i=i+1 #increment counter
    if i % 3 == 0: # display only one third of the frames, you can change this parameter according to your needs
        ret, frame = cap.retrieve() #decode frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(frameTime) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()"""

import cv2
import numpy as np
import sys

p_frame_thresh = 300000 # You may need to adjust this threshold

# cap = cv2.VideoCapture(video_path)
# Read the first frame.
ret, prev_frame = cap.read()

while ret:
    ret, curr_frame = cap.read()
    print(f'normal frame size: {sys.getsizeof(curr_frame)}')
    if ret:
        diff = cv2.absdiff(curr_frame, prev_frame)
        print(f'Difference in size for last and new frame: {sys.getsizeof(diff)}')
        non_zero_count = np.count_nonzero(diff)
        if non_zero_count > p_frame_thresh:
            print("Got P-Frame")
            cv2.imshow('frame',diff)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            cv2.imshow('frame',curr_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        prev_frame = curr_frame