from pgedraw import basic as Prims #Primatives
import pyglet
import logging

class Config(object):


	def __init__(self, Interface):
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger('Config')

            self.IF_BG_COLOR = (176, 163, 156, 255)
            self.TRACK_COLOR = (228, 68, 68, 255)
            self.POD_COLOR = (255, 255, 255, 255)
            self.POD_RADIUS = 30

            self.X_ZERO = Interface.X_ZERO
            self.Y_ZERO = Interface.Y_ZERO

            self.TRACK_X = self.X_ZERO-self.POD_RADIUS
            self.TRACK_Y = self.Y_ZERO/2

            self.TRACK_WIDTH = self.POD_RADIUS*2
            self.TRACK_LENGTH = Interface.Y_ZERO * 2 # Track length is height of the screen



            self.config = dict()

            ## Title & Control Buttons
            self.config['general'] = dict()
            self.config['general']['background_group'] = dict()
            self.config['general']['background_group']['bg'] = Prims.Rectangle((0, 0, Interface.window_width, Interface.window_height), 
                                                                                      color=self.IF_BG_COLOR, strip=False)
      

            self.config['general']['foreground_group'] = dict()

            self.config['general']['labels'] = dict()
            self.config['general']['labels']['title']= pyglet.text.Label('Default Title', 
                                                                              font_name='Times New Roman', 
                                                                              font_size=36,
                                                                              x=self.X_ZERO, y=1.5*self.Y_ZERO)
                                                                                                    


            ## Linear Motion
            self.config['case_1'] = dict()
            self.config['case_1']['background_group'] = dict()
            self.config['case_1']['background_group']['POD'] = Prims.Circle((self.X_ZERO, self.Y_ZERO), 
                                                                       self.POD_RADIUS, 
                                                                       color=self.POD_COLOR, 
                                                                       strip=False
                                                                     )

            self.config['case_1']['background_group']['TRACK'] = Prims.Rectangle((self.TRACK_X, 0, 
                                                                                  self.TRACK_WIDTH, 
                                                                                  self.TRACK_LENGTH), 
                                                                                  color=self.TRACK_COLOR
                                                                                )
                                                                          

            self.config['case_1']['foreground_group'] = []

            ## Circular Motion
            self.config['case_2'] = dict()
            self.config['case_2']['background_group'] = dict()
            self.config['case_2']['background_group']['POD'] = Prims.Circle((self.X_ZERO, self.Y_ZERO), 
                                                                       100, 
                                                                       color=self.POD_COLOR, 
                                                                       strip=False
                                                                     )        


