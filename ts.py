import serial
import time
import datetime
serialcon=serial.Serial('COM3',9600)

while True:
	ok=serialcon.readline().decode('ASCII')
	print(ok)
	now=datetime.datetime.now()
	waktu=str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'-'
	print(waktu)
	time.sleep(2)