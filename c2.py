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
"""msg=client.recv(1024)
terima=msg.decode(ENCODING)
print("")
"""
def get_manual(mypesan):
	paramku=[]
	seplit=mypesan.split(',')
	#print(seplit)
	#0  1     2     3
	#M,DELAY,KIRI,KANAN
	paramku.append(int(seplit[1]))
	paramku.append(int(seplit[2]))
	paramku.append(int(seplit[3]))
	#
	delay=paramku[0]
	kiri=paramku[1]
	kanan=paramku[2]
	print(delay,kiri,kanan)
	ex_manual(delay,kiri,kanan)
	"""
	setMotor(kiri,kanan)
	time.sleep(delay)
	setMotor(0,0,0)"""
def ex_manual(delay,kiri,kanan,belakang=0):
	opop=''
	"""setMotor(kiri,kanan)
	time.sleep(delay)
	setMotor(0,0,0)"""
while True:

	terima=client.recv(SIZE).decode(ENCODING)
	
	if terima:
		if terima.startswith('M'):
			terima=terima.upper()
			print(terima)
			get_manual(terima)
		elif terima=='wahyu':
			print("COBA KIRIM TO SERVER")
			pesan=input()
			client.send(pesan.encode(ENCODING))	
		elif terima=='maju':
			oeee=''
			#setMotor(150,212,232)
		elif terima=='stop':
			#oeee=''
			stop()
		else:
			print(f"S| {terima} ")

	"""
	"""
	"""print("ENTER PESAN:")
	x=input()
	client.send(x.encode(ENCODING))"""
	#print("END PROGRAM")"""
	
