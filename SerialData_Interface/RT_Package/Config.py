

## Configuration class is singleton
class Config(object):

    def __init__(self):
        self.config = {} 
        
        self.config['graph'] = {}
        self.config['graph']['x_title'] = None
        self.config['graph']['y_title'] = None
        self.config['graph']['main_title'] = None
    
        self.config['tk_window'] = {}
        self.config['tk_window']['top_title'] = None
        self.config['tk_window']['window_icon'] = None
        self.config['tk_window']['window_width'] = None
        self.config['tk_window']['window_height'] = None
        
        self.config['tk_window']['lf_width_scale'] = None
        self.config['tk_window']['bt_width_scale'] = None
        self.config['tk_window']['bt_height_scale'] = None
        self.config['tk_window']['graph_width_scale'] = None
        self.config['tk_window']['graph_height_scale'] = None
        
        ## Colors
        self.config['tk_window']['main_background'] = '#a6a8a4'
        self.config['tk_window']['lf_background'] = None
        self.config['tk_window']['bt_background'] = None

        ## Default Values
        self.config['default'] = {}

        self.config['default']['graph'] = {}
        self.config['default']['graph']['x_title'] = 'X Axis'
        self.config['default']['graph']['y_title'] = 'Y Axis'
        self.config['default']['graph']['main_title'] = 'Default Title'

        self.config['default']['tk_window'] = {}
        self.config['default']['tk_window']['top_title'] = 'Default Top Title'
        self.config['default']['tk_window']['window_height'] = 800 
        self.config['default']['tk_window']['window_width'] = 1000
        
        ## Width Scales
        self.config['default']['tk_window']['lf_width_scale'] = .2
        ## Bottom bar has same width as graph
        self.config['default']['tk_window']['bt_width_scale'] = .8
        self.config['default']['tk_window']['graph_width_scale'] = .8
        #
        
        ## Height Scales
        self.config['default']['tk_window']['bt_height_scale'] = .4
        self.config['default']['tk_window']['graph_height_scale'] = .6



    def getGraphConfig(self):
        return self.config['graph']      
    def getTkConfig(self):
        return self.config['tk_window']
    def getGraphDefault(self):
        return self.config['default']['graph']
    def getTkDefault(self):
        return self.config['default']['tk_window']
    
    ## Maps default settings to main configuration
    def setDefaultGUI(self):
        graph_defaults = self.getTkDefault()  

        for key, value in graph_defaults.iteritems():
            self.setTkField(key, value)

    def setGraphField(self, field, value):
        self.config['graph'][field] = value
    def setTkField(self, field, value):
         self.config['tk_window'][field] = value
if __name__ == '__main__':
    c = Config()
    c.setDefaultGUI()
