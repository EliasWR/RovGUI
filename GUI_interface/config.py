import numpy as np

rovCamera = np.array([])

# Commands from GUI to raspberry initial values
light = 0
runZone = -1
mode = 0
forceReset = False

# Sensor information from Raspberry
temp = 0
pressure = 0
leak = 0
angle = 0
interlockedZones = []

# When new command has been selected on GUI, the TCP
# communication will send to Raspberry
newCommands = False 