

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
        self.config['tk_window']['main_icon'] = None
        self.config['tk_window']['main_x'] = None
        self.config['tk_window']['main_y'] = None
        
        self.config['tk_window']['lf_x_scale'] = None
        self.config['tk_window']['bf_x_scale'] = None
        self.config['tk_window']['bf_y_scale'] = None
        self.config['tk_window']['graph_x_scale'] = None
        self.config['tk_window']['graph_y_scale'] = None
        
        ## Colors
        self.config['tk_window']['main_background'] = '#a6a8a4' 
        self.config['tk_window']['lf_background'] = None
        self.config['tk_window']['bf_background'] = None

        ## Default Values
        self.config['default'] = {}

        self.config['default']['graph'] = {}
        self.config['default']['graph']['x_title'] = 'X Axis'
        self.config['default']['graph']['y_title'] = 'Y Axis'
        self.config['default']['graph']['main_title'] = 'Default Title'

        self.config['default']['tk_window'] = {}
        self.config['default']['tk_window']['top_title'] = 'Default Top Title'
        self.config['default']['tk_window']['main_y'] = 800 
        self.config['default']['tk_window']['main_x'] = 1400
        self.config['default']['tk_window']['dpi'] = 96

        ## Color
        self.config['default']['tk_window']['main_background'] = '#a6a8a4'
        self.config['default']['tk_window']['lf_background'] = '#30ff33' 
        self.config['default']['tk_window']['bf_background'] = '#30ff33'
        self.config['default']['tk_window']['graph_background'] = '#ab5950'
        
        ## Width Scales
        self.config['default']['tk_window']['lf_x_scale'] = .2
        ## left frame has same height as main
        ## Bottom bar has same width as graph
        self.config['default']['tk_window']['bf_x_scale'] = .8
        self.config['default']['tk_window']['graph_x_scale'] = .8
        #
        
        ## Height Scales
        self.config['default']['tk_window']['bf_y_scale'] = .25
        self.config['default']['tk_window']['graph_y_scale'] = .75

        ## Serial Config
        self.config['default']['serial_config'] = {}
        self.config['default']['serial_config']['baud'] = 9600
        self.config['default']['serial_config']['command_list'] = 'A'


        ## Commands
        self.config['command_listA'] = {}
        self.config['command_listA']['ping'] = int(0x0B)
        self.config['command_listA']['start_collection'] = int(0x0C)
        self.config['command_listA']['get_data_point'] = int(0x0D)



    def getGraphConfig(self):
        return self.config['graph']      

    def getTkConfig(self):
        return self.config['tk_window']

    def getDefault(self):
        return self.config['default']

    def getTkDefault(self):
        return self.config['default']['tk_window'] 
    def getCommandList(self, whichList):
        if whichList == 'A':
            return self.config['command_listA']

    def setGraphField(self, field, value):
        self.config['graph'][field] = value

    def setTkField(self, field, value):
         self.config['tk_window'][field] = value




