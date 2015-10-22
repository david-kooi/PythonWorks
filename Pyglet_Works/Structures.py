
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

    MOVE = 'MOVE' 
    START_NB = 'START_NODE_BUFFER_TIME'
    START_PB = 'START_POD_BUFFER'
    HAS_CONTACT = 'HAS_CONTACT'
    CHECK_POD_BUFFER = 'CHECK_POD_BUFFER'

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

        self.timer = 0

        ## Pod States   
        self.pod_buffering = False # 1st Priority
        self.bufferer_pod = None 
        self.node_buffering = False # 2nd Priority

    def event_handler(self, command, pod=None, node=None, dt=None):
        ## Move happens unconditionally
        if command== Pod.MOVE:
            # TODO: Add code error protection
            #if dt is None:
            #    raise UsageException

            self.move(dt)


        ## Pod Buffering takes priority over Node Buffering
        if command == Pod.CHECK_POD_BUFFER:
            self.logger.debug('---- CHECK_POD_BUFFER ----')
            if self.exitedPodBufferRange():
                self.STOP_pod_buffer()

        if command == Pod.START_NB:
            self.logger.debug('---- START NODE BUFFER ----')
            self.START_node_buffer()

        if command == Pod.START_PB:
            #if pod is None:
            #    raise UsageException

            self.logger.debug('---- START POD BUFFER ----')
            self.START_pod_buffer(pod)
            self.adjustPodBufferVelocity(pod)

        if command == Pod.HAS_CONTACT:
            self.logger.debug('---- HAS_CONTACT ----')
            #if node = None:
            # raise UsageException
            self.hasContact(node)
    

    def move(self, dt):
        ## Safeguard against extreme speed
        self.logger.debug('POD {} | VEL {}'.format(self.ID, self.velocity))
        if self.velocity >= self.config.MAX_POD_VEL:
            self.velocity = self.config.POD_VEL

        #self.position_logger.info('{}'.format(self.SPRITE.x))
        self.SPRITE.x += self.velocity * dt
        #self.label.y  += self.velocity * dt
    def adjustPodBufferVelocity(self, bufferer_pod):
        pod_buffer = bufferer_pod.SPRITE.x - self.SPRITE.x
        velocity_decrease = - ( (self.config.CASE_1_NODE_SPACING - pod_buffer) / self.config.NODE_TIME_DISTANCE )
        self.velocity += velocity_decrease

        self.logger.debug('Default Velocity: {}'.format(self.config.POD_VEL))
        self.logger.debug('Velocity Decrease: {}'.format(velocity_decrease))

    def isBehind(self, pod):
        distance_between = pod.SPRITE.x - self.SPRITE.x
        if distance_between > 0:
            return True
    ## Starts when in range of node PULSE
    def START_node_buffer(self):
        self.buffer_time_START = time.time()
        self.node_buffering = True

    def START_pod_buffer(self, pod):
        self.bufferer_pod = pod
        self.pod_buffering = True

    def STOP_pod_buffer(self):
        self.velocity = self.config.POD_VEL
        self.bufferer_pod = None
        self.pod_buffering = False

    def exitedPodBufferRange(self):
        self.logger.debug('checking pod buffer range')
        buffer_range = abs(self.bufferer_pod.SPRITE.x - self.SPRITE.x)
        self.logger.debug('buffer_range: {}'.format(buffer_range))
        if buffer_range >= self.config.POD_BUFFER_RANGE:
            return True
        return False

    def hasContact(self, node):
            self.logger.debug('---- NODE {} BUFFER CONTACT POD {} ----'.format(node.ID, self.ID))
            self.buffer_time_END = time.time()
            total_buffer_time = self.buffer_time_END - self.buffer_time_START
            self.logger.debug('buffer_time: {}'.format(total_buffer_time))        

            ## Adjust vel
            self.adjustNodeContactVelocity(total_buffer_time)

            self.data_logger.info('V_{}'.format(self.velocity))
            self.data_logger.info('B_{}'.format(total_buffer_time))

            self.node_buffering = False
    
    def adjustNodeContactVelocity(self, buffer_time):
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
        l = self.SPRITE.x - self.config.GENERAL_DETECTION_RADIUS
        ## Lower Detection radius of bottom node is translated to the top of the screen
        if l <= 0:
            l = self.config.INTERFACE_WIDTH - self.config.GENERAL_DETECTION_RADIUS
        
        u = self.SPRITE.x

        ## If lower radius is greater than upper limit then make upper limit top of screen
        if l >= u:
            u = self.config.INTERFACE_WIDTH

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
                
            else:
                ## Check if pod is in valid node buffer zone
                if (pod.SPRITE.x >= self.LOWER_DETECTION_RADIUS) and (pod.SPRITE.x < self.UPPER_DETECTION_RADIUS):  
                    self.logger.debug('------- NODE {} BUFFERING POD {} --------'.format(self.ID, pod.ID))
                   # self.logger.debug('| {}-POD_Y: {} | {}-NODE_Y: {} | '.format(pod.ID, pod.SPRITE.x, self.ID, self.SPRITE.x))
                    pod.event_handler(Pod.START_NB) ## Start Node Buffer
                    #pod.START_buffer_time()


    def isContact(self, pod):
        distance = abs(pod.SPRITE.x - self.SPRITE.x)
        if distance < 5:
            return True

        return False


