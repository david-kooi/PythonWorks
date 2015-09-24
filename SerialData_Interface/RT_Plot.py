import logging

import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
#matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


## Original Author: 
## http://stackoverflow.com/users/1007990/zah

class RT_Plot():  

    def __init__(self, graph_frame, graph_config, graph_values):
        """
        graph_frame: tk frame to hold the graph_frame
        graph_config: configuration that was set from xml config parse
        graph_values: values that were generated as a result of graph config
        """ 
        self.logger = logging.getLogger('RT_Plot')
        self.logger.debug('__init__')


        # Create Line
        self.data_line = Line2D([],[])

        # Create plot
        self.plot_holder = Figure(figsize=(graph_values['x'], graph_values['y']), dpi=graph_values['dpi']) 
        self.rt_plot = self.plot_holder.add_subplot(111)
        self.rt_plot.add_line(self.data_line)
        
        # Set Title Configuration
        self.rt_plot.set_ylabel(graph_config['y_title']) 
        self.rt_plot.set_xlabel(graph_config['x_title']) 
        self.plot_holder.suptitle(graph_config['main_title'], fontsize=16)

        # Autoscale on unknown axis 
        self.rt_plot.set_autoscaley_on(True)
        self.rt_plot.set_autoscalex_on(True)
        # Set x limits?

        # Create canvas
        canvas = FigureCanvasTkAgg(self.plot_holder, master=graph_frame)
        canvas.show()
        # Attach canvas to graph frame
        canvas.get_tk_widget().grid(row=0, column=0)



        #Set up plot
#        self.figure, self.ax = plt.subplots()
#        self.lines, = self.ax.plot([],[], 'o')
 
#        self.ax.set_xlim(self.min_x, self.max_x)
        #Other stuff
#        self.ax.grid()


    def read_data(self, xdata, ydata):
        #self.logger.debug('read_data')

        #Update data (with the new _and_ the old points)
        self.data_line.set_xdata(xdata)
        self.data_line.set_ydata(ydata)
        #Need both of these in order to rescale
        self.rt_plot.relim()
        self.rt_plot.autoscale_view()
        #We need to draw *and* flush
        self.plot_holder.canvas.draw()
        self.plot_holder.canvas.flush_events()

    #Example
    def __call__(self):

        self.setup()
        xdata = []
        ydata = []
        for x in np.arange(0,1000,0.5):
            xdata.append(x)
            ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
            self.read_data(xdata, ydata)
            time.sleep(.01)
        return xdata, ydata


if __name__ == '__main__':
    d = RT_Plot()
#    d()
