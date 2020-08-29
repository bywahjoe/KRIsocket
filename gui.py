import socket
import sys
import threading
import time 
import queue
import os
import tkinter.scrolledtext as listt
#import tkinter as tk
from tkinter import *
from tkinter import messagebox as viewerror

from inputimeout import inputimeout, TimeoutOccurred
from configku import *

window=Tk()
window.title('Simple Server - Wahjoe Labs')
#window.attributes('-fullscreen', True) 

window.configure(bg='#10171f')
window.geometry('1366x720')
MENU_HEADER='white'
getid=IntVar()
getid.set(3)
status_server=StringVar()
status_server.set('Not Running')


def_pwmup=StringVar()
def_pwmup.set('150')
def_pwmkiri=StringVar()
def_pwmkiri.set('-45,45')
def_pwmkanan=StringVar()
def_pwmkanan.set('45,-45')

pesan='You Are Connected as CLIENT: '
conn_client=[]
ip_client=[]
ip_client1=StringVar()
ip_client1.set('0.0.0.0')
ip_client2=StringVar()
ip_client2.set('0.0.0.0')
ip_client3=StringVar()
ip_client3.set('0.0.0.0')

cname = socket.gethostname()
ip_address=socket.gethostbyname(socket.gethostname())
text_command={'C1':'auto','C2':'stop','C3':'wahyu'}	
pesan='You Are Connected as CLIENT: '
ocl=[]
print(f"MAX DEVICE ALLOW : {TOTAL_CLIENT}")
print(f"+Computer:{cname}")
print(f"+IP      :{ip_address}")
print("+HOST    -    PORT")
print(JARINGAN)

startclient=10
def fail(pesan_error):
	viewerror.showwarning(title='!ERROR', message=pesan_error)
try:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(JARINGAN)
	print("**Starting Server")
except socket.error as e:
	#print(f"ERROR {e}")
	fail(e)
	#error_box()
	
#def error_box():
#	messagebox.showerror("YA")
def multi_client(conn,address,myid):
	conn_client.append(conn)
	ip_client.append(address)
	hola=f"[C:{myid}]:CLIENT from {address} "
	print(hola)
	list_area.configure(state='normal')
	list_area.insert('1.0',hola+'\n')
	list_area.configure(state='disabled')
	if  conn:
		print(f"CLIENT_ID: {myid} | {address}")
		pesan_pertama=pesan+str(myid)
		conn.send(bytes(pesan_pertama,ENCODING))
	while True:
		data = conn.recv(SIZE).decode(ENCODING)
		if data:
			hola=f"[C:{myid}]:{data}"
			print(f"C:{data} | {address}")	
			list_area.configure(state='normal')
			list_area.insert('1.0',hola+'\n')
			list_area.configure(state='disabled')
def multi_send(pesan):
	if pesan.startswith('C'):
		replace_pesan=text_command.get(pesan.upper())
	else:
		replace_pesan=pesan

	index_client=getid.get()
	print(replace_pesan)
	print(index_client)

	list_area.configure(state='normal')
	if index_client==3:
		for toall in conn_client:
			toall.send(bytes(replace_pesan,ENCODING))
		hola=f'[ALL]:{replace_pesan}'
		list_area.insert('1.0',hola+'\n')
	else:
		conn_client[index_client].send(bytes(replace_pesan,ENCODING))
		hola=f'[S:{index_client+1}]:{replace_pesan}'
		list_area.insert('1.0',hola+'\n')
	list_area.configure(state='disabled')
def send_manual(btn_id):
	
	param_up=abs(int(def_pwmup.get()))
	param_down=-1*(param_up)
	param_kiri=def_pwmkiri.get()
	param_kanan=def_pwmkanan.get()
	param_delay=delayp.get()

	isi_pesan='M,'+str(param_delay)+','
	print(f'UP:{param_up}')
	print(f'DOWN:{param_down}')
	print(f'KIRI:{param_kiri}')
	print(f'KANAN:{param_kanan}')
	print(f'DELAY:{param_delay}')
	print('__')
	
	#M,DELAY,LEFT,RIGHT
	if btn_id==1:
		isi_pesan=isi_pesan+str(param_up)+','+str(param_up)
	elif btn_id==2:
		isi_pesan=isi_pesan+str(param_down)+','+str(param_down)
	elif btn_id==3:
		#kiri
		isi_pesan=isi_pesan+param_kiri
	elif btn_id==4:
		#kanan
		isi_pesan=isi_pesan+param_kanan
	isi_pesan=isi_pesan+','
	print(isi_pesan)
	multi_send(isi_pesan)
def start_server():

	print("LISTENING CLIENT...")
	DEVICE=0	
	while True:
		conn,address= server.accept() 
		DEVICE=DEVICE+1
		print(f"[ACTIVE CONNECTIONS] {DEVICE}")
		thread = threading.Thread(target=multi_client, args=(conn, address,DEVICE),daemon=True)
		thread.start()
		if DEVICE>=TOTAL_CLIENT:
			ip_client1.set(ip_client[0])
			ip_client2.set(ip_client[1])
			break
def listen_client():
	bs1["state"] = "disable"
	bs1["bg"] = "black"
	try:
		server.listen()
		status_server.set('OK')
		tp2['fg']='green'
		thread2 = threading.Thread(target=start_server,daemon=True)
		thread2.start()
	except socket.error as e:
		fail(e)		
def get_radio():

	x=getid.get()
	print(x)

def open_server():
	os.system('python server.py')
def get_manual():
	print('ok')
#server start
ts1=Label(window,text='SERVER',font='Helvetica 10 bold',bg='#f7bb00')
#ts1.config(bg='red')
#ts1.grid.SetBackgroundColour(red)
ts1.grid(row=0,column=0,sticky='EW',columnspan=2)
tsy=Label(window,text='IP SERVER : ',bg='#10171f',fg='white',font='Courier 11')
tsy.grid(row=1,column=0,sticky='E',padx=7)
tsy=Label(window,text='PORT : ',bg='#10171f',fg='white',font='Courier 11')
tsy.grid(row=2,column=0,sticky='E',padx=7)
ts2=Label(window,text=ip_address,bg='#10171f',font='Courier 11 bold',fg='white')
ts2.grid(row=1,column=1,sticky='E')
ts2=Label(window,text=PORT,bg='#10171f',font='Courier 11 bold',fg='white')
ts2.grid(row=2,column=1,pady=20,sticky='W')

frm=Frame(window,width='650',height='300',bg='green',bd=5,highlightbackground='white',highlightthickness=3)
frm.grid(row=0,column=2,rowspan=10,padx=5,pady=3)

bs1=Button(window,text='Start Server',command=listen_client,bg='green',fg='white',width=10,height=3,font='Arial 11',activebackground='orange')
bs1.grid(row=0,column=8,padx=6)
bs2=Button(window,text='Close Server',command=window.quit,bg='red',fg='white',width=10,height=3,font='Arial 11')
bs2.grid(row=0,column=10)


#status server

tp2=Label(window,textvariable=status_server,bg='#10171f',fg='red',font='Courier 15')
tp2.grid(row=0,column=3)
#send to
tr2=Label(window,text='SEND TO',font='Helvetica 10 bold',bg='#f7bb00')
tr2.grid(row=4,column=0,sticky='EW',columnspan=2)
rb1=Radiobutton(window,text='ALL',variable=getid,value=3,bg='black',fg='white',indicatoron=0,selectcolor='orange',font='Courier 15 italic')
rb2=Radiobutton(window,text='STRIKER A',variable=getid,value=0,bg='black',fg='white',indicatoron=0,selectcolor='orange',font='Courier 15 italic')
rb3=Radiobutton(window,text='STRIKER B',variable=getid,value=1,bg='black',fg='white',indicatoron=0,selectcolor='orange',font='Courier 15 italic')
rb4=Radiobutton(window,text='KIPER',variable=getid,value=3,bg='black',fg='white',indicatoron=0,selectcolor='orange',font='Courier 15 italic')
rb1.grid(row=5,column=0,sticky='EW',columnspan=2)
rb2.grid(row=6,column=0,sticky='EW',columnspan=2)
rb3.grid(row=7,column=0,sticky='EW',columnspan=2)
rb4.grid(row=8,column=0,sticky='EW',columnspan=2)

trc2=Label(window,text='IP CLIENT',font='Helvetica 10 bold',bg='#f7bb00')
trc2.grid(row=4,column=3,sticky='EW',columnspan=2)
#IP CLIENT CHECK
txp1=Label(window,textvariable=ip_client1,width=22)
txp1.grid(row=6,column=3)
txp2=Label(window,textvariable=ip_client2,width=22)
txp2.grid(row=7,column=3)
txp2=Label(window,textvariable=ip_client3,width=22)
txp2.grid(row=8,column=3)
print(getid.get())


#command button
cpr1=Label(window,text='#COMMAND',font='Helvetica 10 bold')
cpr1.grid(row=10,column=0)
cpr2=Label(window,text='MANUAL',font='Helvetica 10 bold')
cpr2.grid(row=10,column=2,sticky='w')
#
b1=Button(window,text='AUTO',command=lambda: multi_send('C1'),width=9)
b1.grid(row=15,column=0,sticky='w')
b2=Button(window,text='STOP',command=lambda: multi_send('C2'),width=7)
b2.grid(row=15,column=1,sticky='w')
be2=Button(window,text='TESTRECV',command=lambda: multi_send('C3'),width=7)
be2.grid(row=8,column=0,sticky='w')
b3=Label(window,text='MANUAL',font='Helvetica 10 bold')
b3.grid(row=6,column=2,sticky='w')
#
be1=Button(window,text='UP',width=7,command=lambda: send_manual(1))
be1.grid(row=7,column=13)
be2=Button(window,text='DOWN',width=7,command=lambda: send_manual(2))
be2.grid(row=9,column=13)

be3=Button(window,text='LEFT',width=7,command=lambda: send_manual(3))
be3.grid(row=8,column=12,sticky='w')
be4=Button(window,text='RIGHT',width=7,command=lambda: send_manual(4))
be4.grid(row=8,column=14)

#
delayp=Spinbox(window,from_=1,to=5,width=5)
delayp.grid(row=8,column=3)
pwm_kr=Entry(window,bd=4,width=8,textvariable=def_pwmkiri)
pwm_kr.grid(row=9,column=2)
pwm_kn=Entry(window,bd=4,width=8,textvariable=def_pwmkanan)
pwm_kn.grid(row=9,column=4)
pwm_up=Entry(window,bd=4,width=8,textvariable=def_pwmup)
pwm_up.grid(row=7,column=4)

##LIST
label_list=Label(window,text='#DATA LOG',font='Helvetica 10 bold')
label_list.grid(row=11,column=0,sticky='w')
list_area=listt.ScrolledText(window,width=40,height=5)
list_area.grid(row=12,column=0,columnspan=5)

#list_area.insert(INSERT,'ya'+'\n')
list_area.insert('1.0','NO DATA.....'+'\n')
list_area.configure(state='disabled')

#list_area.insert('ok')
#startserver.pack()
#window.after(0,play)
window.mainloop()

