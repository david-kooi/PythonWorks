from pgedraw import basic as Prims #Primatives
import pyglet
import logging

class Config(object):
    instance = None

    class __Config(object):

      def configurePodImages(self):
          for POD_IMAGE in self.pod_images:
              POD_IMAGE.anchor_x = POD_IMAGE.width / 2 ## Set anchor point to middle of image
              POD_IMAGE.anchor_y = POD_IMAGE.height / 2
      def __init__(self, Interface=None):
          self.logger = logging.getLogger('Config')


          ## Auto Adjust
          self.AutoAdjust_ENABLED = True

          ## Interface Things
          self.INTERFACE_HEIGHT = Interface.window_height
          self.INTERFACE_WIDTH = Interface.window_width

          ## Batches
          self.CASE_1_BATCH = Interface.case1_batch
          self.GENERAL_BATCH = Interface.general_batch

          #Groups
          self.GROUP_A = Interface.group_a
          self.GROUP_B = Interface.group_b
          self.GROUP_C = Interface.group_c

          ## COLORS
          self.IF_BG_COLOR = (176, 163, 156, 255) ## Interface Background 
          self.TRACK_COLOR = (228, 68, 68, 255)
          self.BLUE = (64, 97, 228, 255)
          self.BLACK = (0,0,0,0)

          ## General Attributes
          self.CASE_1_numPods = 1
          self.CASE_1_POD_SPACING = Interface.window_width/self.CASE_1_numPods
          self.PULSE_WIDTH = 2
          self.NODE_TIME_DISTANCE = self.PULSE_WIDTH * 1 # Distance in time
          self.TRACK_HEIGHT = Interface.window_height / 2

          ## Node Attributes
          self.CASE_1_numNodes = 1
          self.NODE_RADIUS = 15
          self.CASE_1_NODE_SPACING = Interface.window_width/self.CASE_1_numNodes
          self.logger.debug('NodeSpacing: {}'.format(self.CASE_1_NODE_SPACING))
          self.NODE_IMAGE = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/node.png')   
          self.NODE_IMAGE.anchor_x = self.NODE_IMAGE.width / 2
          self.NODE_IMAGE.anchor_y = self.NODE_IMAGE.height / 2


          ## Pod Attributes
          self.pod_images = []
          self.POD_IMAGE_1 = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/pod_1.png')
          self.pod_images.append(self.POD_IMAGE_1)
          self.POD_IMAGE_2 = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/pod_2.png')
          self.pod_images.append(self.POD_IMAGE_2)
          self.POD_BUFFER_RANGE = self.CASE_1_NODE_SPACING
          ## Configure Pod Images
          self.configurePodImages()

          self.POD_RADIUS = 30
          self.POD_VEL = self.CASE_1_NODE_SPACING/(self.NODE_TIME_DISTANCE) # r = d/t where t = 1s
          self.MAX_POD_VEL = self.POD_VEL + 1000

          self.logger.debug('DEFAULT POD VELOCITY: {}'.format(self.POD_VEL))
          self.logger.debug('MAX POD VELOCITY: {}'.format(self.MAX_POD_VEL))


          ## Track Attributes
          self.TRACK_IMAGE = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/track.png')
          self.TRACK_IMAGE.anchor_x = 0
          self.TRACK_IMAGE.anchor_y = self.TRACK_IMAGE.height / 2    


          ## Background
          self.BG_IMAGE = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/bg.png')
          self.BG_IMAGE.anchor_y = 0
          self.BG_IMAGE.anchor_x = 0

          ## Detector Field
          self.DETECT_IMAGE = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/d_field.png')
          self.DETECT_IMAGE.anchor_x = self.DETECT_IMAGE.width
          self.DETECT_IMAGE.anchor_y = self.DETECT_IMAGE.height / 2
          self.GENERAL_DETECTION_RADIUS = self.CASE_1_NODE_SPACING / 1
          print 'GENERAL DETECTION RADIUS: {}'.format(self.GENERAL_DETECTION_RADIUS)
  
          ## Interface Attributes
          self.X_ZERO = 0
          self.Y_ZERO = Interface.Y_ZERO
  
  
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
