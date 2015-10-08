
import logging

class Pod(object):

    def __init__(self, sprite, pod_ahead, default_velocity):
        self.SPRITE = sprite 
        self.Y_POS = self.SPRITE.y
        self.DEF_VELOCITY = default_velocity
        self.POD_AHEAD = pod_ahead

        ## Pod States
        # . Distance front
        # . Distance back 
        # . 
        # .
        

       	self.velocity = self.DEF_VELOCITY 
        self.distance_front = 0
        self.distance_back = 0


    def selfAdjust():
    	if self.POD_AHEAD.Y_POS - self.Y_POS < Config.POD_SPACING:
    		self.velocity =+ 1
    	else
    		self.velocity = self.DEF_VELOCITY


