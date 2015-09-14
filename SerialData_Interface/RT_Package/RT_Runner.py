from Config import Config
from Tk_Interface import Tk_Interface 
import logging


#logger.setLevel(logging.DEBUG)

def setup(config_file):
    logger.debug('In setup')
   
    ## Parse Config File 
    package_config = parseConfigFile(config_file)

#    tk_config = package_config.getTkConfig()
#    graph_config = package_config.getGraphConfig()

    c = Config()
    default_config = c.getDefault()
    tk_GUI = Tk_Interface(default_config)
    tk_GUI.mainloop()

def parseConfigFile(config_file):
    logger.debug('parseConfigFile')
    pass    
    # Parse Stuffs

    #return package_config


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('RT_Package')
    
    setup(None)    

