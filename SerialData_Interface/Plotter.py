import numpy as np
import time
import matplotlib.pyplot as plt

## Original Author: 
##                 http://stackoverflow.com/users/1007990/zah

class Plotter():
    #Suppose we know the x range
    min_x = 0
    max_x = 10

    def setup(self, graph_config):
        
        y_title = graph_config['y_title']
        x_title = graph_config['x_title'] 
        main_title = graph_config['main_title']
        
        #Set as interactive
        plt.ion()

        #Set up plot
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[], 'o')
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlim(self.min_x, self.max_x)
        #Other stuff
        self.ax.grid()


    def read_data(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

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
    d = Plotter()
    d()
