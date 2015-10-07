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

		## Get Configs and object registries
		self.Config = Config.Config(self)
		self.case_1_objs = self.Config.config['case_1']
		self.case_2_objs = self.Config.config['case_2']

		## Default Case
		self.current_case = Interface.CASE_1

		## Register case triggers
		self.periodics = Periodic(self)
		self.case_triggers = dict()
#		self.case_triggers[Interface.CASE_1] = self.periodics.case_1
#		self.case_triggers[Interface.CASE_2] = self.periodics.case_2

		## Batch and Group Hiearchy	
			## General Batch
			#	|
			#	- background [Ordered Group]
			#	|
			#	- foreground [Ordered Group]
			#
			## Case Batch
			#   |
			#	- background
			#	|
			#   - foreground
		## When on draw is called the general and case batch will be drawn

		## Create Batches and Groups
		self.general_batch = pyglet.graphics.Batch()
		self.case_batch = pyglet.graphics.Batch()
		self.general_labels = []
		self.case_labels = []

		self.background_group = pyglet.graphics.OrderedGroup(0)
		self.foreground_group = pyglet.graphics.OrderedGroup(1)

		## Create a way to access the groups
		self.batch_dict = dict()
		self.batch_dict['background_group'] = self.background_group
		self.batch_dict['foreground_group'] = self.foreground_group

		## Fill batches
		tup = self.fillBatch(Interface.GENERAL)
		self.general_batch = tup[0]
		self.general_labels = tup[1]

		tup = self.fillBatch(self.current_case)
		self.case_batch = tup[0]
		self.case_labels = tup[1]

		## Start Periodic Functions
		#pyglet.clock.schedule_interval(self.case_triggers[self.current_case], 1)
		#pyglet.clock.schedule_interval(self.periodics.case_1_track_clock, 1.5)

	
	def fillBatch(self, whichBatch):
		"""
		whichBatch: Batch to fill.
		returns: (batch, labels) tuple
		"""
		logger.debug('----fillBatch----')
		logger.debug('Filling batch: {}'.format(whichBatch))

		this_batch = pyglet.graphics.Batch()
		these_labels = []

		## Migrate Primitives to general_batch and case_batch
		for category in self.Config.config:			

			if not (category == whichBatch): ## Continue if this category is not what we're looking for
				continue
			logger.debug('category: {}, whichBatch: {}'.format(category, whichBatch))

			for group in self.Config.config[category]:

				if group == 'background_group':
					this_group = self.background_group
				elif group == 'foreground_group':
					this_group = self.foreground_group
				else:
					## Then we are dealing with labels
					pass

				for key in self.Config.config[category][group]:
					prim = self.Config.config[category][group][key]
					if(isinstance(prim, pgedraw.basic.Shape)): ## If we have a primitive
							this_batch.migrate(prim.vertex_list, prim.mode, this_group, this_batch)
							#this_batch.add(prim.vertex_list.get_size(), prim.mode, this_group, prim.vertex_list.vertices)
					elif(isinstance(prim, pyglet.text.Label)): ## We have labels
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
	def another(self):
		logger.debug('another!')

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

	def case_1(self, dt):
		logger.debug("periodic: CASE_1")
		self.interface.something()

	def case_1_track_clock(self, dt):
		pass
	
	def case_2(self, dt):
		logger.debug('periodic: CASE_2')
		self.interface.another()

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger('Pyglet')


	## Create Window
	interface = Interface(w=750, h=750, c="Interface")
	

	## Run app
	pyglet.app.run()


