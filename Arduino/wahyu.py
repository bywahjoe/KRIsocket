from struct import *
import serial
import threading

ser = serial.Serial('COM3', baudrate=9600)

# ok=b'\x05\x00\x00\x00\x07\x00\x00\x00'
# print(unpack('ii',ok))

myKompas,rotateL,rotateR,pulseL,pulseR=0,0,0,0,0
def readSerial():
    global myKompas,rotateL,rotateR,pulseL,pulseR
    while True:
        recv=ser.read(20)
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
x = threading.Thread(target=readSerial, daemon=True)
x.start()

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

