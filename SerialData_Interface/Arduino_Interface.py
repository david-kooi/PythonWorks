import pyfirmata
from pyfirmata import mockup, Arduino
from pyfirmata.boards import BOARDS
import binascii
import logging

class Arduino_Interface(object):


	PING = 0x01
	GET_DATA = 0x02


	def __init__(self, port):
		## Initalize logging
		logging.basicConfig(level=logging.DEBUG)

		self.logger = logging.getLogger('Arduino_Interface')
		self.logger.debug('__init__')


		## Board Initalization
		self.board = Arduino(port)
		self.board.add_cmd_handler(pyfirmata.START_SYSEX, self.handleIncomingSysEx)
		self.board.add_cmd_handler(pyfirmata.STRING_DATA, self.handleIncomingString)

		## Data Buffer Initalization
		self.incoming_data = []

		## Callback holder
		self.callback_holder = dict()

	def ping(self, pingCallback):
		self.logger.debug('----Sending Ping----')
		## Attach callback
		self.callback_holder[Arduino_Interface.PING] = pingCallback


		byte_array = bytearray()
		byte_array.append(Arduino_Interface.PING)


		self.sendSysEx(byte_array)

		self.begin_scanning()

	def sendSysEx(self, byteArray):
		self.logger.debug('----sendSysEx----')
		self.logger.debug('Data: {}'.format(binascii.hexlify(byteArray)))
		self.board.send_sysex(pyfirmata.START_SYSEX, byteArray)

	def sendString(self, stringToSend):
		pass
		#self.board.send_sysex

	def handleIncomingSysEx(self, *byteArray):
		self.logger.debug('----Incoming SysEx----')

		## Flush incoming_data array
		self.incoming_data = []


		for byte in byteArray:
			self.incoming_data.append(byte)
		print self.incoming_data

		## Get header
		header = byteArray[0]
		self.logger.debug('header: {}'.format(header))
		

		if (header == Arduino_Interface.PING) :
			self.logger.debug('PING Response recieved')
			## Ping response recieved. Return True
			self.callback_holder[Arduino_Interface.PING](True)

		elif (header == Arduino_Interface.PING):
			pass




	#	for byte in dataArray:
	#		self.incoming_data.append(chr(byte))
	#	print self.incoming_data

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

class X(object):
	def __init__(self):
		self.ping = False
	def pingCallback(self, status):
		print "PING CALLBACK"
		self.ping = status


if __name__ == '__main__':
	print 'setting up'

	A_COM = Arduino_Interface('/dev/tty.usbmodemfd121')
	print "PING: {}".format(A_COM.PING)
	x  = X()

	#Data to send to arduino
	#byte_array = bytearray()
	#byte_array.extend([0x01, 0x0ff, 0x06, 0x01, 0x03])
	#print 'Byte String: '
	#print binascii.hexlify(byte_array)
	
	print 'sending data'
	## Send data
	A_COM.ping(x.pingCallback)

	## Recieve Data
	A_COM.begin_scanning()

	print "ping status: {}".format(x.ping)

