from RT_Plot import *
from Config import Config 
import Tkinter as tk
from Tkinter import *

import logging
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg




class Tk_Interface(tk.Tk):

    def __init__(self, config, *args, **kwargs):  
        self.logger = logging.getLogger('Tk_Interface')
        self.logger.debug('__init__')

        tk.Tk.__init__(self, *args, **kwargs)
           
        tk_config = config['tk_window'] 
        graph_config = config['graph']

        ## Initalize Window
        self.__tkInit(tk_config)
       
        ## Initalize Graph
        self.__graphInit(graph_config)
        
        ## Initalize Widgets
        widget_config = {} # Temporary config dict.
        self.__widgetInit(widget_config)


        #insertIntoListbox()
        ## Temp run
       # self.test_update()
    
    def __widgetInit(self, widget_config):
        self.logger.debug('widgetInit')

        ## Set quit button
        self.quit_button = Button(self.left_frame, text="Quit", command=self.__quit)
        self.quit_button.grid(sticky=tk.S, row=0, column=0)

        ## Set port list and port connector button
        self.port_var = StringVar(self)

        port_list = self.__getPorts()
        self.port_select = OptionMenu(self.left_frame, self.port_var, *port_list)
        self.port_select.grid()

        self.connect_button = Button(self.left_frame, text='Connect', command=self.__connectToPort)
        self.connect_button.grid()

        ## Set scroll window for data display
        self.listbox = Listbox(self.bottom_frame)
        self.listbox.grid(sticky=tk.E+tk.W, row=0, column=0, columnspan=100, rowspan=100)

        ## Get Continuous Data Button
        self.get_data_button = Button(self.left_frame, text='Get Data', command=self.__getData)


    def insertIntoListbox():

        for i in range(100):
            self.listbox.insert(END, i)


    def __getData(self):
        pass

    def __getPorts(self):

        ports = ['one', 'two', 'n']

        return ports

    def __connectToPort(self):
        pass
    def __quit(self):
        self.destroy()

    def __configureGrid(self, frame):
        for x in range(60):
            Grid.columnconfigure(frame, x, weight=1)

        for y in range(30):
            Grid.rowconfigure(frame, y, weight=1)

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
        self.__configureGrid(self.main_frame)

        ## Left Frame
        self.left_frame = Frame(self.main_frame, width = self.lf_x, height = self.lf_y, bg=lf_bg) 
        self.left_frame.grid(sticky=tk.W, row=0,column=0, rowspan=10, columnspan=2)
        self.left_frame.grid_propagate(False)
        self.__configureGrid(self.left_frame)
        
        ## Bottom Frame
        self.bottom_frame = Frame(self.main_frame, width = self.bf_x, height = self.bf_y, bg=bf_bg)
        self.bottom_frame.grid(sticky=tk.S, row=9, column=2)
        self.bottom_frame.grid_propagate(False)
        self.__configureGrid(self.bottom_frame)


        ## Graph Frame
        self.graph_frame = Frame(self.main_frame, width = self.graph_x, height = self.graph_y, bg=graph_bg)
        self.graph_frame.grid(sticky=tk.N, row=0, column=2)

if __name__=='__main__':

    c = Config()

    default_config = c.getDefault()

    GUI = Tk_Interface(default_config)
    GUI.mainloop()
