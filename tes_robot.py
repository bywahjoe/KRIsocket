import time
from configku import *
from mainarduino import *

print("MTR DRIBLE TEST")
drible(255)
time.sleep(5)
drible(0)
time.sleep(5)

print("MTR KIRI TEST")
kiri(255)
time.sleep(5)
kiri(0)
time.sleep(5)   
kiri(-255)
time.sleep(5)        

print("MTR KANAN TEST")
kanan(255)
time.sleep(5)
kanan(0)
time.sleep(5)   
kanan(-255)
time.sleep(5)

print("MTR BELAKANG TEST")
belakang(255)
time.sleep(5)
belakang(0)
time.sleep(5)   
belakang(-255)
time.sleep(5)  

print("MUTER")
setMotor(-100,100,100) #KIRI
time.sleep(5)  
setMotor(100,-100,-100)#KANAN
time.sleep(5)  
setMotor(0,0,0)

print("IR STATUS: ",getIR())