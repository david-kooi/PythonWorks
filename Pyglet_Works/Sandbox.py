import pyglet
from pyglet.window import key
from pgedraw import basic as Prims #Primatives

import logging

## Subclass window
class Interface(pyglet.window.Window):
	BG_COLOR = (176, 163, 156, 255)
	X_ZERO = 0
	Y_ZERO = 0


	## Cases
	## CASE_1 is default
	CASE_1 = 1
	CASE_2 = 2


	def __init__(self, w, h, c):
		logger.debug("__init__")
		pyglet.window.Window.__init__(self, width=w, height=h, caption=c)    


		## Create Batch Dictionary
		self.b_dict = dict()
		self.b_dict['CASE_1']['batch'] = None
		self.b_dict['CASE_1']['config'] = dict()

		self.b_dict['CASE_2']['batch'] = None
        self.b_dict['CASE_2']['config'] = dict()
        ## And Fill
        self.fillBatchDicts(self.b_dict)


		## Set Coordinates
		X_ZERO = w/2
		Y_ZERO = h/2

		## Batch and Group Hiearchy	
			## Batch
			#	|
			#	- background
			#	|
			#	- foreground

		self.current_batch = pyglet.graphics.Batch()
		self.background = pyglet.graphics.OrderedGroup(0)
		self.foreground = pyglet.graphics.OrderedGroup(1)

		## Set Test Point
		self.c = Prims.Circle((X_ZERO, Y_ZERO), 5, color=(255, 255, 255, 255), strip=False)
		self.batch.migrate(self.c.vertex_list , self.c.mode, self.foreground, self.current_batch)

		## Set Background
		## We must migrate the vertex list to the batch
		s = self.get_size()
		self.bg = Prims.Rectangle((0,0, s[0], s[1]), color=Interface.BG_COLOR)
		self.batch.migrate(self.bg.vertex_list, self.bg.mode, self.background, self.current_batch)
		
		## Register Switch State Event Event
		#self.register_event_type('dispatch_switch_state')
		#self.push_handlers(dispatch_switch_state=self.switch_state)

		## Start Periodic Functions
		periodics = Periodic(self)
		pyglet.clock.schedule_interval(periodics.case_1_Trigger, 1)


	def fillBatchDicts(d, ):
		self.background = pyglet.graphics.OrderedGroup(0)
		self.foreground = pyglet.graphics.OrderedGroup(1)

		## Initalize Dicts as Batch's
		for case in d:
			d[case] = pyglet.graphics.Batch()
			d[case].migrate
		
	def switch_state(self, switch):
		logger.debug('switch_state')
		if(switch == CASE_1):
			self.current_batch = 
		if(switch == CASE_2):
			self.current_batch = 



	def on_activate(self):
		logger.debug('on_activate')

	def something(self):
		logger.debug("something!")

	def on_mouse_press(self, x, y, button, modifiers):
		print "mouse pressed"

	def on_draw(self):
		self.clear()

		self.current_batch.draw()



## Class containing periodic function for an Interface
class Periodic(object):
	def __init__(self, interface):
		self.interface = interface

	def case_1_Trigger(self, dt):
		print "trigger dt: {}".format(dt)
		self.interface.something()
		self.interface.switch_state(Interface.CASE_1)
	
	def case_2_Trigger(self, dt):
		pass


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger('Pyglet')


	## Create Window
	interface = Interface(w=750, h=750, c="Interface")
	

	## Run app
	pyglet.app.run()


