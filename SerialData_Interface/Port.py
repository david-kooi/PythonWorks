import serial

class Serial_Port(object):
    def __init__(self, port, baud):
        self.port = serial.Serial(port, baud)

    def sendCmd(self):
        print "sending cmd"
        self.port.write('1')

        response = self.port.read(1)

        print response

if __name__ == "__main__":

    port = "/dev/tty.usbmodemfd121"
    baud = 9600
    print "Creating"
    s = serial.Serial(port, baud)
    s.write('1')
    s.readline()
