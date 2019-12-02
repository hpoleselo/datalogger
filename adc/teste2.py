#!/usr/bin/python2
# -*- coding: iso-8859-1 -*-
import time
import serial
import glob
 
# Iniciando conexao serial
port1 = "/dev/ttyACM0"
port2 = "/dev/ttyUSB0"

if (glob.glob(port1)==[port1]): 
	comport = serial.Serial(port1, 9600)
else: 
	comport = serial.Serial(port2, 9600)

#comport = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # Setando timeout 1s para a conexao
 
PARAM_CARACTER='t'
PARAM_ASCII=str(chr(116))       # Equivalente 116 = t
 
# Time entre a conexao serial e o tempo para escrever (enviar algo)
time.sleep(1.8) # Entre 1.5s a 2s
 
#comport.write(PARAM_CARACTER)
comport.write(PARAM_ASCII.encode())
 
VALUE_SERIAL=comport.readline()

print ('\nRetorno da serial: {!r}'.format(VALUE_SERIAL))
 
# Fechando conexao serial
comport.close()
