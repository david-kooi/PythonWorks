import pyglet
from pyglet.window import key
from pgedraw import basic as Prims #Primatives
import pgedraw

import Config
import logging

## Subclass window
class Interface(pyglet.window.Window):
	BG_COLOR = (176, 163, 156, 255)
	X_ZERO = 0
	Y_ZERO = 0

	GENERAL = 'general'
	CASE_1 = 'case_1'
	CASE_2 = 'case_2'

	def __init__(self, w, h, c):
		logger.debug("__init__")
		pyglet.window.Window.__init__(self, width=w, height=h, caption=c)    

		## Set Width & Height
		self.window_width = w
		self.window_height = h
		
		## Set Coordinates
		self.X_ZERO = w/2
		self.Y_ZERO = h/2

		## Get Config
		self.Config = Config.Config(self)

		## Default Case
		self.current_case = 'case_1'

		## Batch and Group Hiearchy	
			## General Batch
			#	|
			#	- background [Ordered Group]
			#	|
			#	- foreground [Ordered Group]


		## Create Batches and Groups
		self.general_batch = pyglet.graphics.Batch()
		self.case_batch = pyglet.graphics.Batch()
		self.general_labels = []
		self.case_labels = []

		self.background_group = pyglet.graphics.OrderedGroup(0)
		self.foreground_group = pyglet.graphics.OrderedGroup(1)

		## Create a way to access the batches & groups
		self.batch_dict = dict()
		self.batch_dict['general_batch'] = self.general_batch
		self.batch_dict['case_batch'] = self.case_batch
		self.batch_dict['background_group'] = self.background_group
		self.batch_dict['foreground_group'] = self.foreground_group
		self.batch_dict['labels'] = []


		tup = self.fillBatch(Interface.GENERAL)
		self.general_batch = tup[0]
		self.general_labels = tup[1]

		tup = self.fillBatch(Interface.CASE_1)
		self.case_batch = tup[0]
		self.case_labels = tup[1]

		## Register Switch State Event Event
		#self.register_event_type('dispatch_switch_state')
		#self.push_handlers(dispatch_switch_state=self.switch_state)

		## Start Periodic Functions
		periodics = Periodic(self)
		pyglet.clock.schedule_interval(periodics.case_1_Trigger, 1)

	
	def fillBatch(self, whichBatch):
		"""
		whichBatch: Batch to fill.
		returns: (batch, labels) tuple
		"""
		logger.debug('----fillBatch----')
		logger.debug('Filling batch: {}'.format(whichBatch))


		these_labels = []
		this_batch = pyglet.graphics.Batch()

		## Migrate Primitives to general_batch and case_batch
		for category in self.Config.config:			
			logger.debug('category: {}, whichBatch: {}'.format(category, whichBatch))

			if not (category == whichBatch): ## Continue if this category is not what we're looking for
				continue

			for group in self.Config.config[category]:
				this_group = self.batch_dict[group]
				for key in self.Config.config[category][group]:
					prim = self.Config.config[category][group][key]
					if(isinstance(prim, pgedraw.basic.Shape)): ## If we have a primitive
							this_batch.migrate(prim.vertex_list, prim.mode, this_group, this_batch)
					elif(isinstance(prim, pyglet.text.Label)):
						these_labels.append(prim)
		return (this_batch, these_labels)


	def switch_state(self, switch):
		logger.debug('switch_state')
		if(switch == Interface.CASE_1):
			pass#self.current_batch = 
		if(switch == Interface.CASE_2):
			pass#self.current_batch = 



	def on_activate(self):
		logger.debug('on_activate')

	def something(self):
		logger.debug("something!")

	def on_mouse_press(self, x, y, button, modifiers):
		print "mouse pressed"

	def on_draw(self):
		self.clear()

		self.general_batch.draw()
		self.case_batch.draw()




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


