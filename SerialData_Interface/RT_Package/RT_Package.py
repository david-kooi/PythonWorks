import config
import Tk_Interface 


class RT_Package(object):
 
    def __init__(config_file):
    """
    configFile: filename of configuration xml file
    """
        ## Setup Config
        self.package_config = parseConfigFile(config_file)

        tk_config = package_config.getTkConfig()
        graph_config = package_config.getGraphConfig()
        #


        self.tk_GUI = Tk_Interface(tk_config)
        
        




    def parseConfigFile(config_file):
        
        # Parse Stuffs



        return package_config
