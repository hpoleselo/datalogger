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
print("Using port: %s") %comport.name

# Setup for plotting in Matplotlib
style.use('fivethirtyeight')

xs = []
ys = []
fig = plt.figure()
# Um plot 1x1 e o plot eh o numero 1
ax1 = fig.add_subplot(1,1,1)

dataFromSerial = 0

# Stantard, always save log and 300 ms refresh rate
saveLog = True
refreshRate = 300

# Adicionar argparse com a taxa de atualizacao e True se for pra salvar log

def readFromSerial():
    """ Opening and echoing the Serial port. """
    try:
        # Reads until it gets a carriage return. MAKE SURE THERE IS A CARRIAGE RETURN OR IT READS FOREVER
        data = comport.readline()
        # Splits string into a list at the tabs   
        separatedData = data.split()
        return separatedData
    except(KeyboardInterrupt):
        comport.close()


def sendToSerial():
    """ Send byte to ATMega328"""
    PARAM_CARACTER='t'
    PARAM_ASCII=str(chr(116))       # Equivalente 116 = t
    
    # Time entre a conexao serial e o tempo para escrever (enviar algo)
    time.sleep(1.8) # Entre 1.5s a 2s
    
    #comport.write(PARAM_CARACTER)
    comport.write(PARAM_ASCII.encode())
    
    VALUE_SERIAL=comport.readline()

    print ('\nRetorno da serial: {!r}'.format(VALUE_SERIAL))


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
