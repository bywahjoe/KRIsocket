import pyfirmata
from ardupin import*
board = pyfirmata.ArduinoMega(COM_PORT)
#board = pyfirmata.Arduino('COM3')
it=pyfirmata.util.Iterator(board)
it.start()
IR_READ=board.get_pin('d:3:i')
while True:
	print(IR_READ.read())
	