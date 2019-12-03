import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import time
import glob

# Arduino is set always in linux to /dev/ttyUSB0, baudrate matches Arduino's
# Iniciando conexao serial
port1 = "/dev/ttyACM0"
port2 = "/dev/ttyUSB0"

if (glob.glob(port1)==[port1]): 
	comport = serial.Serial(port1, 9600)
else: 
	comport = serial.Serial(port2, 9600)

print ('Using port: {!r}'.format(comport.name))
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
saveLog = False
refreshRate = 300

def readFromSerial():
    """ Callback that is called everytime we want to plot a new point, the rate
    that this callback is called is defined by the user. This basically hears the
    serial port. """
    try:
        # big para
        PARAM_CARACTER='t'
        comport.write(PARAM_CARACTER.encode())
        dataFromSerial = int.from_bytes(comport.read(), "big")
        return dataFromSerial
    except(KeyboardInterrupt):
        comport.close()


def sendToSerial():
    """ Send byte to ATMega328"""

    #comport.write(PARAM_CARACTER)
    #comport.write(PARAM_ASCII.encode())
    PARAM_CARACTER='t'
    comport.write(PARAM_CARACTER.encode())
    
    VALUE_SERIAL=comport.readline()

    print ('\nRetorno da serial: {!r}'.format(VALUE_SERIAL))


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
    try:
        main()
    except(KeyboardInterrupt):
        comport.close()
