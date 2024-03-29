import socket
import time
import os
import threading
import multiprocessing
from configku import *
from mainarduino import *

###ADD
import cv2
import argparse
import numpy as np
import pickle

#CV
print('Camera Index Using: ',MAIN_CAMERA)
camera = cv2.VideoCapture(MAIN_CAMERA,cv2.CAP_DSHOW)
print(statusauto)

#Var
jumpAnotherAuto=False
STEP_ROBOT = 0
PIDX=0
miss=False

now=time.time()
before=time.time()
lastL,lastR=0,0
#SOCKET
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
def pasTengah(dataX, center,range):
    if dataX>center-range and dataX<center+range:
        return True
    else:
        return False
def pasne(dataX, center,range, speed):
    if pasTengah(dataX, center,range):
        rem()
    else:
        if dataX>center:
            setMotor(speed,-speed,-speed-5)
        else:
            setMotor(-speed,speed,speed+5)

def forward(inputPesan='LETSMOVE'):
    applyFormat=FORWARDING_HEADER+str(inputPesan)
    print(applyFormat)
    kirim(applyFormat)

def checkNewMessageAutoAgain():
    global statusauto,play,jumpAnotherAuto
    if jumpAnotherAuto:
        play=True
        jumpAnotherAuto=True
        if statusauto=='auto1':
            print('Go Otomatis1')
            otomatis1()
        elif statusauto=='auto2':
            print('Go Otomatis2')
            otomatis2()
        elif statusauto=='auto3':
            print('Go Otomatis3')
            otomatis3()

def destroyRobot():
    global play,STEP_ROBOT
    play=False

    STEP_ROBOT=0
    resetRobot()
    cv2.destroyAllWindows()
    kirim('DESTROYCV->'+statusauto)
def retryRobot():
    global STEP_ROBOT,error,last_error
    error,last_error=0,0
    STEP_ROBOT=99
    
    resetRobot()
    kirim('P:RETRYCV')
def playRobot():
    global STEP_ROBOT
    STEP_ROBOT=0
    kirim('P:REAUTO:'+statusauto)

def refreshServer():
    global statusauto,play,jumpAnotherAuto
    try:
        new_message=client.recv(SIZE).decode(ENCODING)
        if new_message:
            if new_message.startswith('auto'):
                #ResetStep
                if(statusauto!=str(new_message)):
                    statusauto=new_message
                    destroyRobot()
                    jumpAnotherAuto=True                
                else:
                    playRobot()
            elif new_message=='retry':
                retryRobot()                
            elif new_message=='destroy':
                destroyRobot()
                jumpAnotherAuto=False
            elif new_message=='LETSMOVE':
                #HANDLE KONDISI SAAT FORWADING
                print('HANDLE')
            else:
                print('Undefined Msg')
                kirim(new_message)
    except BlockingIOError:
        pass

    print('startwhile')

data_ball = pickle.load(open("data_ball.dat", "rb"))
data_bolo = pickle.load(open("data_bolo.dat", "rb"))
data_gawang = pickle.load(open("data_gawang.dat", "rb"))

data_ball2 = pickle.load(open("data_ball2.dat", "rb"))
data_bolo2 = pickle.load(open("data_bolo2.dat", "rb"))
data_gawang2 = pickle.load(open("data_gawang2.dat", "rb"))

data_ball3 = pickle.load(open("data_ball3.dat", "rb"))
data_bolo3 = pickle.load(open("data_bolo3.dat", "rb"))
data_gawang3 = pickle.load(open("data_gawang3.dat", "rb"))

# variable konversi
error = 0
last_error = 0
kp = 5
kd = 20
SPEED = 80
max_speed = 80

centerBallX=322
centerBoloX=346
centerGawangX=359
centerGawangT=325
centerGawangO=503
gawangDummy2=504
gawangTendang1=328
gawangTendang2=350
centerX = 331
centerY = 239


def pid(ballX,centerX, last_error, range = 10, current_speed = SPEED):
    error = konversi(ballX, centerX,range)
    rate_error = error - last_error
    last_error = error

    move_value = (error * kp) + (rate_error * kd)
    move_left = current_speed + move_value
    move_right = current_speed - move_value

    if move_left > max_speed:
        move_left = max_speed
    elif move_left < -max_speed:
        move_left = -max_speed
    if move_right < -max_speed:
        move_right = -max_speed
    elif move_right > max_speed:
        move_right = max_speed

    print("move_right" + str(move_right))
    print("move_left" + str(move_left))

    return [move_left, move_right]

def konversi(ballX,centerX,  range):
    if ballX > centerX + (range/2):
        return (ballX - centerX) / 10
    elif ballX < centerX - (range/2):
        return ((centerX - ballX) * -1) / 10
    else:
        return 0
def saveLast():
    global lastL,lastR

    lastL=getRotateL()
    lastR=getRotateR()
def pasKompas(sudut,range):
    kom=getKompas()
    if kom<=sudut+range and kom>=sudut-range:
        return True
    else:
        return False
        
def gakenek(timer):
    global now,before

    now=time.time()
    var=now-before

    statusIR=getIR is False
    print("var: ",var)
    print("Status IR", statusIR)

    if statusIR is False and var>timer:
        print("MASUK GAKENEK")
        return True
    else:
        return False
"""def getKompas():
    return 1
def getRotateL():
    return 2
def getRotateR():
    return 8
def getPulseL():
    return 4
def getPulseR():
    return 5
def getSerial():
    return 6,7,8,9,0"""

####################################
from struct import *
import serial
import threading


ser = serial.Serial(PYSERIAL_COM,baudrate=BAUDRATE)
# ser.reset_output_buffer()

# ok=b'\x05\x00\x00\x00\x07\x00\x00\x00'
# print(unpack('ii',ok))

myKompas,rotateL,rotateR,pulseL,pulseR=0,0,0,0,0
def readSerial():
    global myKompas,rotateL,rotateR,pulseL,pulseR
    while True:
        recv=ser.read(20)
        # recv=ser.readline()
        # ok=len(recv)
        print(repr(recv))
        # print(len(recv),' bytes')
        if(len(recv)>4):
            unpacked = unpack('iiill', recv)
            print(unpacked)
            myKompas,rotateL,rotateR,pulseL,pulseR=unpacked
            # myKompas=unpacked[0]
            # rotateL=unpacked[1]
            # rotateR=unpacked[2]
            # pulseL=unpacked[3]
            # pulseR=unpacked[4]

            # print(type(unpacked[0]))
            # print(type(unpacked[1]))
            # print(type(unpacked[2]))
            # print(type(unpacked[3]))
            # print(type(unpacked[4]))
            # print(mykompas)

#THREAD TEST!!
x = threading.Thread(target=readSerial,daemon=True)
x.start()
###########################################
def getKompas():
    return myKompas
def getRotateL():
    return rotateL
def getRotateR():
    return rotateR
def getPulseL():
    return pulseL
def getPulseR():
    return pulseR
def getSerial():
    return myKompas,rotateL,rotateR,pulseL,pulseR

print('Load Serial.....')



def otomatis1():
    print("START")

    global STEP_ROBOT,play,now,before,miss,lastL,lastR
    # * Variable Init
    is_ball_found = False
    is_gawang_found = False
    is_bolo_found = False
    ballX = 0
    ballY = 0
    boloX,boloY=0,0
    centerPasGawang=506
    centerBoloO=333

    while play:
        print("Masuk While")
        camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        ret, image = camera.read()
        image = cv2.flip(image, 1)

        if not ret:
            break

        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        kernel = np.ones((5, 5), np.uint8)

        #!---------- PROGRAM CAMERA BALL STARTS HERE ----------

        # * find mask gawang
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = data_ball

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskBall = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # * find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            ballX = center[0]
            ballY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((ballX, ballY))
            jarak_ball = np.linalg.norm(a-b)
            jarak_ball = int(jarak_ball)
            print("jarak_ball = " + str(jarak_ball))

            if radius > 3:
                is_ball_found = True
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                    image, "Ball", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                               10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            else:
                is_ball_found = False

        #!---------- PROGRAM CAMERA BALL ENDS HERE ----------

        #!---------- PROGRAM CAMERA BOLO STARTS HERE ----------
        # * find mask bolo
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = data_bolo

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskBolo = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # * find contours in the mask bolo
        # (x, y) center of the bolo
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # * jika countour ditemukan
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # * EUCLIDEAN BOLO
            boloX = center[0]
            boloY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((boloX, boloY))
            jarak_bolo = np.linalg.norm(a-b)
            print("jarak_bolo = " + str(int(jarak_bolo)))


            # * jika radius lebih dari X
            if radius > 1:
                is_bolo_found = True

                #menggambar lingkaran
                cv2.circle(image, (int(x), int(y)),
                          int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                   image, "Bolo", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                              10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            else:
                is_bolo_found = False

        #!---------- PROGRAM CAMERA BOLO ENDS HERE ----------
        #!---------- PROGRAM CAMERA GAWANG STARTS HERE ----------

        # * find mask gawang
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = data_gawang

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskGawang = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # * find contours in the mask gawang
        # (x, y) center of the gawang
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # * jika countour ditemukan
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            gawangX = center[0]
            gawangY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((gawangX, gawangY))
            jarak_gawang = np.linalg.norm(a-b)
            print("jarak_gawang = " + str(int(jarak_gawang)))

            # * jika radius lebih dari X
            if radius > 10:
                is_gawang_found = True

                # menggambar lingkaran
                cv2.circle(image, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                    image, "Gawang", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                               10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            else:
                is_gawang_found = False

        #!---------- PROGRAM CAMERA GAWANG ENDS HERE ----------

        #!---------- PROGRAM ROBOT STARTS HERE ----------

        is_ball_catch = getIR() is True

        # * jalankan STEP_ROBOT 0
        # serong ke kanan
        if STEP_ROBOT == 0:
            print('STEP_ROBOT = 0')
            # setMotor(-25, 85,-120)
            print("ROOOO : ",type(getRotateR()))        
            # breakpoint()
            if getRotateR()<= (lastR-4):
                remDelay(0.5)          
                STEP_ROBOT = 1
                before=time.time()
                saveLast()
            else:
                setMotor(-25, 85,-120)        
        # maju ke bola sampek jarak X
        elif STEP_ROBOT == 1:

            print('STEP_ROBOT = 1')
            move_left, move_right = pid(ballX, centerX, last_error)
            if is_ball_found:
                if gakenek(10):
                    print('gakenek')
                    setMotor(move_left/1.3, move_right/1.3)
                    miss=True
                else:
                    if jarak_ball > 85:
                        setMotor(move_left/1.3, move_right/1.3)
                    else:
                        pasne(ballX,centerBallX,5,13)
            if is_ball_catch:
                rem()
                if miss:
                    STEP_ROBOT = 2
                    before=time.time()
                 
                else:
                    STEP_ROBOT = 1.5
                    miss=False              
                    time.sleep(2)
        elif STEP_ROBOT==1.5:
            # if is_gawang_found:
                # if pasTengah(gawangX,gawangDummy2,3):
                    # remDelay(1.5)
            setMotor(20,-20,-20)
            if pasKompas(212,4):
                setMotor(50,50,0)
                time.sleep(1.85)
                STEP_ROBOT=2
                remDelay(2)
                before=time.time()
            #     else:
            #         print("PASNE")
            #         pasne(gawangX,gawangDummy2,3,15)
            # else:
            #     rem()
            #     is_gawang_found=False
            #     setMotor(15,15,0)

        elif STEP_ROBOT == 2:
            now=time.time()
            if is_bolo_found:
                if now-before>=3:
                    if pasTengah(boloX,centerBoloO,5):
                        rem()
                        tendang(1)
                        STEP_ROBOT = 3
                    else:
                        pasne(boloX,centerBoloO,5,13)
                else:
                    pasne(boloX,centerBoloO,5,13)
            else :
                setMotor(15,-15,-15)

        elif STEP_ROBOT == 3:
            # if is_gawang_found:
                # if pasTengah(gawangX,centerPasGawang,3):      
            setMotor(-20,20,20)
            if pasKompas(217,3):
                rem()
                    # time.sleep(1.5)
                    # remDelay(2)
                STEP_ROBOT = 3.5
                saveLast()
            # else:
            #     pasne(gawangX,centerPasGawang,3,15)
        elif STEP_ROBOT == 3.5:
            setMotor(25,-80,120)
            if getRotateR()>=lastR+3:
                rem()
                STEP_ROBOT=4
                before=time.time()
                saveLast()

        elif STEP_ROBOT == 4:
            move_left, move_right = pid(ballX, centerX, last_error)
            if is_ball_found:
                if gakenek(7):
                    setMotor(move_left/1.5,move_right/1.5)
                else:
                    if pasTengah(ballX,centerBallX,5):
                        rem()
                # elif jarak_ball > 50:
                #     setMotor(move_left, move_right)
                    else:
                        pasne(ballX,centerBallX,5,15)
            if is_ball_catch:
                STEP_ROBOT = 4.5

        elif STEP_ROBOT == 4.5:
            setMotor(20,-20,-20)
            if pasKompas(206,4):
                rem()
                STEP_ROBOT=5
                saveLast()

        elif STEP_ROBOT == 5:
            setMotor(30,-80,130)
            if getRotateR()>=lastR+2:
                rem()
                STEP_ROBOT=6
            
        elif STEP_ROBOT == 6:    
            if is_gawang_found:
                if pasTengah(gawangX,gawangTendang2,5):
                    rem()
                    tendang(0)
                    STEP_ROBOT = 99
                else:
                    pasne(gawangX,gawangTendang2,5,14)
            else:
                setMotor(20,-20,-20)

        elif STEP_ROBOT==99:
            stop()
            saveLast()       
            
        #!---------- PROGRAM ROBOT ENDS HERE ----------

        # * show the frame to our screen
        cv2.imshow(statusauto, image)
        # cv2.imshow("Mask Bolo", maskBolo)
        # cv2.imshow("Mask Ball", maskBall)
        # ? Ketika Tombol ditekan
        # esc untuk nutup program
    
        refreshServer()

        key = cv2.waitKey(1)
        if key == 27:
            break
                                       
def otomatis2():
    print('UNIT Test : otomatis2')
    global STEP_ROBOT,play,now,before,miss,lastL,lastR
    saveLast()
    # * Variable Init
    is_ball_found = False
    is_gawang_found = False
    is_bolo_found = False
    ballX = 0
    ballY = 0
    pas=0
    boloX=0
    centerBoloOper1=332 #oper awal
    centerNerimoOper1=311
    centerBoloOper2=327 #oper ape nge golne
    
    # STEP_ROBOT=3.5
    # before=time.time()
    while play:
        camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        ret, image = camera.read()
        image = cv2.flip(image, 1)

        if not ret:
            break

        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        kernel = np.ones((5, 5), np.uint8)

        #!---------- PROGRAM CAMERA BALL STARTS HERE ----------

        # * find mask gawang
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = data_ball2

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskBall = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # * find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            ballX = center[0]
            ballY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((ballX, ballY))
            jarak_ball = np.linalg.norm(a-b)
            jarak_ball = int(jarak_ball)
            print("jarak_ball = " + str(jarak_ball))

            if radius > 3:
                is_ball_found = True
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                    image, "Ball", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                               10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            else:
                is_ball_found = False

        #!---------- PROGRAM CAMERA BALL ENDS HERE ----------

        #!---------- PROGRAM CAMERA BOLO STARTS HERE ----------
        # * find mask bolo
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = data_bolo2

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskBolo = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # * find contours in the mask bolo
        # (x, y) center of the bolo
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # * jika countour ditemukan
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # * EUCLIDEAN BOLO
            boloX = center[0]
            boloY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((boloX, boloY))
            jarak_bolo = np.linalg.norm(a-b)
            print("jarak_bolo = " + str(int(jarak_bolo)))


            # * jika radius lebih dari X
            if radius > 1:
                is_bolo_found = True

                #menggambar lingkaran
                cv2.circle(image, (int(x), int(y)),
                          int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                   image, "Bolo", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                              10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            else:
                is_bolo_found = False

        #!---------- PROGRAM CAMERA BOLO ENDS HERE ----------
        #!---------- PROGRAM CAMERA GAWANG STARTS HERE ----------

        # * find mask gawang
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = data_gawang2

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskGawang = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # * find contours in the mask gawang
        # (x, y) center of the gawang
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # * jika countour ditemukan
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            gawangX = center[0]
            gawangY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((gawangX, gawangY))
            jarak_gawang = np.linalg.norm(a-b)
            print("jarak_gawang = " + str(int(jarak_gawang)))

            # * jika radius lebih dari X
            if radius > 15:
                is_gawang_found = True

                # menggambar lingkaran
                cv2.circle(image, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                    image, "Gawang", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                               10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            else:
                is_gawang_found = False

        #!---------- PROGRAM CAMERA GAWANG ENDS HERE ----------

        #!---------- PROGRAM ROBOT STARTS HERE ----------
        is_ball_catch = getIR() is True

        # * jalankan STEP_ROBOT 0        
        if STEP_ROBOT == 0:#SERONG KIRI
            print('STEP_ROBOT = 0')
            # setMotor(-25, 85,-120)
            print("ROOOO : ",type(getRotateR()))        
            # breakpoint()
            if getRotateR()<= (lastR-5):
                remDelay(0.3)          
                STEP_ROBOT = 1
                before=time.time()
                saveLast()
            else:
                setMotor(-25, 85,-120)      
        elif STEP_ROBOT == 1:#NGUBER BALL
            print('STEP_ROBOT = 1')
            move_left, move_right = pid(ballX, centerX, last_error)
            if is_ball_found:
                setMotor(move_left, move_right)
                """if jarak_ball > 110:
                    setMotor(move_left, move_right)
                else:
                    setMotor(move_left/1.2,move_right/1.2)"""
            else:
                stop()
            
            if is_ball_catch:
                rem()
                STEP_ROBOT = 2
                before=time.time()                
        elif STEP_ROBOT == 2:#OPER BOLO
            print('STEP_ROBOT = 2')
            now=time.time()
            if is_bolo_found:
                if now-before>=2.5:
                    if pasTengah(boloX,centerBoloOper1,2):
                        rem()
                        time.sleep(0.5)
                        tendang()
                        STEP_ROBOT = 3
                        #SERONGKANAN
                        remDelay(0.2)
                        setMotor(25,-80,110)
                        time.sleep(1.4)
                        remDelay(1)
                        #MUTERKIRI
                        setMotor(-20,20,20)
                        time.sleep(0.7)
                        remDelay(0.5)
                        before=time.time()
                    else:
                        pasne(boloX,centerBoloOper1,4,13)
            else :
                pasne(boloX,centerBoloX,4,13)

        elif STEP_ROBOT == 3:#NGENTENI OPER
            print('STEP_ROBOT = 3')
            left,right =pid(ballX,centerX,last_error)
            if gakenek(8):
                setMotor(left/1.5,right/1.5)
            else:
                pasne(ballX,centerNerimoOper1,5,14)
            if is_ball_catch:
                rem()
                STEP_ROBOT = 3.5
                before=time.time()
        elif STEP_ROBOT == 3.5:#NGOPER
            now=time.time()
            if is_bolo_found:
                if now-before>=8:
                    if pasTengah(boloX,centerBoloOper2,5):
                        rem()
                        tendang()
                        STEP_ROBOT=99
                        setMotor(25,-70,110)
                        time.sleep(1.2)
                        rem()
                    else:
                        pasne(boloX,centerBoloOper2,5,14)
                else:
                    pasne(boloX,centerBoloOper2,5,14)
        elif STEP_ROBOT == 99:
            print('STEP_ROBOT = 99')
            stop()   
            saveLast()
        #!---------- PROGRAM ROBOT ENDS HERE ----------

        # * show the frame to our screen
        cv2.imshow(statusauto, image)
        #cv2.imshow("Mask Bolo", maskBolo)
        #cv2.imshow("Mask Ball", maskBall)
        # ? Ketika Tombol ditekan
        # esc untuk nutup program
        
        refreshServer()

        key = cv2.waitKey(1)
        if key == 27:
            break
    checkNewMessageAutoAgain()

def otomatis3():
    print('UNIT Test : otomatis3')
    global STEP_ROBOT,play,now,before,miss
    # * Variable Init
    is_ball_found = False
    is_gawang_found = False
    is_bolo_found = False
    ballX = 0
    ballY = 0
    pas=0
    boloX=0
    posTendang=380
    operCorner=323
    tendangGol=323
    lurusneBall=220
    centerOperBolo1=338 #oper awa
    centerBalikOper=315
       
    while play:
        camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        ret, image = camera.read()
        image = cv2.flip(image, 1)

        if not ret:
            break

        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        kernel = np.ones((5, 5), np.uint8)

        #!---------- PROGRAM CAMERA BALL STARTS HERE ----------

        # * find mask gawang
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = data_ball

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskBall = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # * find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            ballX = center[0]
            ballY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((ballX, ballY))
            jarak_ball = np.linalg.norm(a-b)
            jarak_ball = int(jarak_ball)
            print("jarak_ball = " + str(jarak_ball))

            if radius > 3:
                is_ball_found = True
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                    image, "Ball", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                               10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            else:
                is_ball_found = False

        #!---------- PROGRAM CAMERA BALL ENDS HERE ----------

        #!---------- PROGRAM CAMERA BOLO STARTS HERE ----------
        # * find mask bolo
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = data_bolo

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskBolo = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # * find contours in the mask bolo
        # (x, y) center of the bolo
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # * jika countour ditemukan
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # * EUCLIDEAN BOLO
            boloX = center[0]
            boloY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((boloX, boloY))
            jarak_bolo = np.linalg.norm(a-b)
            print("jarak_bolo = " + str(int(jarak_bolo)))


            # * jika radius lebih dari X
            if radius > 1:
                is_bolo_found = True

                #menggambar lingkaran
                cv2.circle(image, (int(x), int(y)),
                          int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                   image, "Bolo", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                              10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            else:
                is_bolo_found = False

        #!---------- PROGRAM CAMERA BOLO ENDS HERE ----------
        #!---------- PROGRAM CAMERA GAWANG STARTS HERE ----------

        # * find mask gawang
        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max, focus = data_gawang

        thresh = cv2.inRange(
            frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        maskGawang = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # * find contours in the mask gawang
        # (x, y) center of the gawang
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # * jika countour ditemukan
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            gawangX = center[0]
            gawangY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((gawangX, gawangY))
            jarak_gawang = np.linalg.norm(a-b)
            print("jarak_gawang = " + str(int(jarak_gawang)))

            # * jika radius lebih dari X
            if radius > 7:
                is_gawang_found = True

                # menggambar lingkaran
                cv2.circle(image, (int(x), int(y)),
                           int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(
                    image, "Gawang", (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                cv2.putText(image, "("+str(center[0])+","+str(center[1])+")", (center[0] +
                                                                               10, center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            else:
                is_gawang_found = False

        #!---------- PROGRAM CAMERA GAWANG ENDS HERE ----------

        #!---------- PROGRAM ROBOT STARTS HERE ----------

        turn_speed = 120
        move_speed = 120
        slow_mode = 30
        is_ball_catch = getIR() is True

        # * jalankan STEP_ROBOT 0        
        if STEP_ROBOT == 0:#
            print('STEP_ROBOT = 0')
            left,right=pid(ballX,centerX,last_error)
            if is_ball_found:
                setMotor(left/1.5,right/1.5)
            if is_ball_catch:
                rem()
                STEP_ROBOT = 1
                before=time.time()

        elif STEP_ROBOT == 1:#
            now=time.time()
            print('STEP_ROBOT = 1')
            if now-before>=3:
                if is_bolo_found:
                    if pasTengah(boloX,centerOperBolo1,4):
                        remDelay(1)
                        tendang()
                        STEP_ROBOT = 2
                    else:
                        pasne(boloX,centerOperBolo1,4,14)
                else:
                    rem()
            else:
                pasne(boloX,centerOperBolo1,4,14)

        elif STEP_ROBOT == 2:#
            print('STEP_ROBOT = 2')
            setMotor(-25,80,-110)
            time.sleep(1.2)
            remDelay(0.5)
            STEP_ROBOT=2.5
            
        
        elif STEP_ROBOT==2.5:
            setMotor(30,40,0)
            time.sleep(1.3)
            rem()
            STEP_ROBOT=3
            before=time.time()

        elif STEP_ROBOT == 3:#nuggu oper
            now=time.time()
            print('STEP_ROBOT = 3')
            if is_ball_found:
                if now-before>=2:
                    if pasTengah(ballX,operCorner,4):
                        rem()
                    else:
                        pasne(ballX,operCorner,4,14)
            if is_ball_catch:
                rem()
                setMotor()
                STEP_ROBOT=4

        elif STEP_ROBOT==4: #aBalik oper, kabur
            now=time.time()
            print('STEP_ROBOT = 4')
            if is_gawang_found:
                setMotor(-15,15,15)
                if gawangX<230:
                    remDelay(1)
                    setMotor(-25,70,-100)
                    time.sleep(1.7)
                    remDelay(1)
                    setMotor(50,70,0)
                    time.sleep(1.5)
                    rem()
                    STEP_ROBOT=5
                    before=time.time()

        elif STEP_ROBOT==5:
            now=time.time()
            if is_gawang_found:
                if now-before>=3:
                    if pasTengah(gawangX,tendangGol,5):
                        rem()
                        tendang()
                        STEP_ROBOT=99
                    else:
                        pasne(gawangX,tendangGol,5,15)
            else:
                pasne(gawangX,tendangGol,5,15)

        elif STEP_ROBOT == 99:
            print('STEP_ROBOT = 99')
            stop()
                            
        #!---------- PROGRAM ROBOT ENDS HERE ----------

        # * show the frame to our screen
        cv2.imshow(statusauto, image)
        #cv2.imshow("Mask Bolo", maskBolo)
        #cv2.imshow("Mask Ball", maskBall)
        # ? Ketika Tombol ditekan
        # esc untuk nutup program
        
        refreshServer()

        key = cv2.waitKey(1)
        if key == 27:
            break

while True:
    # global play
    try:
        terima=client.recv(SIZE).decode(ENCODING)
        if terima:
            #MAIN Block
            if terima.startswith('auto'):           
                # global statusauto
                play=True
                statusauto=terima
                jumpAnotherAuto=True
                while(jumpAnotherAuto):
                    checkNewMessageAutoAgain()
                    terima=statusauto
                    print(' - ' ,statusauto)             

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