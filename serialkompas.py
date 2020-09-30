import serial
import time
import datetime
import os
from configku import *
serialcon=serial.Serial(PYSERIAL_COM,BAUDRATE)
kompasPID=os.getpid()
print('Serial---CMD')
print('THREAD PID : ',kompasPID)
mulai=0
def clearFIleKompas():
	clearLOG=open(FILE_KOMPAS,'w').close()
clearFIleKompas()
while True:
	try: 
		recvdata=serialcon.readline().decode(ENCODING_FORMAT)

		print(recvdata)
		now=datetime.datetime.now()
		waktu=','+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+','
		recvdata=recvdata.replace('\r','').replace('\n','')
		print(waktu,recvdata)
		recvdata=recvdata+waktu
		if mulai==RESET_LOG_KOMPAS:
			mulai=0
			file=open(FILE_KOMPAS,'w')
		else:
			file=open(FILE_KOMPAS,'a')
			mulai=mulai+1
		file.write(recvdata+'\n')
		file.close()
	except serial.serialutil.SerialException:
		print("FAIL")
		time.sleep(2)
		serialcon.close()
		serialcon=serial.Serial(PYSERIAL_COM,BAUDRATE)	
	except Exception as e:
		print('FAILED',e)
		serialcon.close()
		serialcon=serial.Serial(PYSERIAL_COM,BAUDRATE)