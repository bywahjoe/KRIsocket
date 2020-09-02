import socket
import subprocess
import time
import os
import threading
from configku import *
from mainarduino import *

print("CLIENT VIEW **")
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"    Computer Name	   : {hostname}")
print(f"    IP Address   	   : {ip_address}")
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((JARINGAN))
#client.settimeout(0.1)
client.setblocking(0)
pesan='1st check'

def kirim(isi_pesan):
	isi_pesan=str(isi_pesan)
	client.send(isi_pesan.encode(ENCODING))
def get_manual(mypesan):
	paramku=[]
	seplit=mypesan.split(',')
	#print(seplit)
	#0  1     2     3	4
	#M,DELAY,KIRI,KANAN,BELAKANG
	paramku.append(int(seplit[1]))
	paramku.append(int(seplit[2]))
	paramku.append(int(seplit[3]))
	paramku.append(int(seplit[4]))
	#
	delay=paramku[0]
	kiri=paramku[1]
	kanan=paramku[2]
	blkg=paramku[3]

	print(kiri,kanan,blkg,delay)
	ex_manual(delay,kiri,kanan,blkg)
	"""
	setMotor(kiri,kanan)
	time.sleep(delay)
	setMotor(0,0,0)"""
def ex_manual(delay,kiri,kanan,belakang=0):
	setMotor(kiri,kanan,belakang)
	time.sleep(delay)
	stop()

def runArduinoCompass():

	#excecute='python serialkompas.py'
	#runCMD=subprocess.Popen(['python','serialkompas.py'], shell=True)
	os.system('start /wait cmd /k python serialkompas.py')
threadx = threading.Thread(target=runArduinoCompass,daemon=True)
threadx.start()
def otomatis():
	print('startwhile')
	play=True
	while play:
		##CODE
			
		try:
			new_message=client.recv(SIZE).decode(ENCODING)
			if new_message:
				return new_message
		except BlockingIOError:
			pass
		#print('continue')
	print('stopwhile')
while True:

	try:
		terima=client.recv(SIZE).decode(ENCODING)
		if terima:
			if terima=='auto':
				terima=otomatis()
			if terima.startswith('MNL'):
				terima=terima.upper()
				print(terima)
				get_manual(terima)
			elif terima=='wahyu':
				kirim('Masuk')
			elif terima=='stops':
				#oeee=''
				stop()
			elif terima=='selenoid':
				tendang()
			else:
				print(f"S| {terima} ")
	except BlockingIOError:
		pass