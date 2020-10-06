import socket
import time
import os
import threading
import multiprocessing
from configku import *
from mainarduino import *

# ADD
import cv2
import argparse
import numpy as np
import pickle

MODE_ROBOT = 1

PIDX = 0
print('CLIENT VIEW **,CMD PID:', os.getpid())
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"    Computer Name	   : {hostname}")
print(f"    IP Address   	   : {ip_address}")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((JARINGAN))
# client.settimeout(0.1)
client.setblocking(0)
pesan = '1st check'


def testThreadMotor(delay, kiri, kanan, belakang=0):
    myThread = threading.Thread(target=ex_manual, args=(
        delay, kiri, kanan, belakang), daemon=True)
    myThread.start()


def kirim(isi_pesan):
    isi_pesan = str(isi_pesan)
    client.send(isi_pesan.encode(ENCODING))


def get_manual(mypesan):
    paramku = []
    seplit = mypesan.split(',')
    # print(seplit)
    # 0  1     2     3	4
    # M,DELAY,KIRI,KANAN,BELAKANG
    paramku.append(int(seplit[1]))
    paramku.append(int(seplit[2]))
    paramku.append(int(seplit[3]))
    paramku.append(int(seplit[4]))
    #
    delay = paramku[0]
    kiri = paramku[1]
    kanan = paramku[2]
    blkg = paramku[3]

    print(kiri, kanan, blkg, delay)
    ex_manual(delay, kiri, kanan, blkg)
    """
	setMotor(kiri,kanan)
	time.sleep(delay)
	setMotor(0,0,0)"""


def ex_manual(delay, kiri, kanan, belakang=0):
    setMotor(kiri, kanan, belakang)
    time.sleep(delay)
    stop()


def runArduinoCompass():

    # excecute='python serialkompas.py'
    # runCMD=subprocess.Popen(['python','serialkompas.py'], shell=True)

    os.system('start /wait cmd /k python serialkompas.py')
    PIDX = os.getpid()
    print(PIDX)


"""threadx = threading.Thread(target=runArduinoCompass,daemon=True)
threadx.start()"""


def forward():
    kirim('LETSGO')


def otomatis():
    print('startwhile')

    data_ball = pickle.load(open("data_ball.dat", "rb"))
    data_gawang = pickle.load(open("data_gawang.dat", "rb"))
    data_bolo = pickle.load(open("data_bolo.dat", "rb"))

    # change camera setup here
    camera = cv2.VideoCapture(1)
    camera.set(28, 75)

    # * Variable Init
    centerX = 319
    centerY = 239
    is_ball_found = False
    is_gawang_found = False
    last_ball_posX = 0
    ballX = 0
    ballY = 0

    STEP_ROBOT = 0

    while True:
        ret, image = camera.read()
        image = cv2.flip(image, 1)

        if not ret:
            break

        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        kernel = np.ones((5, 5), np.uint8)

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

            # * EUCLIDEAN GAWANG
            gawangX = center[0]
            gawangY = center[1]

            a = np.array((centerX, centerY))
            b = np.array((gawangX, gawangY))
            jarak_gawang = np.linalg.norm(a-b)
            print("jarak_gawang = " + str(int(jarak_gawang)))

            # * jika radius lebih dari X
            if radius > 2:
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
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
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

            # only proceed if the radius meets a minimum size
            # print("radius :", radius)
            if radius > 2:
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

                # menggambar lingkaran
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

        #!---------- PROGRAM ROBOT STARTS HERE ----------

        turn_speed = 150
        move_speed = 200
        slow_mode = 30
        is_ball_catch = getIR() is True

        # * jalankan STEP_ROBOT 0
        # serong ke kiri
        if STEP_ROBOT == 0:
            print('STEP_ROBOT = 0')

            t_end = time.time() + 2.4
            while time.time() < t_end:
                setMotor(0, -100, 160)

            setMotor()
            # break
            STEP_ROBOT = 1

        # * jalankan STEP_ROBOT 1
        # ngejar bola trus madep bolo dan umpan
        if STEP_ROBOT == 1:
            print('STEP_ROBOT = 1')

            # ngejar bola
            if is_ball_found and not is_ball_catch:
                print('is_ball_found and not is_ball_catch')

                if (ballX > 300 and ballX < 330):
                    # lek wes oleh bal mandek
                    if ballY >= 150 and ballY < 155:
                        setMotor()
                    else:
                        setMotor(move_speed / 2, move_speed / 2)

                # belok kiri
                if ballX < 300:
                    # fastmode
                    if(ballX < 300 - slow_mode):
                        setMotor(0, turn_speed, 20)
                    else:
                        setMotor(0, 70, 20)
                # belok kanan
                elif ballX > 330:
                    # fastmode
                    if(ballX > 330 + slow_mode):
                        setMotor(turn_speed, 0, -20)
                    else:
                        setMotor(70, 0, -20)

            elif is_ball_catch:
                # * madep bolo'
                if (boloX > 300 and boloX < 330):
                    # lek wes madep bolo tendang
                    setMotor()
                    time.sleep(0.5)
                    tendang(1)
                    STEP_ROBOT = 2

                # belok kiri
                elif boloX < 300:
                    setMotor(0, 0, 70)
                # belok kanan
                elif boloX > 330:
                    setMotor(0, 0, -70)

        # * jalankan STEP_ROBOT 2
        #  serong kiri saitik ke gawang
        elif STEP_ROBOT == 2:
            print('STEP_ROBOT = 2')

            t_end = time.time() + 2
            while time.time() < t_end:
                setMotor(-120, 0, -160)

            setMotor()

            STEP_ROBOT = 3

        # * jalankan STEP_ROBOT 3
        # madep bola
        elif STEP_ROBOT == 3:
            print('STEP_ROBOT = 3')

            if is_ball_found:
                # * madep ball
                if (ballX > 300 and ballX < 330):
                    # ngirim ping
                    print('kirim ping')
                    setMotor()
                    # time.sleep(1)
                    # kirim('UMPANTENDANG')
                    STEP_ROBOT = 4

                # belok kiri
                elif ballX < 300:
                    setMotor(0, 0, 70)
                # belok kanan
                elif ballX > 330:
                    setMotor(0, 0, -70)

            else:
                setMotor()

        # * jalankan STEP_ROBOT 4
        #  ngejar bola lek cedek
        elif STEP_ROBOT == 4:
            print('STEP_ROBOT = 4')

            is_ball_close = jarak_ball < 130

            if is_ball_found and is_ball_catch is False:
                print('STEP_ROBOT = 4 is_ball_found and is_ball_catch is False')

                if ballX > 300 and ballX < 330:
                    # lek wes oleh bal mandek
                    if is_ball_close:
                        setMotor(move_speed / 2, move_speed / 2)
                    else:
                        setMotor()

                elif ballX < 300:
                    setMotor(0, 70, 20)
                    # belok kanan
                elif ballX > 330:
                    setMotor(70, 0, -20)
            elif is_ball_catch:
                setMotor()
                STEP_ROBOT = 5
            else:
                setMotor()

        # * Jalankan STEP_ROBOT 5
        # tendang bola ke gawang
        elif STEP_ROBOT == 5:
            print('STEP_ROBOT = 5')

            if is_ball_catch and is_gawang_found:
                if (gawangX > 300 and gawangX < 330):
                    print("tendang")
                    tendang()
                    stop()

                    #! TERMINATION
                    # break

                elif gawangX > 330:
                    print("menggok kanan")
                    setMotor(0, 0, -70)
                elif gawangX < 300:
                    print("menggok kiri")
                    setMotor(0, 0, 70)
                else:
                    setMotor(0, 0)

                    print("logic error")
                    print("Kompas = ", getKompas())
            else:
                setMotor()

        #!---------- PROGRAM ROBOT ENDS HERE ----------

        # * show the frame to our screen
        cv2.imshow("Original", image)
        cv2.imshow("Mask Bolo", maskBolo)
        cv2.imshow("Mask Gawang", maskGawang)
        cv2.imshow("Mask Ball", maskBall)

        # ? Ketika Tombol ditekan
        # esc untuk nutup program
        key = cv2.waitKey(1)
        if key == 27:
            break

        try:
            new_message = client.recv(SIZE).decode(ENCODING)
            if new_message:
                if new_message == 'auto':
                    # ResetStep
                    kirim('P:REAUTO')
                    # CODE
                elif new_message == 'retry':
                    # AllMotorStop
                    kirim('P:RETRYCV')
                    # CODE
                elif new_message == 'LETSMOVE':
                    # HANDLE KONDISI SAAT FORWADING
                    print('HANDLE')
                else:
                    # DESTROYCV
                    return new_message
        except BlockingIOError:
            pass

        print('stopwhile')


while True:

    try:
        terima = client.recv(SIZE).decode(ENCODING)
        if terima:
            if terima == 'auto':
                terima = otomatis()
            if terima.startswith('MNL'):
                terima = terima.upper()
                print(terima)
                get_manual(terima)
            elif terima == 'wahyu':
                kirim('Masuk')
            elif terima == 'testmotor':
                ex_manual(3, 150, 150, 150)
                ex_manual(3, -150, -150, -150)
            elif terima == 'stops':
                # oeee=''
                stop()
            elif terima == 'getir':
                kirim(getAllMyIR())
            elif terima == 'selenoid':
                tendang()
            elif terima == 'statusumpan':
                forward()
            elif terima == 'kompas':
                kirim(getKompas())
                print(getKompas())
            else:
                print(f"S| {terima} ")
    except BlockingIOError:
        pass
    except ConnectionResetError:
        os.system('taskkill /IM "python.exe" /F')
    except Exception as e:
        print(e)
        pass
