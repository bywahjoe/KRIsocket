import socket
import sys
import threading
import time 
import queue
from inputimeout import inputimeout, TimeoutOccurred
from configku import *

q=queue.Queue()

cname = socket.gethostname()
ip_address=socket.gethostbyname(socket.gethostname())
startclient=1
pesan='You Are Connected as CLIENT: '
ocl=[]


print(f"MAX DEVICE ALLOW : {TOTAL_CLIENT}")
print(f"+Computer:{cname}")
print(f"+IP      :{ip_address}")
print("+HOST    -    PORT")
print(JARINGAN)

try:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(JARINGAN)
	server.listen()
	#server.settimeout(5)
	print("**Starting Server")
except socket.error as e:
	print(f"ERROR {e}")

def multi_client(conn,address,myid):
	q.put(conn)
	print(f"Connection from {address} ")
	if  conn:
		print(f"CLIENT_ID: {myid} | {address}")
		pesan_pertama=pesan+str(myid)
		conn.send(bytes(pesan_pertama,ENCODING))
	while True:
		data = conn.recv(SIZE).decode(ENCODING)
		if data:
			print(f"C:{data} | {address}")	
def multi_send():
	while True:
		while not q.empty():
			ocl.append(q.get())
		print("exit")
		try:
			print(f"Thread Data Send 7 sec")
			print("C1[keyword] : CLIENT1 | C2[keyword] : CLIENT2 ")
			pesan = inputimeout(prompt='>>',timeout=7)
			if pesan.upper().startswith('C1') or pesan.upper().startswith('C2'):
				replace_pesan=(pesan[2:])
				#print(replace_pesan)
				client_index=int(pesan[1])-1
				#print(client_index)
				ocl[client_index].send(bytes(replace_pesan,ENCODING))
			else:
				for toall in ocl:
					toall.send(bytes(pesan,ENCODING))
		except TimeoutOccurred:
				print('timeout data send')	
				print('waiting data from client')
def device_conn():
	while not q.empty():
		ocl.append(q.get())
		print("CONN RECEIVE")

def play():
	DEVICE=0	
	pertama=True
	while True:
		
		conn,address= server.accept() 
		DEVICE=DEVICE+1
		print(f"[ACTIVE CONNECTIONS] {DEVICE}")
		thread = threading.Thread(target=multi_client, args=(conn, address,DEVICE))
		thread.start()
		#DEVICE=DEVICE+1
		#device=threading.activeCount() - 1
		if (DEVICE>=TOTAL_CLIENT and pertama==True):
			device_conn()
			pertama=False
			threadsent=threading.Thread(target=multi_send)
			threadsent.start()
play()

