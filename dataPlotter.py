# This program plots two variables in real time
# by henrivis

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--savelog", type=bool, required=True,
	help="Want to save the data? True or False")
ap.add_argument("-r", "--refreshrate", type=int, required=True,
	help="Every x milliseconds the data will be acquired")
args = vars(ap.parse_args())

# Arduino is set always in linux to /dev/ttyUSB0, baudrate matches Arduino's
#ser = serial.Serial('/dev/ttyUSB0', 9600)
ser = serial.Serial('/dev/ttyACM0', 9600)
print("Using port: %s") %ser.name

# Setup for plotting in Matplotlib
style.use('fivethirtyeight')

xs = []
ys = []
fig = plt.figure()
# Um plot 1x1 e o plot eh o numero 1
ax1 = fig.add_subplot(1,1,1)

dataFromSerial = 0

# Store what the user gave to us
saveLog = args["savelog"]
refreshRate = args["refreshrate"]

# Adicionar argparse com a taxa de atualizacao e True se for pra salvar log

def readFromSerial():
    """ Opening and echoing the Serial port. """
    try:
        # Reads until it gets a carriage return. MAKE SURE THERE IS A CARRIAGE RETURN OR IT READS FOREVER
        data = ser.readline()
        # Splits string into a list at the tabs   
        separatedData = data.split()
        return separatedData
    except(KeyboardInterrupt):
        ser.close()


def sendToSerial():
    """ Send byte to ATMega328"""
    pass


def plotData(i):
    """ Plot the retrieved data from Arduino via serial communication using matplotlib. """
    global xs, ys    
    data = readFromSerial()
    #if len(data) > 1:
    # Extract the element from the list
    strToSplit = data[0]
    # Separate the time and sensor data
    x, y = strToSplit.split(',')
    # The data must me plotted as float not as a string!
    xs.append(float(x))
    ys.append(float(y))
    # Clean everything before we plot
    ax1.clear()
    ax1.plot(xs,ys)


def saveData():
    """ Store the retrieved data into a txt file to the local where the script is running. """
    outputFile = "logFromATMega328.txt"  
    global xs,ys
    # Combines lists together
    rows = zip(xs, ys)

    # Creates array from list
    row_arr = np.array(rows)

    # Saves data in file (load w/np.loadtxt())
    np.savetxt(outputFile, row_arr)


def main():
    """ Calls the plotData() constantly """
    animt = animation.FuncAnimation(fig, plotData, interval=refreshRate)
    plt.show()
    if saveLog:
        saveData()

if __name__ == "__main__":
    main()
