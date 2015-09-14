import serial


class Port_Com(object):

    

    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud)


    def requestData(requestCode):
    	self.ser.write(requestCode)
    	response = self.ser.read()

    	

if __name__ == '__main__':

    port = '/dev/tty.usbserial'
    baud = 9600
    stop = False

    pCom = Port_Com(port, baud)

    while stop not False:
        stop = pCom.get_stop_bit()
