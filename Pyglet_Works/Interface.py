import pyglet
from pyglet.window import key
from pgedraw import basic as Prims #Primatives
import pgedraw

from Structures import Pod
from Structures import Clock
from Structures import Node
import ObjectRegistry
import logging
import Config
import subprocess

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
		logger.debug('window_width: {}'.format(w))
		logger.debug('window_height: {}'.format(h))

		pyglet.window.Window.__init__(self, width=w, height=h, caption=c)    

		## Clock Instance
		self.master_clock = Clock()

		## Default Case
		self.current_case = Interface.CASE_1

		## Set Width & Height
		self.window_width = w
		self.window_height = h
		
		## Set Coordinates
		self.X_ZERO = w/2
		self.Y_ZERO = h/2

		## Create Batches and Groups
		self.background_group = pyglet.graphics.OrderedGroup(0)
		self.foreground_group = pyglet.graphics.OrderedGroup(1)
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

		## Create a way to access the groups
		self.batch_dict = dict()
		self.batch_dict['background_group'] = self.background_group
		self.batch_dict['foreground_group'] = self.foreground_group

		## Start Periodic Functions
		#pyglet.clock.schedule_interval(self.case_triggers[self.current_case], 1)
		#pyglet.clock.schedule_once(self.periodics.case_1_node_pod_link, 0)
		pyglet.clock.schedule_interval(self.periodics.case_1_pod_motion, 1/60.0)
		pyglet.clock.schedule_interval(self.periodics.case_1_check_pod_contact, 1/60.0)
		#pyglet.clock.schedule_interval(self.periodics.case_1_engage_node_state_machine, 1/60.0)
		#pyglet.clock.schedule_interval(self.periodics.case_1_master_clock_ticker, self.configuration.PULSE_WIDTH)


	def on_activate(self):
		logger.debug('----on_activate----')
	def on_close(self):
		logger.debug('----on_close----')
		## Delete all objects
		#for pods in self.ObjReg.pod_registry:
	#		pod.SPRITE.delete()

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

	def case_1_node_pod_link(self, dt):
		logger.debug('----node pod link----')
		for idx,pod in enumerate(self.interface.ObjReg.pod_registry):
			pod.NODE_AHEAD = self.interface.ObjReg.node_registry[idx]
			pod.NODE_AHEAD.registerNextPod(self)

	def case_1_pod_motion(self, dt):
		#logger.debug("periodic: dt: {}".format(dt))
		pod_velocity = self.config.POD_VEL

		for pod in interface.ObjReg.pod_registry:

				#logger.debug('pod: {}'.format(pod.ID))
				#logger.debug('next node: {}'.format(pod.NODE_AHEAD.ID))
			     #   logger.debug('old pos: {}'.format(pod.SPRITE.y))
				#newPosition = pod.Y_POS + (pod_velocity * dt)
				#logger.debug('new pos: {}'.format(newPosition))
				pod.move(dt)
				#logger.debug('pod y: {}'.format(pod.SPRITE.y))

				if pod.SPRITE.y >= self.interface.window_height: #+ pod.SPRITE.height / 2:
					pod.SPRITE.y = 0

	def case_1_engage_node_state_machine(self, dt):
		for node in interface.ObjReg.node_registry:
			node.engageStateMachine()

	def case_1_check_pod_contact(self, dt):
		for node in interface.ObjReg.node_registry:
			for pod in interface.ObjReg.pod_registry:
				if node.isContact(pod):
					pod.hasContact()


	def case_1_master_clock_ticker(self, dt):
		self.interface.master_clock.startPulse()
	

if __name__ == "__main__":
	## Establish Data Files
        data_FILE = '/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/data_FILE.txt'
       # position_data_FILE = '/Users/TheTraveler/Workspace/PythonWorks/Pyglet_Works/position_data.txt'
	
	## Clear Data Files
	subprocess.call('rm {}'.format(data_FILE), shell=True)
	#subprocess.call('rm {}'.format(position_data_FILE), shell=True)

	## Create Logger Structure
	logging.basicConfig(level=logging.DEBUG, filename='logdump.log') # Top Level...everything goes into the diump
	
	logger = logging.getLogger('Process_Logger') # Log application process
	
	##TODO: Mess with format...make look nice
	#logger.format()

	console_handler = logging.StreamHandler()
	logger.addHandler(console_handler) ## Handler sends LogEvents to stderr
	logger.debug('Process_Logger Online')
	
	data_logger = logging.getLogger('data_logger')
	data_handler = logging.FileHandler(data_FILE)
	data_handler.setLevel(logging.INFO)
	data_logger.addHandler(data_handler)
	data_logger.info('Data_Logger Online')

	#time_logger = logging.getLogger('time_logger')
	#position_logger = logging.getLogger('position_logger')

	#logger.addHandler(time_logger)
	#logger.addHandler(position_logger)

	## Create Window
	interface = Interface(w=700, h=700, c="Interface")

	## Config
	config = Config.Config(interface)

	#position_data = logging.FileHandler(config.position_data)
	#position_data.setLevel(logging.INFO)
	

	## Run app
	pyglet.app.run()


