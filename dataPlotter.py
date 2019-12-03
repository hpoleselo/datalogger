import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import time
import glob
import os

Vref = 5;

port1 = "/dev/ttyACM0"
port2 = "/dev/ttyUSB0"

if (glob.glob(port1)==[port1]): 
	comport = serial.Serial(port1, 9600)
else: 
	comport = serial.Serial(port2, 9600)

print ('Using port: {!r}'.format(comport.name))
os.system('sudo chmod 666 {!r}'.format(comport.name))

time.sleep(1.8) # Entre 1.5s a 2s

# Setup for plotting in Matplotlib
style.use('fivethirtyeight')

xs = []
ys = []

# Variable to count the samples that are being received
count = 0

fig = plt.figure()

# Um plot 1x1 e o plot eh o numero 1
ax1 = fig.add_subplot(1,1,1)
dataFromSerial = 0

# Stantard, always save log and 300 ms refresh rate
saveLog = True
refreshRate = 100

def readFromSerial():
    """ Callback that is called everytime we want to plot a new point, the rate
    that this callback is called is defined by the user. This basically hears the
    serial port. """
    try:
        PARAM_CARACTER='t'
        comport.write(PARAM_CARACTER.encode())
        dataFromSerial = int.from_bytes(comport.read(), "big")
        return dataFromSerial*5/255
    except(KeyboardInterrupt):
        comport.close()


def plotData(i):
    """ Plot the retrieved data from Arduino via serial communication using matplotlib. """
    global count, ys  
    count += 1
    data = readFromSerial()

    # The data must me plotted as float not as a string!
    xs.append(float(count))
    ys.append(float(data))

    # Clean everything before we plot
    ax1.clear()
    ax1.plot(xs,ys)

    ax1.set_xlabel('milliseconds (ms)')
    ax1.set_ylabel('Volts (V)')
    ax1.set_title('Sensor Acquistion')


def saveData():
    """ Store the retrieved data into a txt file to the local where the script is running. """
    outputFile = "logFromATMega328.txt"  
    global xs,ys
    np.savetxt('data.txt', np.column_stack((xs, ys)), fmt='%0.3f', delimiter=',') 


def main():
    """ Calls the plotData() constantly """
    animt = animation.FuncAnimation(fig, plotData, interval=refreshRate)
    plt.show()
    if saveLog:
        saveData()

if __name__ == "__main__":
    try:
        main()
    except(KeyboardInterrupt):
        comport.close()
