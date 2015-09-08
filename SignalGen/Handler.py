import time 
import subprocess
from subprocess import *
import sys
import os
from Tkinter import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib

class SignalGen(object):

    def startSignal(SourceFile):
         cmd = 'python {source} {args}'.format(source=SourceFile, args='')
         signalSource = subprocess.Popen(cmd, stdout=PIPE, shell=True)
         print 'SignalSource started'
        
         __processSignal(signalSource)


    def __processSignal(signalSource):
        print 'Processing Signal'

        while True:
            data = signalSource.stdout.readline()
            if not data: break

            print data    
            

    def startGUI():

        root = Tk()
        root.geometry('400x400')
        
        frame = Frame(root)
        frame.pack()

        dataLabel = Label(frame, text='test')
        dataLabel.pack()

        root.mainloop()



if __name__ == '__main__':
    # Change to current directory and start generating signal
    os.chdir(os.getcwd())
    
    


