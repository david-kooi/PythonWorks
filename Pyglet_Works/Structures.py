
import logging
import pyglet
import time
import Config
from pyglet.text import Label


class Clock(pyglet.event.EventDispatcher):
    def __init__(self):
        Clock.register_event_type('pulse')
    def startPulse(self):
        self.dispatch_event('pulse')


class Pod(object):

    def __init__(self, sprite, default_velocity, ID):
        self.logger = logging.getLogger('process_logger.POD')
        self.data_logger= logging.getLogger('data_logger')

        ## Config
        self.config = Config.Config()
        self.logger.debug('autoADJ: {}'.format(self.config.AutoAdjust_ENABLED))

        ## Sprite contains the coordinates
        self.SPRITE = sprite 

        self.ID = ID
       	self.velocity = default_velocity 

        ## AutoAdjust Variables
        self.buffer_time_START = 0
        self.buffer_time_END = 0
        self.BUFFERING = False

        self.timer = 0


    ## 60 Hz
    def move(self, dt):

        #self.position_logger.info('{}'.format(self.SPRITE.y))
        self.SPRITE.y += self.velocity * dt
        #self.label.y  += self.velocity * dt

    ## Starts when in range of node PULSE
    def START_buffer_time(self):
        self.buffer_time_START = time.time()
        self.BUFFERING = True


    def hasContact(self, node):
        if self.BUFFERING:
            self.logger.debug('---- NODE {} BUFFER CONTACT POD {} ----'.format(node.ID, self.ID))
            self.buffer_time_END = time.time()
            total_buffer_time = self.buffer_time_END - self.buffer_time_START
            self.logger.debug('buffer_time: {}'.format(total_buffer_time))    

            if total_buffer_time > 1:
                total_buffer_time = 0        

            ## Adjust vel
            self.adjustVelocity(total_buffer_time)

            self.data_logger.info('V_{}'.format(self.velocity))
            self.data_logger.info('B_{}'.format(total_buffer_time))

            self.BUFFERING = False
    
    def adjustVelocity(self, buffer_time):
        if self.config.AutoAdjust_ENABLED:
            self.logger.debug('Adjusting Velocity')
            spacing = self.config.CASE_1_NODE_SPACING
            time_distance = self.config.NODE_TIME_DISTANCE
            self.velocity =  spacing / (time_distance - buffer_time)


    def resetAutoAdjust(self):
        ## AutoAdjust Variables
        self.buffer_time_START = 0
        self.buffer_time_END = 0

class Node(object):
    def __init__(self, pod_registry, sprite, clock, ID):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('process_logger.NODE')
        self.data_logger = logging.getLogger('data_logger')


        ## Get Object Registry
        self.pod_registry = pod_registry

        ## Register self to pulse updates
        clock.push_handlers(self)

        ## Get Config
        self.config = Config.Config()
        

        ## Time Buffers
        self.buffer_time = 0

        ## Other
        self.ID = ID
        self.SPRITE = sprite 
        limits = self.getDetectionRadius()
        self.UPPER_DETECTION_RADIUS = limits['upper']
        self.LOWER_DETECTION_RADIUS = limits['lower']

        ## State Variables
        self.POD_IN_CONTACT = None
        self.BUFFERING = False


    def getDetectionRadius(self):
        l = self.SPRITE.y - self.config.GENERAL_DETECTION_RADIUS
        ## Lower Detection radius of bottom node is translated to the top of the screen
        if l <= 0:
            l = self.config.INTERFACE_HEIGHT - self.config.GENERAL_DETECTION_RADIUS
        
        u = self.SPRITE.y

        ## If lower radius is greater than upper limit then make upper limit top of screen
        if l > u:
            u = self.config.INTERFACE_HEIGHT

        ## Wrap return values
        d = dict()
        d['lower'] = l
        d['upper'] = u

        self.logger.debug('---- NODE {} DETECTION LIMITS ----'.format(self.ID))
        self.logger.debug('UPPER {} | LOWER {}'.format(u, l))
        
        return d

    def pulse(self):
        self.logger.debug('NODE {} PULSE'.format(self.ID))

        self.checkPulseContact()
            
    def checkPulseContact(self):
        for pod in self.pod_registry:
            
            if self.isContact(pod):
                self.logger.debug('---- NODE {} PULSE CONTACT POD {} ----'.format(self.ID, pod.ID))
                pod.velocity = self.config.POD_VEL
                self.POD_IN_CONTACT = pod

                self.data_logger.info('V_{}'.format(pod.velocity))
                self.data_logger.info('B_0')


            else:
                ## Check if pod is in valid buffer zone
                if (pod.SPRITE.y >= self.LOWER_DETECTION_RADIUS) and (pod.SPRITE.y < self.UPPER_DETECTION_RADIUS):  
                    self.logger.debug('------- NODE {} BUFFERING POD {} --------'.format(self.ID, pod.ID))
                   # self.logger.debug('| {}-POD_Y: {} | {}-NODE_Y: {} | '.format(pod.ID, pod.SPRITE.y, self.ID, self.SPRITE.y))
                    pod.START_buffer_time()

        ## TODO: Add case for when there is no pod in near distance

    def isContact(self, pod):
        distance = abs(pod.SPRITE.y - self.SPRITE.y)
        if distance < 5:
            return True

        return False


