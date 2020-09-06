import time
import pyfirmata
import os
from ardupin import *
from configku import *

board = pyfirmata.ArduinoMega(COM_PORT)
#board = pyfirmata.Arduino('COM3')
it=pyfirmata.util.Iterator(board)
it.start()
"""
print(RPWM_DRIBLE_PIN) 
print(LPWM_DRIBLE_PIN)
print(EON1_DRIBLE_PIN)
print(EON2_DRIBLE_PIN)

print(RPWM_KANAN_PIN)
print(LPWM_KANAN_PIN)
print(EON1_KANAN_PIN)
print(EON2_KANAN_PIN)

print(RPWM_BELAKANG_PIN)
print(LPWM_BELAKANG_PIN)
print(EON1_BELAKANG_PIN)
print(EON2_BELAKANG_PIN)

print(RPWM_KIRI_PIN)
print(LPWM_KIRI_PIN)
print(EON1_KIRI_PIN)
print(EON2_KIRI_PIN)

"""
#IR_READ=board.get_pin('d:43:i')

IR_READ=board.get_pin(IR_PIN)
RPWM_DRIBLE=board.get_pin(RPWM_DRIBLE_PIN)
LPWM_DRIBLE=board.get_pin(LPWM_DRIBLE_PIN)
EON1_DRIBLE=board.get_pin(EON1_DRIBLE_PIN)
EON2_DRIBLE=board.get_pin(EON2_DRIBLE_PIN)

RPWM_KANAN=board.get_pin(RPWM_KANAN_PIN)
LPWM_KANAN=board.get_pin(LPWM_KANAN_PIN)
EON1_KANAN=board.get_pin(EON1_KANAN_PIN)
EON2_KANAN=board.get_pin(EON2_KANAN_PIN)

RPWM_BELAKANG=board.get_pin(RPWM_BELAKANG_PIN)
LPWM_BELAKANG=board.get_pin(LPWM_BELAKANG_PIN)
EON1_BELAKANG=board.get_pin(EON1_BELAKANG_PIN)
EON2_BELAKANG=board.get_pin(EON2_BELAKANG_PIN)

RPWM_KIRI=board.get_pin(RPWM_KIRI_PIN)
LPWM_KIRI=board.get_pin(LPWM_KIRI_PIN)
EON1_KIRI=board.get_pin(EON1_KIRI_PIN)
EON2_KIRI=board.get_pin(EON2_KIRI_PIN)

def drible(inputspeed=150):
	speed=inputspeed/255
	speed=round(speed,2)
	if speed==0:
		EON1_DRIBLE.write(0)
		EON2_DRIBLE.write(0)
	elif speed<0:
		speed=abs(speed)
		EON1_DRIBLE.write(1)
		EON2_DRIBLE.write(1)
		LPWM_DRIBLE.write(0)
		RPWM_DRIBLE.write(speed)
	else:
		EON1_DRIBLE.write(1)
		EON2_DRIBLE.write(1)
		LPWM_DRIBLE.write(speed)
		RPWM_DRIBLE.write(0)
	print(speed)
def kanan(inputspeed=150):
	speed=inputspeed/255
	speed=round(speed,2)
	if speed==0:
		EON1_KANAN.write(0)
		EON2_KANAN.write(0)
	elif speed<0:
		speed=abs(speed)
		EON1_KANAN.write(1)
		EON2_KANAN.write(1)
		LPWM_KANAN.write(speed)
		RPWM_KANAN.write(0)
	else:	
		EON1_KANAN.write(1)
		EON2_KANAN.write(1)
		LPWM_KANAN.write(0)
		RPWM_KANAN.write(speed)
	print(speed)
def kiri(inputspeed=150):
	speed=inputspeed/255
	speed=round(speed,2)
	if speed==0:
		EON1_KIRI.write(0)
		EON2_KIRI.write(0)
	elif speed<0:
		speed=abs(speed)
		EON1_KIRI.write(1)
		EON2_KIRI.write(1)
		LPWM_KIRI.write(speed)
		RPWM_KIRI.write(0)
	else:	
		EON1_KIRI.write(1)
		EON2_KIRI.write(1)
		LPWM_KIRI.write(0)
		RPWM_KIRI.write(speed)
	print(speed)
def belakang(inputspeed=150):
	speed=inputspeed/255
	speed=round(speed,2)
	if speed==0:
		EON1_BELAKANG.write(0)
		EON2_BELAKANG.write(0)
	elif speed<0:
		speed=abs(speed)
		EON1_BELAKANG.write(1)
		EON2_BELAKANG.write(1)
		LPWM_BELAKANG.write(speed)
		RPWM_BELAKANG.write(0)
	else:	
		EON1_BELAKANG.write(1)
		EON2_BELAKANG.write(1)
		LPWM_BELAKANG.write(0)
		RPWM_BELAKANG.write(speed)
	print(speed)
def stop():
	setMotor()
def setMotor(motor_kiri=0,motor_kanan=0,motor_belakang=0):
	kiri(motor_kiri)
	belakang(motor_belakang)
	kanan(motor_kanan)
def tendang():
	drible(-255)
	time.sleep(2)
	drible()
def getIR():
	if IR_READ.read():
		return False
	else:
		return True
def fileKompasNotEmpty():
	get_status=os.stat(FILE_KOMPAS).st_size>0
	return get_status
def getKompas(index=0):
	#HEADING1,HEADING2,TIMELOG
	if(fileKompasNotEmpty()):
		try:
			file=open(FILE_KOMPAS,READ_FILE)
			dataAsli=file.readline()
			file.close()
			pecahData=dataAsli.split(',')
			print('FILE ASLI:',dataAsli)
			print('FILE SPLIT:',pecahData)
			return int(float(pecahData[index]))
		except ValueError:
			return int(float(pecahData[index]))
		except IndexError:
			return int(float(pecahData[index]))
		except:
			pass
	else:
		return BASE_MUSUH
print(getKompas())
drible()

"""while True:
	print(getIR())"""
#time.sleep(4)
#stop()
"""belakang()
stop()
time.sleep(7)
setMotor(-150,-150,-150)
drible(150)
time.sleep(7)
stop()
"""
"""kanan(-150)
kiri(-150)
drible(-150)
belakang(-150)
setMotor(-200,-220,-150)"""
