from RT_Plot import *
from Config import Config 
import Tkinter as tk
from Tkinter import *


import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

class Tk_Interface(tk.Tk):

    def __init__(self, config, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)
           
        tk_config = config['tk_window'] 
        graph_config = config['graph']

        ## Initalize Window
        self.__tkInit(tk_config)
       
        ## Initalize Graph
        self.__graphInit(graph_config)

    def __graphInit(self, graph_config):
        
        ## Wrap generated graph values
        # (Place somewhere else?)
        graph_values = {}
        graph_values['x'] = self.graph_x / self.dpi # Get graph in inches 
        graph_values['y'] = self.graph_y / self.dpi # Get graph in inches 
        graph_values['dpi'] = self.dpi
        
        print 'Before RT_plot'
        rt_plot = RT_Plot(self.graph_frame, graph_config, graph_values) 
        print 'After RT_Plot'

    def __tkInit(self, tk_config):
        ## Set Title and icon for window 
        top_title = tk_config['top_title']
#        icon = tk_config['window_icon']

        ## Set DPI
        self.dpi = tk_config['dpi']

        ## Set Colors 
        main_background = tk_config['main_background']
        lf_bg = tk_config['lf_background']
        graph_bg = tk_config['graph_background']
 
        ## Main Frame
        self.main_x = tk_config['main_x']
        self.main_y = tk_config['main_y']

        ## Left Frame
        self.lf_x_scale = tk_config['lf_x_scale']
        self.lf_x = self.main_x * self.lf_x_scale
        self.lf_y = self.main_y
        
        ## Bottom Frame
        self.bf_x_scale = tk_config['bf_y_scale']
        self.bf_x = self.main_x * self.bf_x_scale
        self.bf_y = self.main_y  

        ## Graph Frame
        self.graph_y_scale = tk_config['graph_y_scale']
        self.graph_x_scale = tk_config['graph_x_scale']
        self.graph_y = self.main_y * self.graph_y_scale
        self.graph_x = self.main_x * self.graph_x_scale

        #tk.Tk.iconbitmap(self, default={}).format(icon)
        tk.Tk.wm_title(self, top_title)
       
        self.main_frame = Frame(height=self.main_y, width=self.main_x, bg=main_background)
        self.main_frame.grid(column=0)

        self.left_frame = Frame(self.main_frame, width = self.lf_x, height = self.lf_y, bg=lf_bg) 
        self.left_frame.grid(sticky=tk.W, row=0,column=0)
        
        self.graph_frame = Frame(self.main_frame, width = self.graph_x, height = self.graph_y, bg=graph_bg)
        self.graph_frame.grid(sticky=tk.NE, row=0, column=1)

 




if __name__=='__main__':

    c = Config()

    default_config = c.getDefault()

    GUI = Tk_Interface(default_config)
    GUI.mainloop()
