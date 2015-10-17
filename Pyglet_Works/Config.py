from pgedraw import basic as Prims #Primatives
import pyglet
import logging

class Config(object):
    instance = None

    class __Config(object):
      def __init__(self, Interface=None):
          self.logger = logging.getLogger('Config')


          ## Auto Adjust
          self.AutoAdjust_ENABLED = True

          ## Interface Things
          self.INTERFACE_HEIGHT = Interface.window_height
          self.INTERFACE_WIDTH = Interface.window_width

          ## Batches
          self.CASE_1_BATCH = Interface.case1_batch

          #Groups
          self.CASE_1_F_GROUP = Interface.foreground_group
          self.CASE_1_B_GROUP = Interface.background_group

          ## COLORS
          self.IF_BG_COLOR = (176, 163, 156, 255) ## Interface Background 
          self.TRACK_COLOR = (228, 68, 68, 255)
          self.BLUE = (64, 97, 228, 255)
          self.BLACK = (0,0,0,0)

          ## Case1 Attributes
          self.CASE_1_numPods = 1
          self.CASE_1_POD_SPACING = Interface.window_height/self.CASE_1_numPods
          self.PULSE_WIDTH = 1
          self.NODE_TIME_DISTANCE = self.PULSE_WIDTH * 1 # Distance in time

          ## Node Attributes
          self.NODE_RADIUS = 15
          self.NODE_COLOR = (203, 26, 10, 255)
          self.CASE_1_NODE_START = 50
          self.CASE_1_numNodes = 1
          self.CASE_1_NODE_SPACING = Interface.window_height/self.CASE_1_numNodes


          ## Pod Attributes
          self.POD_IMAGE = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/pod.png')
          self.POD_IMAGE.anchor_x = self.POD_IMAGE.width / 2 ## Set anchor point to middle of image
          self.POD_IMAGE.anchor_y = self.POD_IMAGE.height / 2 

          self.POD_RADIUS = 30
          self.POD_COLOR = (255, 255, 255, 255)
          self.POD_VEL = self.CASE_1_NODE_SPACING/(self.NODE_TIME_DISTANCE) # r = d/t where t = 1s
          self.logger.debug('POD_VEL: {}'.format(self.POD_VEL))

          ## Track Attributes
          self.TRACK_IMAGE = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/track.png')
          self.TRACK_IMAGE.anchor_x = self.TRACK_IMAGE.width / 2 ## Set anchor point to middle of image
          self.TRACK_IMAGE.anchor_y = self.TRACK_IMAGE.height / 2    

          ## Node Attributes
          self.NODE_IMAGE = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/node.png')   
          self.NODE_IMAGE.anchor_x = self.NODE_IMAGE.width / 2
          self.NODE_IMAGE.anchor_y = self.NODE_IMAGE.height / 2
  
          ## Interface Attributes
          self.X_ZERO = Interface.X_ZERO
          self.Y_ZERO = Interface.Y_ZERO
  
          ## Track Attributes
          self.TRACK_X = self.X_ZERO-self.POD_RADIUS
          self.TRACK_Y = self.Y_ZERO/2
  
          self.TRACK_WIDTH = self.POD_RADIUS*2
          self.TRACK_LENGTH = Interface.Y_ZERO * 2 # Track length is height of the screen
  
          self.BUTTON_HEIGHT = Interface.window_height/15
          self.BUTTON_WIDTH = Interface.window_width/5
  
          ##Next Button
          self.n_BUTTON_X = self.X_ZERO + self.X_ZERO/2
          self.n_BUTTON_Y = 0 + self.Y_ZERO/4
  
          ##Another Button
          self.a_BUTTON_X = self.n_BUTTON_X
          self.a_BUTTON_Y = self.n_BUTTON_Y + 100
  
  
    def __init__(self, Interface=None):
        print'----Creating Config----'
        if Config.instance == None:
            print 'Config instance is none'
            #if Interface == None:
            # raise Exception ## Must be first inialized with an Interface
            Config.instance = Config.__Config(Interface=Interface) 
        else:
            print 'Config instance exists'
        

    def __getattr__(self, name):
        return getattr(Config.instance, name)
