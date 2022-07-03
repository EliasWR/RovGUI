"""
PYTHON SCRIPT FOR GUI APPLICATION FOR ROV. CONTAINS THE GLOBAL VARIABLES
THAT ARE SHARED BETWEEN MAIN.PY AND INTERFACING.PY, RESPECTIVELY COMMUNICATION
AND MAIN GUI SCRIPTS.
"""
import numpy as np

# Holds the frame communicated from Raspberry Pi
rovCamera = np.array([])

# Commands from GUI to raspberry with initial values
light = 0
motorSpeed = 0
runZone = -1
forceReset = False
mode = 1
takePhoto = False
takeVideo = False

# Sensor information from Raspberry with inital values
temp = 0
pressure = 0
leak = 0
angle = 0
interlockedZones = [True] * 8

# Boolean flag that indicates if new actions have been
# performed on GUI
newCommands = False 