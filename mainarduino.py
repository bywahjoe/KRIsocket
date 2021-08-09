import time
import pyfirmata
import os
import threading
from ardupin import *
from configku import *

board = pyfirmata.ArduinoMega(ARDUINO_COM_PORT)
#board = pyfirmata.Arduino('COM3')
it=pyfirmata.util.Iterator(board)
it.start()
#RELAY/PENENDANG
PENENDANG=board.get_pin(PENENDANG_PIN)
MODE_PENENDANG=board.get_pin(MODE_PENENDANG_PIN)
#INFRARED
IR_KIRI=board.get_pin(IR_PIN_KIRI)
IR_KIRI2=board.get_pin(IR_PIN_KIRI2)
IR_TENGAH=board.get_pin(IR_PIN_TENGAH)
IR_KANAN=board.get_pin(IR_PIN_KANAN)
IR_KANAN2=board.get_pin(IR_PIN_KANAN2)
#MOTOR
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
##
modeSelenoid=0
##
def customThread(fungsiThread):
	myThread=threading.Thread(target=fungsiThread,daemon=True)
	myThread.start()
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
def rem(varKiri=1,varKanan=1,varBelakang=1):
	if varKiri==1:
		EON1_KIRI.write(1)
		EON2_KIRI.write(1)
		LPWM_KIRI.write(1)
		RPWM_KIRI.write(1)
	else:
		kiri(0)
	#
	if varKanan==1:
		EON1_KANAN.write(1)
		EON2_KANAN.write(1)
		LPWM_KANAN.write(1)
		RPWM_KANAN.write(1)
	else:
		kanan(0)
	#
	if varBelakang==1:
		EON1_BELAKANG.write(1)
		EON2_BELAKANG.write(1)
		LPWM_BELAKANG.write(1)
		RPWM_BELAKANG.write(1)
	else:
		belakang(0)
	print('REM STATUS:',varKiri,varKanan,varBelakang)
def stop():
	setMotor()
def setMotor(motor_kiri=0,motor_kanan=0,motor_belakang=0):
	kiri(motor_kiri)
	kanan(motor_kanan)
	belakang(motor_belakang)
def nonBlockingKicker():
	print('mulai tendang')
	PENENDANG.write(1)#AKTIF HIGH
	time.sleep(2)
	PENENDANG.write(0)
def modeTendang(value=0):
	global modeSelenoid
	if value==0:
		MODE_PENENDANG.write(value)
		print('SET NEXT:MODE LOW POWER')
		modeSelenoid=value
	elif value==1:
		MODE_PENENDANG.write(value)
		print('SET NEXT:MODE HIGH POWER')
		modeSelenoid=value
	else:
		print('SET NEXT:MODE NOT CHANGE')
def getSelenoidMode():	
	if modeSelenoid==0:
		myMode='RUNNING_MODE: LOW POWER'
	elif modeSelenoid==1:
		myMode='RUNNING_MODE: HIGH POWER'
	else:
		myMode='NULL'
	return myMode
def tendang(MODE=2):
	#0=LOW POWER
	#1=HIGH POWER
	#2=DEFAULT
	drible(0)
	print('\nmulai tendang_',getSelenoidMode())
	PENENDANG.write(1)#AKTIF HIGH
	time.sleep(1.5)
	PENENDANG.write(0)
	drible(180)
	#CHANGE MODE
	modeTendang(MODE)
def resetTendang(value=0):
	#0=LOW
	#1=HIGH
	print('RESET-- ')
	tendang(value)
#IR
#    _2\ 3 /4_
#  1/   \ /   \5
#  /           \
def getIRKiri2():
	#1
	return not IR_KIRI2.read()
def getIRKiri():
	#2
	return not IR_KIRI.read()
def getIR():
	#3
	return not IR_TENGAH.read()
def getIRKanan():
	#4
	return not IR_KANAN.read()
def getIRKanan2():
	#5
	return not IR_KANAN2.read()
def getAllMyIR():
	statusIR=[]
	#kiri2,kiri,tengah,kanan,kanan2
	statusIR.append(getIRKiri2())
	statusIR.append(getIRKiri())
	statusIR.append(getIR())
	statusIR.append(getIRKanan())
	statusIR.append(getIRKanan2())
	return statusIR
def fileKompasNotEmpty():
	get_status=os.stat(FILE_KOMPAS).st_size>0
	return get_status
def getKompas(index=0):
	#HEADING1,HEADING2,TIMELOG
	batasError=0
	while True:
		
		try:
			file=open(FILE_KOMPAS,READ_FILE)
			dataAsli=file.readline()
			file.close()
			pecahData=dataAsli.split(',')[0]
			#print(pecahData)
			if pecahData and pecahData.strip():
				sendKompas=int(float(pecahData))
				return sendKompas
		except Exception as e:
			print('FAIL: ',e)
			print(pecahData)
			#time.sleep(5)
			pass
		if batasError==3:
			print('READ FILE ERROR')
			#time.sleep(5)
			return BASE_MARKAS
			break;
		batasError=batasError+1			
def lockTarget(setRange=ERROR_RATE,position=BASE_MUSUH):
	try:
		myKompas=getKompas()
	except Exception as e:
		print(e)
		return False
	if(setRange==ERROR_RATE) and (position==BASE_MUSUH):
		rangeKompas=myKompas>=BASE_MUSUH_MIN and myKompas<=BASE_MUSUH_MAX
		print('STATUS\t\t: ',rangeKompas,'\nRANGE_RATE\t: ',setRange,'\nBASE_MUSUH_MIN\t: ',BASE_MUSUH_MIN,'\nKOMPAS_VALUE\t: ',myKompas,'\nBASE_MUSUH_MAX\t: ',BASE_MUSUH_MAX)
		return rangeKompas
	else:
		NEW_BASE_MUSUH_MIN=(position-setRange)%360
		NEW_BASE_MUSUH_MAX=(position+setRange)%360
		rangeKompas=myKompas>=NEW_BASE_MUSUH_MIN and myKompas<=NEW_BASE_MUSUH_MAX
		print('STATUS\t\t: ',rangeKompas,'\nRANGE_RATE\t: ',setRange,'\nBASE_MUSUH_MIN\t: ',NEW_BASE_MUSUH_MIN,'\nKOMPAS_VALUE\t: ',myKompas,'\nBASE_MUSUH_MAX\t: ',NEW_BASE_MUSUH_MAX)
		return rangeKompas
def destroyTarget(setRange=ERROR_RATE,position=BASE_MUSUH):
	if(lockTarget(setRange,position)):
		stop()
		tendang()
		return True 
	else:
		print('POSITION FAILED')
		return False
def startSerialKompas():
	os.system('start /wait cmd /k python serialkompas.py')
def openKompas():
	threadKompas = threading.Thread(target=startSerialKompas,daemon=True)
	threadKompas.start()
#openKompas()
drible(180)
# modeTendang(1)
resetTendang()
# setMotor(150,150,150)
# while True:
# 	setMotor(100,100,100)
# 	time.sleep(5)
# 	setMotor(-100,-100,-100)
# 	time.sleep(5)
#kanan()
"""while True:
	time.sleep(10)
	tendang()"""
#tendang()
#modeTendang(1)
#rem()
"""while True:
	print(getAllMyIR())"""
#tendang()
#tendang(1)
#tendang(0)
#tendang()
"""tendang()
setTendang()
#tendang()
while True:
	time.sleep(10)
	tendang()
	setTendang(1)
	time.sleep(20)
	tendang()
	setTendang()"""
"""play=True
setMotor(50,50,0)
while play:
	print(getAllMyIR())
	a=getIRKiri()
	b=getIRKanan()
	print(a,b)
	if a:
		print('aaa')
		stop()
	elif b:
		stop()
		print('bbb')
	else:
		setMotor(100,100,0)"""
#print(lockTarget())
#print(destroyTarget())

"""while True:
	tendang(1)
	time.sleep(5)
	tendang(0)	
	time.sleep(5)	"""
"""
while True:
	getarah=lockTarget(14,198)
	if getarah:
		stop()
		tendang()
		break
	setMotor(50,-50,-50)"""
