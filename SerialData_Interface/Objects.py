

## Configuration class is singleton
class Config(object):

    instance = None

    def __init__(self):
        # Only initalize when instance is None
        if(Config.instance == None):
            Config.instance = Config.__Config()

    def getGraphConfig(self):
        return Config.instance.config['graph']      
    def getTkConfig(self):
        return Config.instance.config['Tk_window']
    
    def setGraphField(self, field, value):
        Config.instance.config['graph'][field] = value
    def setTkField(self, field, value):
         Config.instance.config['Tk_window'][field] = value


    class __Config(object):
        
        def __init__(self):
            self.config = {} 
            
            self.config['graph'] = {}
            self.config['graph']['x_title'] = None
            self.config['graph']['y_title'] = None
            self.config['graph']['main_title'] = None
        
            self.config['Tk_window'] = {}
            self.config['Tk_window']['top_title'] = None
            self.config['Tk_window']['window_icon'] = None

