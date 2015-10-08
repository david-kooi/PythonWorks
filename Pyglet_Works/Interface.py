import pyglet
from pyglet.window import key
from pgedraw import basic as Prims #Primatives
import pgedraw

import Config
import ObjectRegistry
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

		## Default Case
		self.current_case = Interface.CASE_1

		## Set Width & Height
		self.window_width = w
		self.window_height = h
		
		## Set Coordinates
		self.X_ZERO = w/2
		self.Y_ZERO = h/2

		## Create Batches and Groups
		self.general_batch = pyglet.graphics.Batch()
		self.case1_batch = pyglet.graphics.Batch()
		self.general_labels = []
		self.case_labels = []

		## Get Configs and object registries
		self.configuration = Config.Config(Interface=self)
		self.ObjReg = ObjectRegistry.ObjectRegistry(self)

		## Register case triggers
		self.periodics = Periodic(self)
		self.case_triggers = dict()
#		self.case_triggers[Interface.CASE_1] = self.periodics.case_1
#		self.case_triggers[Interface.CASE_2] = self.periodics.case_2

	
		self.background_group = pyglet.graphics.OrderedGroup(0)
		self.foreground_group = pyglet.graphics.OrderedGroup(1)

		## Create a way to access the groups
		self.batch_dict = dict()
		self.batch_dict['background_group'] = self.background_group
		self.batch_dict['foreground_group'] = self.foreground_group

		## Start Periodic Functions
		#pyglet.clock.schedule_interval(self.case_triggers[self.current_case], 1)
		pyglet.clock.schedule_interval(self.periodics.case_1_pod_motion, 1/60.0)

	
	def fillBatch(self, batch_name, batch):
		"""
		whichBatch: Batch to fill.
		returns: (batch, labels) tuple
		"""
		logger.debug('----fillBatch----')
		logger.debug('Filling batch: {}'.format(batch_name))

		these_labels = []

		## Migrate Primitives to general_batch and case_batch
		for category in self.Config.config:			

			if not (category == batch_name): ## Continue if this category is not what we're looking for
				continue
			#logger.debug('category: {}, batch_name: {}'.format(category, batch_name))

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
							batch.migrate(prim.vertex_list, prim.mode, this_group, batch)
							#this_batch.add(prim.vertex_list.get_size(), prim.mode, this_group, prim.vertex_list.vertices)
					if(isinstance(prim, pyglet.sprite.Sprite)):
							pass
					elif(isinstance(prim, pyglet.text.Label)): ## We have labels
							these_labels.append(prim)
		return (batch, these_labels)


	def switch_state(self, switch):
		logger.debug('switch_state')
		if(switch == Interface.CASE_1):
			pass#self.current_batch = 
		if(switch == Interface.CASE_2):
			pass#self.current_batch = 


	def on_activate(self):
		logger.debug('----on_activate----')
	def on_close(self):
		logger.debug('----on_close----')
		## Delete all objects
		for obj_name, obj in self.ObjReg.objects:
			if isinstance(obj, pyglet.sprite.Sprite):
				obj.delete()


	def on_mouse_press(self, x, y, button, modifiers):
		print "mouse pressed"

	def on_draw(self):
		self.clear()

		self.case1_batch.draw()



## Class containing periodic function for an Interface
class Periodic(object):
	def __init__(self, interface):
		self.interface = interface
		self.config = Config.Config()

	def case_1_pod_motion(self, dt):
		#logger.debug("periodic: dt: {}".format(dt))
		pod_velocity = self.config.POD_VEL

		for obj in interface.ObjReg.objects['case_1']:
			if obj.split('_')[0] == 'pod':
				pod = interface.ObjReg.objects['case_1'][obj]
				pod.y += pod_velocity * dt  
				#logger.debug('batch: '.format(pod.batch))
				#logger.debug('pod y: {}'.format(pod.y))

				if pod.y >= self.interface.window_height + pod.height/2:
					pod.y = 0
		

	def case_1_track_clock(self, dt):
		pass
	
	def case_2(self, dt):
		logger.debug('periodic: CASE_2')
		self.interface.another()

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger('Pyglet')


	## Create Window
	interface = Interface(w=700, h=700, c="Interface")

	## Run app
	pyglet.app.run()


