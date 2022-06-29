import threading
import time

thread1='1'
thread2='2'

def createThread(s):
    while True:
        print("running in thread-",s)
        time.sleep(1)

print("Process Start")
threadA = threading.Thread(target=createThread,args=(thread1))
threadA.start()

threadB = threading.Thread(target=createThread,args=(thread2))
threadB.start()

