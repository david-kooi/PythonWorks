
import logging
import pyglet

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
        self.ID = ID

        ## Pod States
        # . Distance front
        # . Distance back 
        # . 
        # .
        

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
    def __init__(self, sprite, clock, ID):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('NODE')


        self.clock = clock
        self.clock.push_handlers(self)


        self.ID = ID

        self.SPRITE = sprite
    def pulse(self):
        self.logger.debug('NODE {} PULSED'.format(self.ID))
        






