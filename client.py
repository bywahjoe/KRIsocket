import socket
import time
import os
import threading
import multiprocessing
from configku import *
from mainarduino import *

#ADD
import cv2
import argparse
import numpy as np
import pickle

#CV
print('Camera Index Using: ',MAIN_CAMERA)
camera = cv2.VideoCapture(MAIN_CAMERA,cv2.CAP_DSHOW)
print(statusauto)
STEP_ROBOT=0

PIDX=0
print('CLIENT VIEW **,CMD PID:',os.getpid())
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"    Computer Name      : {hostname}")
print(f"    IP Address         : {ip_address}")
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((JARINGAN))
#client.settimeout(0.1)
client.setblocking(0)
pesan='1st check'

def testThreadMotor(delay,kiri,kanan,belakang=0):
    myThread=threading.Thread(target=ex_manual,args=(delay,kiri,kanan,belakang),daemon=True)
    myThread.start()
def kirim(isi_pesan):
    isi_pesan=str(isi_pesan)
    client.send(isi_pesan.encode(ENCODING))
def get_manual(mypesan):
    paramku=[]
    seplit=mypesan.split(',')
    #print(seplit)
    #0  1     2     3   4
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
def getStreamKeyboard(mypesan):
    new_pesan=mypesan.split(',',4)
    kiri=int(new_pesan[1])
    kanan=int(new_pesan[2])
    belakang=int(new_pesan[3])
    setMotor(kiri,kanan,belakang)
def runArduinoCompass():
    #excecute='python serialkompas.py'
    #runCMD=subprocess.Popen(['python','serialkompas.py'], shell=True)  
    os.system('start /wait cmd /k python serialkompas.py')
    PIDX=os.getpid()
    print(PIDX)
"""threadx = threading.Thread(target=runArduinoCompass,daemon=True)
threadx.start()"""

def forward(inputPesan='LETSMOVE'):
    applyFormat=FORWARDING_HEADER+str(inputPesan)
    print(applyFormat)
    kirim(applyFormat)

def destroyRobot():
    STEP_ROBOT=0
    resetRobot()
    cv2.destroyAllWindows()
    kirim('DESTROYCV->'+statusauto)
    
    return statusauto

def retryRobot():
    STEP_ROBOT=99
    resetRobot()
    kirim('P:RETRYCV')

def playRobot():
    STEP_ROBOT=0
    kirim('P:REAUTO:'+statusauto)

def refreshServer():
    global statusauto
    try:
        new_message=client.recv(SIZE).decode(ENCODING)
        if new_message:
            if new_message.startswith('auto'):
                #ResetStep
                if(statusauto!=new_message):
                    statusauto=new_message
                    destroyRobot()
                else:
                    playRobot()
            elif new_message=='retry':
                retryRobot()                
            elif new_message=='destroy':
                destroyRobot()
            elif new_message=='LETSMOVE':
                #HANDLE KONDISI SAAT FORWADING
                print('HANDLE')
            else:
                print('Undefined Msg')
                kirim(new_message)
    except BlockingIOError:
        pass

def otomatis1():
    while play:
        camera.set(28, cv2.CAP_PROP_AUTOFOCUS)
        ret, image = camera.read()
        image = cv2.flip(image, 1)

        if not ret:
            break
        key = cv2.waitKey(1)

        cv2.imshow(statusauto, image)
        refreshServer()

    print('UNIT Test : otomatis1')    
def otomatis2():
    print('UNIT Test : otomatis2')
def otomatis3():
    print('UNIT Test : otomatis3')

while True:
    try:
        terima=client.recv(SIZE).decode(ENCODING)
        if terima:
            #MAIN Block
            if terima.startswith('auto'):           
                # global statusauto
                statusauto=terima
                print(statusauto)

                if terima=='auto1':
                    statusauto=otomatis1()
                elif terima=='auto2':
                    statusauto=otomatis2()
                elif terima=='auto3':
                    statusauto=otomatis3()
                
            #OPTIONAL                       
            if terima.startswith('MNL'):
                terima=terima.upper()
                print(terima)
                get_manual(terima)
            elif terima.startswith('KEY'):
                print(terima)
                getStreamKeyboard(terima)
            elif terima=='wahyu':
                kirim('Masuk')
            elif terima=='testmotor':
                ex_manual(3,150,150,150)
                ex_manual(3,-150,-150,-150)
            elif terima=='stops':
                #oeee=''
                stop()
            elif terima=='getir':
                kirim(getAllMyIR())
            elif terima=='selenoid':
                tendang()
            elif terima=='statusumpan':
                forward()
            elif terima=='kompas':
                kirim(getKompas())
                print(getKompas())
            else:
                print(f"S| {terima} ")

    except BlockingIOError:
        pass
    except ConnectionResetError:
        stop()
        os.system('taskkill /IM "python.exe" /F')
    except Exception as e:
        print(e)
        pass