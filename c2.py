import socket
import time
from configku import *

number=0
print("CLIENT VIEW **")
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"    Computer Name	   : {hostname}")
print(f"    IP Address   	   : {ip_address}")
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((JARINGAN))
pesan='1st check'
#client.settimeout(0.1)
client.setblocking(0)
"""msg=client.recv(1024)
terima=msg.decode(ENCODING)
print("")
"""

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
	print('ok')
	"""setMotor(kiri,kanan,belakang)
	time.sleep(delay)
	stop()"""
def forward(inputPesan='LETSMOVE'):
	applyFormat=FORWARDING_HEADER+str(inputPesan)
	print(applyFormat)
	kirim(applyFormat)
def otomatis():
	print('startwhile')
	play=True
	while play:
		##CODE
			
		try:
			new_message=client.recv(SIZE).decode(ENCODING)
			if new_message:
				if new_message=='reauto':
					#ResetStep
					kirim('P:REAUTO')
					#CODE
				elif new_message=='retrycv':
					#AllMotorStop
					kirim('P:RETRYCV')
					#CODE
				elif new_message=='LETSMOVE':
					#HANDLE KONDISI SAAT FORWADING
					print('HANDLE')
				else:
					#DESTROYCV
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
				oeee=''
				#stop()
			elif terima=='selenoid':
				ok=''
			elif terima=='statusumpan':
				forward()
			else:
				print(f"S| {terima} ")
	except BlockingIOError:
		pass


