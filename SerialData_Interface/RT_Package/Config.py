

## Configuration class is singleton
class Config(object):

    instance = None

    def __init__(self):
        self.config = {} 
        
        self.config['graph'] = {}
        self.config['graph']['x_title'] = None
        self.config['graph']['y_title'] = None
        self.config['graph']['main_title'] = None
    
        self.config['Tk_window'] = {}
        self.config['Tk_window']['top_title'] = None
        self.config['Tk_window']['window_icon'] = None

    def getGraphConfig(self):
        return self.config['graph']      
    def getTkConfig(self):
        return self.config['Tk_window']
    
    def setGraphField(self, field, value):
        self.config['graph'][field] = value
    def setTkField(self, field, value):
         self.config['Tk_window'][field] = value
