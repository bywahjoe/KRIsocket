import socket
import time
import datetime
import csv
from configku import *
from mainarduino import *
from megaserial import *

number=0
print("CLIENT VIEW **")
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"    Computer Name	   : {hostname}")
print(f"    IP Address   	   : {ip_address}")
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((JARINGAN))
pesan='1st check'
client.setblocking(0)


def getTime():
	now=datetime.datetime.now()
	waktu=str(now)
	# waktu=str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'->'
	#print(waktu)
	return waktu
	# return
def kirim(isi_pesan):
	logData("SEND",isi_pesan)
	isi_pesan=str(isi_pesan)
	client.send(isi_pesan.encode(ENCODING))

def createCSV(param):
	with open(f"tes_client.csv", "a", newline="") as f:
	    writer = csv.writer(f)
	    writer.writerow(param)
def logData(mode,msg):
	timestamp=str(getTime())
	unix=str(time.time())
	print('+--------------------+')
	print('Mode     : ',mode)
	print('Timestamp: ',timestamp)
	print('UNIX Time: ',unix)
	print('Message  : ',msg)
	print('Server   : ',JARINGAN)
	
	createCSV([mode,msg,unix,timestamp])

createCSV(['CLIENT IS START',getTime()])
while True:
	try:
		terima=client.recv(SIZE).decode(ENCODING)
		if terima:
			logData("RECV",str(terima))
			if terima=='cekDrible':
				drible(0)
				time.sleep(3)
				drible(255)
			elif terima=='tendang':
				tendang()
			elif terima=='setTendangHigh':
				tendang(1)
			elif terima=='setTendangHigh':
				tendang(0)
			elif terima=='motorPlus':
				setMotor(100,100,100)
			elif terima=='motorMin':
				setMotor(-100,-100,-100)
			elif terima=='myIR':
				kirim('StatusIR: '+str(getIR()))
			elif terima=='myKompas':
				kirim('LastKompas: '+str(getKompas()))
			elif terima=='myEncoder':
				kirim('Rotate L/R: '+str(getRotateL())+'/'+str(getRotateR()))
	except BlockingIOError:
		pass


