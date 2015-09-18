import serial
import logging
import time
from Config import Config

class Com_Port(object):

    

    def __init__(self, port, baud):
        """
            port: Serial Port Name
            baud: Bits/second
            cmd_listID: What command list to use within Config
        """
        ## Get Logger
        self.logger = logging.getLogger('Com_Port')
        self.logger.debug('__init__')

        ## Serial Port
        self.ser = serial.Serial(port, baud)
        ## Get status
        self.logger.debug('Slave Status: {}'.format(self.ser.read(1)))
        self.ser.flush()

    def commandDispatch(self, opCode):
        self.logger.debug('commandDispatch')
        self.logger.debug('opCode: {}'.format(opCode))
       # self.logger.debug('opCode char: {}'.format(chr(opCode)))

        ## opCode must be written as a char
    	#self.ser.write(chr(opCode))
        bytes = self.ser.write(chr(opCode))
        self.logger.debug('Num bytes sent: {}'.format(bytes))
       # while (self.ser.inWaiting() == 0):
       #     pass

    	response = self.ser.read(2)
        self.logger.debug('Slave Response: {}'.format(response))
        return hex(int(response))
         


class Arduino_Port(Com_Port):

    def __init__(self, port, baud, cmd_listID):
        self.logger = logging.getLogger('Arduino_Port')
        self.logger.debug('__init__')

        Com_Port.__init__(self, port, baud)

         ## Configuration
        c = Config()
        cmd_list = c.getCommandList(cmd_listID)
        
        ## Commands
        self.PING = cmd_list['ping']
        self.START_COLLECTION = cmd_list['start_collection']
        self.GET_DATA_POINT = cmd_list['get_data_point']


        ## Let Arduino initalize
        self.logger.info("Allowing arduino to initalize...")
        time.sleep(3)

    def ping(self):
        self.logger.debug('ping request sent')
        response = self.commandDispatch(self.PING)

        self.logger.debug('response: {}'.format(response))
        self.logger.debug('opCode: {}'.format(self.PING))
        if response == hex(self.PING):
            return True
        else:
            return False

    def getDataPoint(self):
        self.logger.debug('getDataPoint request sent')
        response = self.commandDispatch(self.GET_DATA_POINT)   	

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('Arduino_Interface')

    port = "/dev/tty.usbmodemfa131"
    baud = 9600


    com = serial.Serial(port, baud)
    print "Status: {}".format(com.read(1))


    logger.debug('Allowing Arduino to connect...')
    time.sleep(2)

    com.write(chr(0x01))
    response = com.read(2)
    logger.debug('response: {}'.format(response))
    #pCom = Com_Port(port, baud)

    #pCom.commandDispatch(1)
