import pyfirmata
from pyfirmata import mockup, Arduino
from pyfirmata.boards import BOARDS
import binascii
import logging

class Arduino_Interface(object):

	def __init__(self, port):
		## Initalize logging
		self.logger = logging.getLogger('Arduino_Interface')
		self.logger.debug('__init__')


		## Board Initalization
		self.board = Arduino(port)
		self.board.add_cmd_handler(pyfirmata.START_SYSEX, self.handleIncomingSysEx)
		self.board.add_cmd_handler(pyfirmata.STRING_DATA, self.handleIncomingString)

		## Data Buffer Initalization
		self.incoming_data = []

	def sendSysEx(self, byteArray):
		self.logger.debug('sendSysEx')

		self.board.send_sysex(pyfirmata.START_SYSEX, byteArray)

	def sendString(self, stringToSend):
		pass
		#self.board.send_sysex

	def handleIncomingSysEx(self, *dataArray):
		self.logger.debug('handling Incoming SysEx')

		## Flush incoming_data array
		self.incoming_data = []

		for byte in dataArray:
			self.incoming_data.append(chr(byte))
		print self.incoming_data

	def handleIncomingString(self, *string):
		self.logger.debug('handling Incoming String')

		## Flush incoming_data
		self.incoming_data = []

		for byte in string:
			self.incoming_data.append(chr(byte))

		recieved_string = ''.join(self.incoming_data)
		print recieved_string

	def begin_scanning(self):
		self.board.iterate()
	
if __name__ == '__main__':
	print 'setting up'

	A_COM = Arduino_Interface('/dev/tty.usbmodemfd121')

	#Data to send to arduino
	byte_array = bytearray()
	byte_array.extend([0x01, 0x0ff, 0x06, 0x01, 0x03])
	print 'Byte String: '
	print binascii.hexlify(byte_array)
	print 'sending data'

	## Send data
	A_COM.sendSysEx(byte_array)

	## Recieve Data
	A_COM.begin_scanning()

