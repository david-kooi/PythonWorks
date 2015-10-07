from pgedraw import basic as Prims #Primatives
import pyglet
import logging


class ObjectRegistry(object):

	def __init__(self, Interface):
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger('ObjectRegistry')

		## COLORS
	    self.IF_BG_COLOR = (176, 163, 156, 255) ## Interface Background 
	    self.TRACK_COLOR = (228, 68, 68, 255)
	    self.BLUE = (64, 97, 228, 255)

	    ## Case1 Attributes
	    self.CASE_1_numPods = 3
	    self.CASE_1_POD_SPACING = Interface.window_height/self.CASE_1_numPods

	    ## Node Attributes
	    self.NODE_RADIUS = 15
	    self.NODE_COLOR = (203, 26, 10, 255)

	    ## Pod Attributes
	    self.POD_IMAGE = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/pod.png')
            self.POD_IMAGE.anchor_x = self.POD_IMAGE.width // 2 ## Set anchor point to middle of image
            self.POD_IMAGE.anchor_y = self.POD_IMAGE.height // 2 

            ## Track Attributes
            self.TRACK_IMAGE = pyglet.image.load('/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/res/track.png')
            self.TRACK_IMAGE.anchor_x = self.TRACK_IMAGE.width // 2 ## Set anchor point to middle of image
            self.TRACK_IMAGE.anchor_y = self.TRACK_IMAGE.height // 2         

            self.POD_RADIUS = 30
            self.POD_COLOR = (255, 255, 255, 255)
            self.POD_VEL = self.CASE_1_POD_SPACING/1 # r = d/t where t = 1s

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

            ##Another BUtton
            self.a_BUTTON_X = self.n_BUTTON_X
            self.a_BUTTON_Y = self.n_BUTTON_Y + 100

            self.objects = dict()
            self.objects['case_1'] = dict()

            ## Pods
            self.objects['case_1']['pod_1'] = self.createPod(self.X_ZERO, 0 * self.CASE_1_POD_SPACING, Interface.case1_batch)
            self.objects['case_1']['pod_2'] = self.createPod(self.X_ZERO, 1 * self.CASE_1_POD_SPACING, Interface.case1_batch)
            self.objects['case_1']['pod_3'] = self.createPod(self.X_ZERO, 2 * self.CASE_1_POD_SPACING, Interface.case1_batch)
            self.objects['case_1']['pod_4'] = self.createPod(self.X_ZERO, 3 * self.CASE_1_POD_SPACING, Interface.case1_batch)


            ## Track
            self.objects['case_1']['track'] = self.createTrack(self.X_ZERO, self.Y_ZERO, Interface.case1_batch)


	def createPod(self, x, y, case_batch):
            pod = pyglet.sprite.Sprite(self.POD_IMAGE, x, y, batch=case_batch)
            pod.scale = .2

            self.logger.debug('----pod created----')
            self.logger.debug('pod x: {} | pod y: {}'.format(pod.x, pod.y))
            return pod
        def createTrack(self, x, y, case_batch):
            track = pyglet.sprite.Sprite(self.TRACK_IMAGE, x, y, batch=case_batch)
            track.scale = 1

            self.logger.debug('----track created----')
            self.logger.debug('track x: {} | pod y: {}'.format(track.x, track.y))
            return track
