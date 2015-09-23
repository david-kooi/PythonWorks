from RT_Plot import *
from Config import Config 
import Arduino_Interface
from Arduino_Interface import *

import Tkinter as tk
from Tkinter import *

import logging
from Tk_Logging import *

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import serial.tools.list_ports


class Tk_Interface(tk.Tk):

    ## Standard Timeout
    STD_TO = 15

    def __init__(self, config, *args, **kwargs):  
        self.logger = logging.getLogger('Tk_Interface')
        self.logger.debug('__init__')

        tk.Tk.__init__(self, *args, **kwargs)
           
        tk_config = config['tk_window'] 
        graph_config = config['graph']
        serial_config = config['serial_config']

        ## Runtime status
        self.status_reg = {}
        self.status_reg[Arduino_Interface.PING] = False # Are we connected?

        ## Input Buffers
        self.x_buffer = [20]
        self.y_buffer = [20]

        ## Initalize Window
        self.__tkInit(tk_config)
       
        ## Initalize Graph
        self.__graphInit(graph_config)
        
        ## Initalize Widgets
        widget_config = {} # Temporary config dict.
        self.__widgetInit(widget_config)

        ## Initalize Serial Configuration
        self.__serialConfigInit(serial_config)


        ## Setup is done. Add logging handlers
        self.logger.debug('Adding Handler')
        self.log_handler = Tk_Logging_Handler(level=logging.DEBUG, listbox=self.listbox)
        self.logger.addHandler(self.log_handler)


        ## Temp run
        #self.test_update()
    


    ##                                          ##
    ##             Utility Methods              ##
    ##                                          ##
    ##                                          ##

    def flushBuffers(self):
        self.x_buffer = []
        self.y_buffer = []


    def __getPorts(self):

        raw_ports = serial.tools.list_ports.comports()

        ports = []
        ## Parse raw_ports tuple
        for (name, x, y) in raw_ports:
            ports.append(name)

        return ports

    def __configureGrid(self, frame, max_rows, max_cols):
        for x in range(max_cols):
            Grid.columnconfigure(frame, x, weight=1)

        for y in range(max_rows):
            Grid.rowconfigure(frame, y, weight=1)
      


    def checkTimeout(self, time_limit):
        start_time = time.time()

        ## Timeout check
        while(self.status_reg['WAITING'] is True):
            end_time = time.time()
            if end_time-start_time == time_limit:
                raise RuntimeWarning

        ## Return true if we escape time loop
        return True


    ##                                          ##
    ##               On Click                   ##
    ##                                          ##
    ##                                          ##


    def __connectToPort(self):
        try:

            port = self.port_vars.get()
            self.logger.debug('Connecting to Port: {}'.format(port))

            self.logger.debug('----Initalizing Arduino Interface----')
            self.arduino_interface = Arduino_Interface(port, self.log_handler)

            ## Send ping
            self.arduino_interface.ping(self.pingCallback)

            ## Do we need a delay to allow communcation??
            if self.status_reg[Arduino_Interface.PING]:
                self.logger.info('Successfully Connected to port {}'.format(port))
                ## Green light
            else:
                self.logger.info('Connection to port {} unsuccessful'.format(port))
                ## Red Light
        except Exception as e:
            self.logger.error('Exception: {}'.format(str(e)))


    def __getTestData(self):
        for i in range(50):
            self.logger.debug('----Getting Test Data----')
            self.arduino_interface.requestTestData(self.testDataCallback)

            self.logger.debug('x_buffer: {}'.format(len(self.x_buffer)))
            self.logger.debug('y_buffer: {}'.format(len(self.y_buffer)))
            self.rt_plot.read_data(self.x_buffer, self.y_buffer)

            self.flushBuffers()

    def __quit(self):
        self.destroy()


    ##                                          ##
    ##                CallBacks                 ##
    ##                                          ##
    ##                                          ##
    
    def pingCallback(self, status):
        self.logger.debug('pingCallback')
        self.status_reg[Arduino_Interface.PING] = status

    def testDataCallback(self, incoming_data):
        self.logger.debug('----testDataCallback----')


        for idx,data in enumerate(incoming_data):
            ## Time Point
            if (idx % 2 == 0):
                self.x_buffer.append(data)
            else:
                self.y_buffer.append(data)


        ## Make buffers the same size
        while len(self.x_buffer) > len(self.y_buffer):
            self.x_buffer.pop()
      

    ##                                          ##
    ##              Initalization               ##
    ##                                          ##
    ##                                          ##

    def __serialConfigInit(self, serial_config):
        self.logger.debug('serialConfig')

        self.serial_baud = serial_config['baud']
        self.cmd_listID = serial_config['command_list']

    def __widgetInit(self, widget_config):
        self.logger.debug('widgetInit')

        ## Port list
        self.port_vars = StringVar(self)
        port_list = self.__getPorts()
        self.port_select = OptionMenu(self.left_frame, self.port_vars, *port_list)
        self.port_select.grid(sticky=tk.N, row=1, column=1)

        ## Connect Button
        self.connect_button = Button(self.left_frame, text='Connect', command=self.__connectToPort)
        self.connect_button.grid(sticky=tk.S, row=1, column=1)

        ## Set scroll window for data display
        self.listbox = Listbox(self.bottom_frame)
        self.listbox.grid(sticky=tk.E+tk.W, row=0, column=0, columnspan=100, rowspan=100)

        ## Get Continuous Data Button
        self.get_data_button = Button(self.left_frame, text='Get Test Data', command=self.__getTestData)
        self.get_data_button.grid(row=2, column=1)

        ## Set quit button
        self.quit_button = Button(self.left_frame, text="Quit", command=self.__quit)
        self.quit_button.grid(sticky=tk.S, row=19, column=1)


    def __graphInit(self, graph_config):
        self.logger.debug('graphInit')
        ## Wrap generated graph values
        # (Place somewhere else?)
        graph_values = {}
        graph_values['x'] = self.graph_x / self.dpi # Get graph in inches 
        graph_values['y'] = self.graph_y / self.dpi # Get graph in inches 
        graph_values['dpi'] = self.dpi
        
        self.rt_plot = RT_Plot(self.graph_frame, graph_config, graph_values) 

    def __tkInit(self, tk_config):
        self.logger.debug('tkInit')

        ## Set Title and icon for window 
        top_title = tk_config['top_title']
#        icon = tk_config['window_icon']

        ## Set DPI
        self.dpi = tk_config['dpi']

        ## Set Colors 
        main_background = tk_config['main_background']
        lf_bg = tk_config['lf_background']
        bf_bg = tk_config['bf_background']
        graph_bg = tk_config['graph_background']
 
        ## Main Frame
        self.main_x = tk_config['main_x']
        self.main_y = tk_config['main_y']

        ## Left Frame
        self.lf_x = self.main_x * tk_config['lf_x_scale']
        self.lf_y = self.main_y
        
        ## Bottom Frame
        self.bf_x = self.main_x * tk_config['bf_x_scale']
        self.bf_y = self.main_y  * tk_config['bf_y_scale']

        ## Graph Frame
        self.graph_y = self.main_y * tk_config['graph_y_scale']
        self.graph_x = self.main_x * tk_config['graph_x_scale']

        #tk.Tk.iconbitmap(self, default={}).format(icon)
        tk.Tk.wm_title(self, top_title)
       
        ## Main Frame
        self.main_frame = Frame(height=self.main_y, width=self.main_x, bg=main_background)
        self.main_frame.grid(column=0)
        self.__configureGrid(self.main_frame, tk_config['default_max_rows'], tk_config['default_max_cols'])

        ## Left Frame
        self.left_frame = Frame(self.main_frame, width = self.lf_x, height = self.lf_y, bg=lf_bg) 
        self.left_frame.grid(sticky=tk.W, row=0,column=0, rowspan=10, columnspan=2)
        self.left_frame.grid_propagate(False)
        self.__configureGrid(self.left_frame, tk_config['default_max_rows'], tk_config['default_max_cols'])
        
        ## Bottom Frame
        self.bottom_frame = Frame(self.main_frame, width = self.bf_x, height = self.bf_y, bg=bf_bg)
        self.bottom_frame.grid(sticky=tk.S, row=9, column=2)
        self.bottom_frame.grid_propagate(False)
        self.__configureGrid(self.bottom_frame, tk_config['default_max_rows'], tk_config['default_max_cols'])

        ## Graph Frame
        self.graph_frame = Frame(self.main_frame, width = self.graph_x, height = self.graph_y, bg=graph_bg)
        self.graph_frame.grid(sticky=tk.N, row=0, column=2)

if __name__=='__main__':

    c = Config()

    default_config = c.getDefault()

    GUI = Tk_Interface(default_config)
    GUI.mainloop()
