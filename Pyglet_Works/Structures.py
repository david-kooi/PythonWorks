
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
        self.logger = logging.getLogger('POD')

        ## Config
        self.config = Config.Config()

        ## Sprite and Coordinates
        self.SPRITE = sprite 
        self.Y_POS = self.SPRITE.y
        self.X_POS = self.SPRITE.x

        self.ID = ID
       	self.velocity = default_velocity 

        ## AutoAdjust Variables
        self.buffer_time_START = 0
        self.buffer_time_END = 0
        self.BUFFERING = False

        self.timer = 0

    def move(self, dt):
        self.timer += dt
        if self.timer > 1:
            self.timer = 0
            self.logger.debug('---- 1 SECOND ----')
            self.logger.debug('Y_POS: {}'.format(self.SPRITE.y))
        self.SPRITE.y += self.velocity * dt
        #self.label.y  += self.velocity * dt


    def START_buffer_time(self):
        self.buffer_time_START = time.time()
        self.BUFFERING = True

        #self.debug('---- BUFFER STARTED ----')
    def hasContact(self):
        if self.BUFFERING:
            self.logger.debug('BUFFER CONTACT')
            self.logger.debug('POD: {}'.format(self.ID))
            self.logger.debug('POD Y: {}'.format(self.SPRITE.y))

            self.buffer_time_END = time.time()
            total_buffer_time = self.buffer_time_END - self.buffer_time_START
            self.logger.debug('buffer_time: {}'.format(total_buffer_time))

            ## Adjust vel
            spacing = self.config.CASE_1_NODE_SPACING
            time_distance = self.config.NODE_TIME_DISTANCE
            self.velocity =  spacing / (time_distance - total_buffer_time)
            self.logger.debug('mod velocity: {}'.format(self.velocity))


            self.BUFFERING = False

    def setYPos(self,y):
    	self.SPRITE.y = y

    def setXPos(self, x):
    	self.SPRITE.x = x

    
    def resetAutoAdjust(self):
        ## AutoAdjust Variables
        self.buffer_time_START = 0
        self.buffer_time_END = 0

class Node(object):
    def __init__(self, pod_registry, sprite, clock, ID):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('NODE')

        ## Get Object Registry
        self.pod_registry = pod_registry

        ## Register self to pulse updates
        clock.push_handlers(self)

        ## Get Config
        self.config = Config.Config()
        
        ## State Variables
        self.POD_CONTACT = False

        ## Time Buffers
        self.buffer_time = 0

        ## Other
        self.ID = ID
        self.SPRITE = sprite 
        self.POD_IN_CONTACT = None

    def pulse(self):
        self.logger.debug('NODE {} PULSE'.format(self.ID))

        self.checkPulseContact()

            
    def checkPulseContact(self):
        for pod in self.pod_registry:
            
            if self.isContact(pod):
                self.logger.debug('---- PULSE CONTACT ----')
                pod.velocity = self.config.POD_VEL
                self.logger.debug('pod velocity: {}'.format(pod.velocity))
            else:
                self.logger.debug('---- BUFFERING ----')
                self.logger.debug('pod: {}'.format(pod.ID))
                self.logger.debug('POD_Y: {}'.format(pod.SPRITE.y))
                self.logger.debug('NODE_Y: {}'.format(self.SPRITE.y))
                pod.START_buffer_time()


    def isContact(self, pod):
        distance = abs(pod.SPRITE.y - self.SPRITE.y)
        if distance < 5:
           # self.logger.debug('---- CONTACT ----')
            #self.logger.debug('NODE: {}'.format(self.ID))
            #self.logger.debug('POD: {}'.format(pod.ID))
            return True
        return False


    def engageStateMachine(self):
        self.logger.debug('engageStateMachine')
        self.logger.debug('IS_ACTIVE: {}'.format(self.IS_ACTIVE))

        if self.IS_ACTIVE:
            loop_start = time.time()
            while True:
                if self.CLOCK_PULSED:
                    self.logger.debug('Time Buffer START')
                    To = time.time() # T naught

                    while True:
                        if self.POD_CONTACT:
                            self.logger.debug('Time Buffer STOP')
                            ## Timer stop 
                            Tf = time.time() # T final
                            self.buffer_time = Tf - To
                            break
                    break
                

                ## Timeout condition
                loop_end = time.time()
                elapsed_loop_time = loop_end - loop_start
                if elapsed_loop_time > 5:
                    self.logger.error('STATE MACHINE TIMEOUT')
                    break

            mod_velocity = self.config.CASE_1_NODE_SPACING / (self.config.NODE_TIME_DISTANCE + self.buffer_time)
            self.next_pod.velocity = mod_velocity

        self.resetStateVariables()


    def resetStateVariables(self):
        ## State Variables
        self.IS_ACTIVE = False
        self.START_BUFFER = True
        self.CLOCK_PULSED = False # 
        self.POD_CONTACT = False

        ## Reset Pod-Node Relationship
        self.unregisterPod()
        ## Time Buffers
        self.buffer_time = 0



