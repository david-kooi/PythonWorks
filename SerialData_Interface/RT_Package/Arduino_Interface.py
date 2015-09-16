import serial
import logging
import time
from Config import Config


class Port_Com(object):

    

    def __init__(self, port, baud, cmd_listID):
        """
            port: Serial Port Name
            baud: Bits/second
            cmd_listID: What command list to use within Config
        """
        ## Get Logger
        self.logger = logging.getLogger('Port_Com')
        self.logger.debug('__init__')

        ## Serial Port
        self.ser = serial.Serial(port, baud)
        self.ser.flushInput()
        self.ser.flushOutput()

        ## Configuration
        c = Config.Config()
        cmd_list = c.getCommandList(cmd_listID)
        
        ## Commands
        self.PING = cmd_list['ping']
        self.START_COLLECTION = cmd_list['start_collection']
        self.GET_DATA_POINT = cmd_list['get_data_point']

    def commandHandler(self, requestCode):
        self.logger.debug('commandHandler')

    	self.ser.write(requestCode)
        while (self.ser.inWaiting() == 0):
            pass
            #print 'Waiting...'

    	response = self.ser.read(1)
        print response
        return response
            	

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('Arduino_Interface')

    port = "/dev/cu.usbmodemfa131"
    baud = 9600
    stop = False

    pCom = Port_Com(port, baud, 'A')

    while True:

        pCom.requestData('1')
        pCom.requestData('2')
