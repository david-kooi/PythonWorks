
import logging
import pyglet
import time
import Config

class Clock(pyglet.event.EventDispatcher):
    def __init__(self):
        Clock.register_event_type('pulse')
    def startPulse(self):
        self.dispatch_event('pulse')


class Pod(object):

    def __init__(self, sprite, pod_ahead, pod_behind, default_velocity, ID):
    	logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('POD')

        self.SPRITE = sprite 
        self.Y_POS = self.SPRITE.y
        self.X_POS = self.SPRITE.x
        self.DEF_VELOCITY = default_velocity
        self.POD_AHEAD = pod_ahead
        self.POD_BEHIND = pod_behind
        self.NODE_AHEAD = None
        self.ID = ID

       	self.velocity = self.DEF_VELOCITY 
        self.distance_front = 0
        self.distance_back = 0

    def setYPos(self,y):
    	self.SPRITE.y = y

    def setXPos(self, x):
    	self.SPRITE.x = x

    def selfAdjust(self):
    	if self.POD_AHEAD.Y_POS - self.Y_POS < Config.POD_SPACING:
    		self.velocity =+ 1
    	else:
    		self.velocity = self.DEF_VELOCITY

class Node(object):
    def __init__(self, node_registry, sprite, clock, ID):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('NODE')

        ## Get Object Registry
        self.node_registry = node_registry

        ## Register self to pulse updates
        clock.push_handlers(self)

        ## Get Config
        self.config = Config.Config()
        
        ## State Variables
        self.IS_ACTIVE = False
        self.START_BUFFER = True
        self.CLOCK_PULSED = False # 
        self.POD_CONTACT = False

        ## Time Buffers
        self.buffer_time = 0

        ## Other
        self.ID = ID
        self.SPRITE = sprite
        self.nextPod = None

    def pulse(self):
        self.logger.debug('NODE {} PULSE'.format(self.ID))
        self.logger.debug('IS_ACTIVE: {}'.format(self.IS_ACTIVE))

        if self.IS_ACTIVE:
            self.CLOCK_PULSED = True
        else:
            self.CLOCK_PULSED = False
        
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

    def registerNextPod(self, pod):
        self.next_pod = pod
        self.IS_ACTIVE = True

    def unregisterPod(self):
        next_node_id = self.ID + 1
        self.next_pod.NODE_AHEAD = self.node_registry[next_node_id]
        self.next_pod = None

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



