import socket
import sys
import threading
import time 
import datetime
import queue
import os
import tkinter.scrolledtext as listt
import keyboard
#import tkinter as tk
from perintah import *
from tkinter import *
from tkinter import messagebox as viewerror
from inputimeout import inputimeout, TimeoutOccurred
from configku import *


window=Tk()
window.title('Simple Server - Wahjoe Labs')
window.state('zoomed') 
window.configure(bg='#10171f')
#window.geometry('%dx%d+0+0' % (panjang,lebar))
MENU_HEADER='white'

#DEFAULT SENDER OPTION
getid=IntVar()
getid.set(3)
global mySendDefaultID
mySendDefaultID=getid.get()
#
strgy=IntVar()
strgy.set(1)
status_server=StringVar()
status_server.set('Not Running')


def_pwmup=StringVar()
def_pwmup.set('120')
def_pwmkiri=StringVar()
def_pwmkiri.set('-45,45')
def_pwmkanan=StringVar()
def_pwmkanan.set('45,-45')
def_pwmblkg=StringVar()
def_pwmblkg.set('20')

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
#text_command={'C1':'auto','C2':'stop','C3':'wahyu','CTST4':'selenoid'}	
pesan='You Are Connected as CLIENT: '
ocl=[]
print(f"MAX DEVICE ALLOW : {TOTAL_CLIENT}")
print(f"+Computer:{cname}")
print(f"+IP      :{ip_address}")
print("+HOST    -    PORT")
print(JARINGAN)

def fail(pesan_error):
	viewerror.showerror(title='!ERROR', message=pesan_error)
def notice(pesan_error):
	viewerror.showinfo(title='!NOTICE', message=pesan_error)
def getTime():
	now=datetime.datetime.now()
	waktu=str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'->'
	#print(waktu)
	return waktu
try:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(JARINGAN)
	print("**Starting Server")
except socket.error as e:
	#print(f"ERROR {e}")
	fail(e)
	#error_box()
def addToTerminal(myClientID,inputPesan):
	#				0		1		 2		  3		     4
	listSendID=['[SVR]:','[C:A]:','[C:B]:','[KIPER]:','[ALL]:']
	getLocalTime=getTime()
	pesanTerminal=getLocalTime+listSendID[myClientID]+inputPesan
	#
	list_area.configure(state='normal')
	list_area.insert('1.0',pesanTerminal+'\n')
	list_area.configure(state='disabled')
	#
	if myClientID==0:
		notice(pesanTerminal)
	print(pesanTerminal)
def sendToClient(myClientID,replace_pesan):
	conn_client[myClientID].send(bytes(replace_pesan,ENCODING))
def oky():
	while True:
		mtr='0,0,0'
		if(keyboard.is_pressed('w')):
			mtr='120,120,0,'
			print('w')
		if(keyboard.is_pressed('a')):
			print('a')
			mtr='-45,45,20,'
		if(keyboard.is_pressed('s')):
			print('s')
			mtr='-120,-120,0'
		if(keyboard.is_pressed('d')):
			print('d')
			mtr='45,-45,-20'
		if(keyboard.is_pressed('x')):
			print('STOP MANUAL KEYBOARD')
			notice('MANUAL -- STOP STREAM')
			break
		sendStreamKeyboard='KEY,'+mtr
		sendToClient(0,sendStreamKeyboard)
		time.sleep(0.2)
def streamKeyboard():
	print('ok')
	#topFrame=Toplevel(bg='blue')
	#topFrame.title('Stream Keyboard Mode - WAHJOE LABS')
	#topFrame.geometry('350x350+500+300')
	notice('PRESS X TO STOP MANUAL')
	threadk = threading.Thread(target=oky,daemon=True)
	threadk.start()
	

def ping_client():
	isi_pesan='PING'
	try:
		for toall in conn_client:
			toall.send(bytes(isi_pesan,ENCODING))
		notice('ALL CLIENT CONNECTED')
	except socket.error as e:
		text_error=str(e)+'\n ***CONECTION LOSS '
		fail(text_error)
def anotherClient(myid):
	print(f'MYID:{myid}','\nID:1 -->CLIENTA/1','\nID:2 -->CLIENTB/2')
	if myid==2:
		executeID=0
	else:
		executeID=1
	return executeID
def multi_client(conn,address,myid):
	if myid==1:
		ip_client1.set(ip_client[0])
	elif myid==2:
		ip_client2.set(ip_client[1])
	#
	addToTerminal(0,f'CLIENT from {address}')
	if  conn:
		#print(f"CLIENT_ID: {myid} | {address}")
		pesan_pertama=pesan+str(myid)
		conn.send(bytes(pesan_pertama,ENCODING))
		#sendToClient(,pesan_pertama)
	while True:
		try:
			data = conn.recv(SIZE).decode(ENCODING)
			if data:
				addToTerminal(myid,data)
				print(f"C:{data} | {address}")
				if data.startswith(FORWARDING_HEADER) and len(data)>4:
					removeHeaderFormat=data.replace(FORWARDING_HEADER,'')
					reverseClient=anotherClient(myid)
					sendToClient(reverseClient,removeHeaderFormat)
		except Exception as e:
			print(e)
			text_error=str(e)+'\n ***CLIENT CONECTION LOST '
			fail(text_error)
			break;
def multi_send(pesan):
	try:
		typePesan='SND|'
		print(f"""
		[MODE]{typePesan}
		1:CLIENT1
		2:CLIENT2
		3:ALL

		""")
		if pesan.startswith('MNL'):
			replace_pesan=pesan
		else:
			replace_pesan=text_command.get(pesan.upper())
		#
		index_client=getid.get()
		#
		print('SEND_TO_CLIENT:',index_client,': ',replace_pesan)
		#print(index_client)
		if index_client==mySendDefaultID:
			for toall in conn_client:
				toall.send(bytes(replace_pesan,ENCODING))
			index_client=4
		else:
			myClientID=index_client
			sendToClient(myClientID,replace_pesan)
			index_client=index_client+1
		addToTerminal(index_client,typePesan+replace_pesan)
	except Exception as e:
		fail(e)
def getStrategy():
	headerFormatStrategy='STRGY'
	print(strgy.get())
	pesan=headerFormatStrategy+str(strgy.get())
	multi_send(pesan)	
def send_manual(btn_id):
	
	param_up=abs(int(def_pwmup.get()))
	param_down=-1*(param_up)
	param_kiri=def_pwmkiri.get()
	param_kanan=def_pwmkanan.get()
	param_delay=delayp.get()
	param_blkg=abs(int(def_pwmblkg.get()))
	param_blkgMIN=-1*param_blkg

	isi_pesan='MNL,'+str(param_delay)+','
	print(f'UP:{param_up}')
	print(f'DOWN:{param_down}')
	print(f'KIRI:{param_kiri}')
	print(f'KANAN:{param_kanan}')
	print(f'BLKGKIRI:{param_blkg}')
	print(f'BLKGMIN:{param_blkgMIN}')
	print(f'DELAY:{param_delay}')
	print('__')
	
	#M,DELAY,LEFT,RIGHT
	if btn_id==1:
		isi_pesan=isi_pesan+str(param_up)+','+str(param_up)+',0'
	elif btn_id==2:
		isi_pesan=isi_pesan+str(param_down)+','+str(param_down)+',0'
	elif btn_id==3:
		#kiri
		isi_pesan=isi_pesan+param_kiri+','+str(param_blkg)
	elif btn_id==4:
		#kanan
		isi_pesan=isi_pesan+param_kanan+','+str(param_blkgMIN)
	isi_pesan=isi_pesan+','
	print(isi_pesan)
	multi_send(isi_pesan)
def start_server():
	print("LISTENING CLIENT...")
	DEVICE=0	
	while True:
		conn,address= server.accept() 
		conn_client.append(conn)
		ip_client.append(address)
		DEVICE=DEVICE+1
		print(f"[ACTIVE CONNECTIONS] {DEVICE}")
		thread = threading.Thread(target=multi_client, args=(conn, address,DEVICE),daemon=True)
		thread.start()
		if DEVICE>=TOTAL_CLIENT:
			try:
				ip_client1.set(ip_client[0])
				ip_client2.set(ip_client[1])
			except IndexError:
				pass
			break
def listen_client():
	bs1["state"] = "disable"
	bs1["bg"] = "black"
	try:
		server.listen()
		status_server.set('OK')
		tp2['fg']='green'
		tp2['font']='Courier 15 bold'
		thread2 = threading.Thread(target=start_server,daemon=True)
		thread2.start()
	except socket.error as e:
		fail(e)	

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
ts2.grid(row=1,column=1,sticky='W')
ts2=Label(window,text=PORT,bg='#10171f',font='Courier 11 bold',fg='white')
ts2.grid(row=2,column=1,pady=20,sticky='W')

frm=Frame(window,width='612',height='459',bg='green',bd=5,highlightbackground='white',highlightthickness=3)
frm.grid(row=0,column=2,rowspan=11,columnspan=5,padx=5,pady=3,sticky='W')

bs1=Button(window,text='Start Server',command=listen_client,bg='green',fg='white',width=10,height=3,font='Arial 11',activebackground='orange')
bs1.grid(row=4,column=0,padx=6)
bs2=Button(window,text='Close Server',command=window.quit,bg='red',fg='white',width=10,height=3,font='Arial 11')
bs2.grid(row=4,column=1)
#status server
tp2=Label(window,textvariable=status_server,bg='#10171f',fg='red',font='Courier 15')
tp2.grid(row=3,column=0,columnspan=2)


#send to
tr2=Label(window,text='SEND TO',font='Helvetica 10 bold',bg='blue',fg='white')
tr2.grid(row=5,column=0,sticky='EW',columnspan=2,pady=7)
rb1=Radiobutton(window,text='ALL',variable=getid,value=3,bg='black',fg='white',indicatoron=0,selectcolor='orange',font='Courier 15 italic')
rb2=Radiobutton(window,text='STRIKER A',variable=getid,value=0,bg='black',fg='white',indicatoron=0,selectcolor='orange',font='Courier 15 italic')
rb3=Radiobutton(window,text='STRIKER B',variable=getid,value=1,bg='black',fg='white',indicatoron=0,selectcolor='orange',font='Courier 15 italic')
rb4=Radiobutton(window,text='KIPER',variable=getid,value=3,bg='black',fg='white',indicatoron=0,selectcolor='orange',font='Courier 15 italic')
rb1.grid(row=6,column=0,sticky='EW',columnspan=2)
rb2.grid(row=7,column=0,sticky='EW',columnspan=2)
rb3.grid(row=8,column=0,sticky='EW',columnspan=2)
rb4.grid(row=9,column=0,sticky='EW',columnspan=2)


#STRATEGY
#CMD
tro2=Label(window,text='STRATEGY',font='Helvetica 10 bold',bg='#f7bb00')
tro2.grid(row=11,column=2,sticky='NWNE',columnspan=5)
st1=Radiobutton(window,text='STRATEGY1',variable=strgy,width=5,height=2,value=1,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st2=Radiobutton(window,text='STRATEGY2',variable=strgy,width=5,height=2,value=2,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st3=Radiobutton(window,text='DEFEND',variable=strgy,width=5,height=2,value=3,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st4=Radiobutton(window,text='STRIKER 1',variable=strgy,width=5,height=2,value=4,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st5=Radiobutton(window,text='MODECEPAT',variable=strgy,width=5,height=2,value=5,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st6=Radiobutton(window,text='TABRAK',variable=strgy,width=5,height=2,value=6,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st7=Radiobutton(window,text='FULLPOWER',variable=strgy,width=5,height=2,value=7,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st8=Radiobutton(window,text='UMPAN',variable=strgy,width=5,height=2,value=8,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st9=Radiobutton(window,text='AVOIDER',variable=strgy,width=5,height=2,value=9,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st10=Radiobutton(window,text='STRATEGY6',variable=strgy,width=5,height=2,value=10,bg='black',fg='white',indicatoron=0,selectcolor='red',font='Arial 12 italic bold')
st1.grid(row=12,column=2,sticky='EW',pady=4,padx=3)
st2.grid(row=12,column=3,sticky='EW',pady=4,padx=3)
st3.grid(row=12,column=4,sticky='EW',pady=4,padx=3)
st4.grid(row=12,column=5,sticky='EW',pady=4,padx=3)
st5.grid(row=12,column=6,sticky='EW',pady=4,padx=3)
st6.grid(row=13,column=2,sticky='EW',pady=4,padx=3)
st7.grid(row=13,column=3,sticky='EW',pady=4,padx=3)
st8.grid(row=13,column=4,sticky='EW',pady=4,padx=3)
st9.grid(row=13,column=5,sticky='EW',pady=4,padx=3)
st10.grid(row=13,column=6,sticky='EW',pady=4,padx=3)


trc2=Label(window,text='IP CLIENT',font='Helvetica 10 bold',bg='blue',fg='white')
trc2.grid(row=10,column=0,sticky='EW',columnspan=2,pady='3')
#IP CLIENT CHECK
txp1=Label(window,textvariable=ip_client1,width=22)
txp1.grid(row=11,column=0,columnspan=2)
txp2=Label(window,textvariable=ip_client2,width=22)
txp2.grid(row=12,column=0,columnspan=2)
txp2=Label(window,textvariable=ip_client3,width=22)
txp2.grid(row=13,column=0,columnspan=2)
print('START_DEFAULT_SENDER:',getid.get())


#command button
#
trn2=Label(window,text='COMMAND STATION',font='Helvetica 10 bold',bg='#f7bb00')
trn2.grid(row=0,column=7,sticky='EW',columnspan=6,pady=7)
b1=Button(window,text='AUTO',command=getStrategy,width=10,height=2,bg='#1BBC9B',font='Arial 10 bold',)
b2=Button(window,text='STOP',command=lambda: multi_send('C2'),width=10,height=2,bg='#1D9DCE',font='Arial 10 bold',fg='white')
b3=Button(window,text='RETRY',command=lambda: multi_send('C3'),width=10,height=2,bg='#1BBC9B',font='Arial 10 bold')
b4=Button(window,text='CORNER',command=lambda: multi_send('C3'),width=10,height=2,bg='#1D9DCE',font='Arial 10 bold',fg='white')
b5=Button(window,text='FREE KICK',command=lambda: multi_send('C3'),width=10,height=2,bg='#1BBC9B',font='Arial 10 bold')
b6=Button(window,text='RETRY',command=lambda: multi_send('C6'),width=10,height=2,bg='#1D9DCE',font='Arial 10 bold',fg='white')
b7=Button(window,text='RE-STRGY',command=lambda: multi_send('C7'),width=10,height=2,bg='#1BBC9B',font='Arial 10 bold')
b8=Button(window,text='TESTRECV',command=lambda: multi_send('C3'),width=10,height=2,bg='#1D9DCE',font='Arial 10 bold',fg='white')
b9=Button(window,text='TESTRECV',command=lambda: multi_send('C3'),width=10,height=2,bg='#1BBC9B',font='Arial 10 bold')
b10=Button(window,text='TESTRECV',command=lambda: multi_send('C3'),width=10,height=2,bg='#1D9DCE',font='Arial 10 bold',fg='white')
b11=Button(window,text='TESTRECV',command=lambda: multi_send('C3'),width=10,height=2,bg='#1BBC9B',font='Arial 10 bold')
b12=Button(window,text='TESTRECV',command=lambda: multi_send('C3'),width=10,height=2,bg='#1D9DCE',font='Arial 10 bold',fg='white')
b13=Button(window,text='TESTRECV',command=lambda: multi_send('C3'),width=10,height=2,bg='#1BBC9B',font='Arial 10 bold')
b14=Button(window,text='TESTRECV',command=lambda: multi_send('C3'),width=10,height=2,bg='#1D9DCE',font='Arial 10 bold',fg='white')
b15=Button(window,text='TESTRECV',command=lambda: multi_send('C3'),width=10,height=2,bg='#1BBC9B',font='Arial 10 bold')

b1.grid(row=1,column=8,sticky='EW',padx=3,pady=3)
b2.grid(row=1,column=9,sticky='EW',padx=3,pady=3)
b3.grid(row=1,column=10,sticky='EW',padx=3,pady=3)
b4.grid(row=1,column=11,sticky='EW',padx=3,pady=3)
b5.grid(row=1,column=12,sticky='EW',padx=3,pady=3)
b6.grid(row=2,column=8,sticky='EW',padx=3,pady=3)
b7.grid(row=2,column=9,sticky='EW',padx=3,pady=3)
b8.grid(row=2,column=10,sticky='EW',padx=3,pady=3)
b9.grid(row=2,column=11,sticky='EW',padx=3,pady=3)
b10.grid(row=2,column=12,sticky='EW',padx=3,pady=3)
b11.grid(row=3,column=8,sticky='EW',padx=3,pady=3)
b12.grid(row=3,column=9,sticky='EW',padx=3,pady=3)
b13.grid(row=3,column=10,sticky='EW',padx=3,pady=3)
b14.grid(row=3,column=11,sticky='EW',padx=3,pady=3)
b15.grid(row=3,column=12,sticky='EW',padx=3,pady=3)


trpn2=Label(window,text='TEST STATION',font='Helvetica 10 bold',bg='#f7bb00')
trpn2.grid(row=4,column=7,sticky='EW',columnspan=6,pady=7)
bxp1=Button(window,text='PING',command=ping_client,width=10,height=2,bg='green',font='Arial 10 bold',fg='white')
bxp2=Button(window,text='GET_IR',command=lambda: multi_send('TST2'),width=10,height=2,bg='red',font='Arial 10 bold',fg='white')
bxp3=Button(window,text='MOTOR',command=lambda: multi_send('TST3'),width=10,height=2,bg='green',font='Arial 10 bold',fg='white')
bxp4=Button(window,text='SELENOID',command=lambda: multi_send('TST4'),width=10,height=2,bg='red',font='Arial 10 bold',fg='white')
bxp5=Button(window,text='KOMPAS',command=lambda: multi_send('TST5'),width=10,height=2,bg='green',font='Arial 10 bold',fg='white')
bxp6=Button(window,text='TESTRECV',command=lambda: multi_send('TST6'),width=10,height=2,bg='red',font='Arial 10 bold',fg='white')
bxp7=Button(window,text='MYBALL',command=lambda: multi_send('TST7'),width=10,height=2,bg='green',font='Arial 10 bold',fg='white')
bxp8=Button(window,text='TESTRECV',command=lambda: multi_send('TST8'),width=10,height=2,bg='red',font='Arial 10 bold',fg='white')
bxp9=Button(window,text='TESTRECV',command=lambda: multi_send('TST9'),width=10,height=2,bg='green',font='Arial 10 bold',fg='white')
bxp10=Button(window,text='TESTRECV',command=lambda: multi_send('TST10'),width=10,height=2,bg='red',font='Arial 10 bold',fg='white')

bxp1.grid(row=5,column=8,sticky='EW',padx=3,pady=3)
bxp2.grid(row=5,column=9,sticky='EW',padx=3,pady=3)
bxp3.grid(row=5,column=10,sticky='EW',padx=3,pady=3)
bxp4.grid(row=5,column=11,sticky='EW',padx=3,pady=3)
bxp5.grid(row=5,column=12,sticky='EW',padx=3,pady=3)
bxp6.grid(row=6,column=8,sticky='EW',padx=3,pady=3)
bxp7.grid(row=6,column=9,sticky='EW',padx=3,pady=3)
bxp8.grid(row=6,column=10,sticky='EW',padx=3,pady=3)
bxp9.grid(row=6,column=11,sticky='EW',padx=3,pady=3)
bxp10.grid(row=6,column=12,sticky='EW',padx=3,pady=3)

#MANUAL
trpn2=Label(window,text='MANUAL STATION',font='Helvetica 10 bold',bg='#f7bb00')
trpn2.grid(row=7,column=7,sticky='EW',columnspan=6,pady=7)
trpn2=Label(window,text='BELAKANG : ',font='Helvetica 10 bold',bg='#f7bb00')
trpn2.grid(row=8,column=7,sticky='EW',columnspan=2)
pwm_blkg=Entry(window,bd=4,width=11,font='Arial 13 bold',textvariable=def_pwmblkg,justify='center')
pwm_blkg.grid(row=8,column=9)
btn_stream=Button(window,text='KEYBOARD',command=streamKeyboard,width=10,height=2,bg='#1D9DCE',font='Arial 10 bold',fg='white')
btn_stream.grid(row=8,column=12,sticky='EW')

be1=Button(window,text='UP',width=10,height=2,command=lambda: send_manual(1),bg='green',fg='white')
be1.grid(row=12,column=10)
be2=Button(window,text='DOWN',width=10,height=2,command=lambda: send_manual(2),bg='green',fg='white')
be2.grid(row=14,column=10,sticky='N')

be3=Button(window,text='LEFT',width=10,height=2,command=lambda: send_manual(3),fg='white',bg='red')
be3.grid(row=13,column=9,sticky='E')
be4=Button(window,text='RIGHT',width=10,height=2,command=lambda: send_manual(4),fg='white',bg='red')
be4.grid(row=13,column=11,sticky='W')

#
delayp=Spinbox(window,from_=1,to=5,width=8,font='Arial 13 bold')
delayp.grid(row=13,column=10)
pwm_kr=Entry(window,bd=4,width=9,font='Arial 13 bold',textvariable=def_pwmkiri,justify='center')
pwm_kr.grid(row=12,column=9,pady=7)
pwm_kn=Entry(window,bd=4,width=9,font='Arial 13 bold',textvariable=def_pwmkanan,justify='center')
pwm_kn.grid(row=12,column=11,pady=7)
pwm_up=Entry(window,bd=4,width=9,font='Arial 13 bold',textvariable=def_pwmup,justify='center')
pwm_up.grid(row=11,column=10,pady=7)

##LIST TERMINAL
list_area=listt.ScrolledText(window,width=75,height=5)
list_area.grid(row=14,column=2,columnspan=5)

#list_area.insert(INSERT,'ya'+'\n')
list_area.insert('1.0','NO DATA.....'+'\n')
list_area.configure(state='disabled')


window.mainloop()

