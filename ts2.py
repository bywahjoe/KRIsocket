import pyfirmata
import time
import datetime
from ardupin import*
board = pyfirmata.Arduino('COM4')
pin=board.get_pin('d:13:o')
#board = pyfirmata.Arduino('COM3')
it=pyfirmata.util.Iterator(board)
it.start()
while True:
	print ('ok')
	pin.write(0)
	makefile=open('datacompas.txt','w')
	now=datetime.datetime.now()
	waktu=str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'-'
	makefile.write(waktu+' '+'y')
	time.sleep(2);
	pin.write(1)
	time.sleep(2);
	