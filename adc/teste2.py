#!/usr/bin/python2
# -*- coding: iso-8859-1 -*-
import time
import serial
import glob
 
# Iniciando conexao serial
port1 = "/dev/ttyACM0"
port2 = "/dev/ttyUSB0"

if (glob.glob(port1)==[port1]): 
	comport = serial.Serial(port1, 9600, timeout=1)
else: 
	comport = serial.Serial(port2, 9600, timeout=1)

PARAM_CARACTER='t'
time.sleep(1.8)
for i in range(100):
	comport.write(PARAM_CARACTER.encode())
	VALUE_SERIAL=int.from_bytes(comport.read(), "big")
	print ('\nRetorno da serial: {!r}'.format(VALUE_SERIAL))
 
# Fechando conexao serial
comport.close()
