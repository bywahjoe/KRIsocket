import time
import pyfirmata
from pyfirmata import ArduinoMega,util


board = ArduinoMega('COM3')
it=util.Iterator(board)
it.start()
#board = pyfirmata.Arduino('COM3')
IRREAD=board.get_pin('d:43:i')
#IRREAD.enable

def getIR():
	if IRREAD.read():
		return False
	else:
		return True
while True:
	print(IRREAD.read())